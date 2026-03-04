"""Module for estimating SpO2 from RED and IR PPG signals."""

import numpy as np
from scipy.signal import find_peaks

from .common import bandpass_filter
from .config import (
    OXYMETRY_INTERCEPT_FIXTURE,
    OXYMETRY_SLOPE_FIXTURE,
)

def _find_ac_dc_relation(signal: np.ndarray, fs: float) -> float:
    """Finds the AC/DC relation for a given PPG signal."""

    # Apply bandpass filter to isolate the pulsatile component
    filtered_signal = bandpass_filter(signal, fs)

    # Find peaks in the filtered signal
    peaks, _ = find_peaks(filtered_signal)
    if len(peaks) == 0:
        raise ValueError("No peaks found in the signal. Cannot calculate AC/DC relation.")

    # Calculate AC and DC components
    ac_component = np.mean(filtered_signal[peaks])  # Average of peak values
    dc_component = np.mean(signal)  # Average of the original signal
    if dc_component == 0:
        raise ValueError("DC component is zero. Cannot calculate AC/DC relation.")

    return ac_component / dc_component

def calculate_spo2(red_signal: np.ndarray, ir_signal: np.ndarray, fs: float) -> np.ndarray:
    """Calculates the estimated SpO2 from the RED and IR signals using a linear model."""

    red_relation = _find_ac_dc_relation(red_signal, fs)
    ir_relation = _find_ac_dc_relation(ir_signal, fs)
    ir_relation = max(ir_relation, 1e-6)  # Avoid division by zero
    ratio = red_relation / ir_relation

    # Apply the linear model to estimate SpO2
    spo2 = OXYMETRY_SLOPE_FIXTURE * ratio + OXYMETRY_INTERCEPT_FIXTURE

    return spo2
