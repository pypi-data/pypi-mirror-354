from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from numpy.typing import NDArray
from scipy.signal import lfilter


@dataclass
class HydroEventDetector:

    date_range: NDArray[np.datetime64]
    streamflow: NDArray[np.float64]
    baseflow: NDArray[np.float64] | None = None
    events: pd.DataFrame | None = None
    dataframe: pd.DataFrame | None = None

    def baseflow_lyne_hollick(self, alpha: float = 0.987) -> None:
        """Estimates baseflow from streamflow using the Lyne-Hollick method.
    
        See: 
            * https://doi.org/10.7158/13241583.2013.11465417
            * https://doi.org/10.1029/WR026i007p01465
        """
        streamflow = self.streamflow
        
        if streamflow.size < 2:
            raise ValueError("at least two elements")
    
        # Coefficients for the IIR filter
        b = [(1 + alpha) / 2]  # numerator
        a = [1, -alpha]        # denominator
    
        # --- Forward filter ---
        dq = np.diff(streamflow, prepend=streamflow[0])  # prepend to keep same length
        qf_forward = lfilter(b, a, dq)
    
        # --- Backward filter ---
        dq_rev = np.diff(streamflow[::-1], prepend=streamflow[-1])
        qf_backward = lfilter(b, a, dq_rev)[::-1]   
    
        # --- baseflow and quickflow ---
        quickflow = (qf_forward + qf_backward) / 2
        baseflow = streamflow - quickflow
        baseflow = np.clip(baseflow, 0, streamflow)
    
        self.baseflow = baseflow
    
    def detect_events(
        self,
    ) -> pd.DataFrame:

        date_range = self.date_range
        streamflow = self.streamflow
        baseflow = self.baseflow
        
        dates_dt = pd.to_datetime(date_range)
        n = len(streamflow)
    
        mask = streamflow > baseflow
        changes = np.diff(mask.astype(int))
    
        idx_start = np.where(changes == 1)[0]  # one position before the crossing
        idx_end = np.where(changes == -1)[0] + 1
    
        # Edge cases
        if mask[0]:
            idx_start = np.insert(idx_start, 0, 0)
        if mask[-1]:
            idx_end = np.append(idx_end, n - 1)
        if idx_end[0] < idx_start[0]:
            idx_end = idx_end[1:]
        if len(idx_start) > len(idx_end):
            idx_start = idx_start[:len(idx_end)]
    
        events = []
    
        for i_start, i_end in zip(idx_start, idx_end):
            if i_end <= i_start:
                continue  # inválid
    
            i_peak = i_start + np.argmax(streamflow[i_start:i_end + 1])
    
            # Peak index cannot match an start or end indices
            if i_peak == i_start or i_peak == i_end:
                continue
    
            events.append({
                "i_start": i_start,
                "i_peak": i_peak,
                "i_end": i_end,
            })
    
        self.events = pd.DataFrame(events)

    
    def filter_events(
            self,
            percentile: int = 95,
        ) -> pd.DataFrame:

        events_df = self.events
        baseflow = self.baseflow
        streamflow = self.streamflow
        
        peak_indices = events_df.i_peak.values
    
        peak_streamflow = streamflow[peak_indices]
        peak_baseflow = baseflow[peak_indices]
        peak_quickflow = peak_streamflow - peak_baseflow
    
        threshold = np.percentile(peak_quickflow[peak_quickflow > 0], percentile) #
        
        significant_peaks_mask = peak_quickflow >= threshold
        significant_events_df = events_df[significant_peaks_mask]
    
        print(f"📈 95th percentile (baseflow): {threshold:.2f}")
        print(f"🔍 Number of peaks after the filter: {len(significant_events_df)}")
    
        self.events = significant_events_df
    
    
    def create_events_dataframe(self,
                                
    ) -> pd.DataFrame:
        """
        Constructs a filtered and enriched DataFrame of significant hydrologic events.
    
        Args:
            events_df (pd.DataFrame): DataFrame with columns ['i_start', 'i_peak', 'i_end'].
            streamflow (np.ndarray): Streamflow values aligned with the date_range.
            baseflow (np.ndarray): Baseflow values aligned with the date_range.
            date_range (np.ndarray): Array of datetime64 aligned with streamflow/baseflow.
    
        Returns:
            pd.DataFrame: Clean DataFrame with dates, values, monthly info, and volumes.
        """

        date_range = self.date_range
        streamflow = self.streamflow
        baseflow = self.baseflow
        events_df = self.events


        
        # Extract index arrays
        i_start_arr = events_df["i_start"]
        i_peak_arr = events_df["i_peak"]
        i_end_arr = events_df["i_end"]
    
        # Build enrichment DataFrame
        
        enrichment_df = pd.DataFrame({
            "date_start": date_range[i_start_arr],
            "date_peak": date_range[i_peak_arr],
            "date_end": date_range[i_end_arr],
            "flow_start": streamflow[i_start_arr],
            "flow_peak": streamflow[i_peak_arr],
            "flow_end": streamflow[i_end_arr],
            "baseflow_start": baseflow[i_start_arr],
            "baseflow_peak": baseflow[i_peak_arr],
            "baseflow_end": baseflow[i_end_arr],
        })
        
        # Month info
        dt_peaks = pd.to_datetime(enrichment_df["date_peak"])
        enrichment_df["month_num"] = dt_peaks.dt.month
        enrichment_df["month_name"] = dt_peaks.dt.month_name()
        
        # Time interval in seconds
        delta_seconds = np.median(np.diff(date_range).astype('timedelta64[s]').astype(int))
        
        # Volume computation
    
        n = len(streamflow)
        event_ids = np.full(n, -1, dtype=int)
        for eid, (start, end) in enumerate(zip(i_start_arr, i_end_arr)):
            event_ids[start:end + 1] = eid
    
        valid_mask = event_ids >= 0
        sf_values = streamflow[valid_mask]
        bf_values = baseflow[valid_mask]
        ids = event_ids[valid_mask]
        
        volume_sf = np.bincount(ids, weights=sf_values) * delta_seconds
        volume_bf = np.bincount(ids, weights=bf_values) * delta_seconds
        
        enrichment_df["event_volume"] = volume_sf
        enrichment_df["baseflow_volume"] = volume_bf
        
        # Combine and return final DataFrame
        final_df = pd.concat([events_df.reset_index(drop=True), enrichment_df], axis=1)
        
        self.dataframe = final_df[[
            "date_start", "flow_start", "baseflow_start",
            "date_peak", "flow_peak", "baseflow_peak",
            "date_end", "flow_end", "baseflow_end",
            "month_num", "month_name",
            "event_volume", "baseflow_volume",]]
    
    def plot_events(
        self, 
        start: str,
        end: str,
    ) -> None:
        """
        Plot streamflow and baseflow with annotated significant events, split by year.
        
        Args:
            dates (np.ndarray): Full datetime range.
            streamflow (np.ndarray): Array of streamflow values.
            baseflow (np.ndarray): Array of baseflow values.
            events_df (pd.DataFrame): DataFrame with filtered and enriched significant events.
        """

        dates = self.date_range
        streamflow = self.streamflow
        baseflow = self.baseflow
        events_df = self.dataframe

        
        start_np = np.datetime64(start)
        end_np = np.datetime64(end)
    
        # Convert to pandas Series for easier slicing
        sf_series = pd.Series(streamflow, index=pd.to_datetime(dates))
        bf_series = pd.Series(baseflow, index=pd.to_datetime(dates))
        
        sf_slice = sf_series[start_np:end_np]
        bf_slice = bf_series[start_np:end_np]
    
        # Filter events
        events_slice = events_df[
            (events_df["date_end"] >= start_np) &
            (events_df["date_start"] <= end_np)
        ]
        
        fig = go.Figure()
        
        # Add lines for streamflow and baseflow
        fig.add_trace(go.Scatter(
            x=sf_slice.index, y=sf_slice.values,
            mode="lines", name="Streamflow", line=dict(width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=bf_slice.index, y=bf_slice.values,
            mode="lines", name="Baseflow", line=dict(width=1.5, dash="dot")
        ))
    
        # Add event start and end points
        fig.add_trace(go.Scatter(
            x=events_slice["date_start"], y=events_slice["flow_start"],
            mode="markers", name="Start", marker=dict(symbol="circle", size=6)
        ))
        fig.add_trace(go.Scatter(
            x=events_slice["date_end"], y=events_slice["flow_end"],
            mode="markers", name="End", marker=dict(symbol="x", size=6)
        ))
    
        # Add event peak values
        fig.add_trace(go.Scatter(
            x=events_slice["date_peak"], y=events_slice["flow_peak"],
            mode="markers", name="Peak Flow", marker=dict(symbol="diamond", size=8)
        ))
        fig.add_trace(go.Scatter(
            x=events_slice["date_peak"], y=events_slice["baseflow_peak"],
            mode="markers", name="Peak Baseflow", marker=dict(symbol="star", size=8)
        ))
    
        fig.update_layout(
            title=f"Hydrologic Events From {start} To {end}",
            xaxis_title="Date",
            yaxis_title="Flow (cfs)",
            legend_title="Legend",
            height=600
        )
        fig.show()
