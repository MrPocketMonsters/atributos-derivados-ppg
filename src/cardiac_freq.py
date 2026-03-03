"""Functions for calculating cardiac frequency attributes."""

import numpy as np
from scipy.signal import find_peaks
from .common import bandpass_filter, robust_normalize
from .config import TACHYCARDIA_THRESHOLD



def intervals_in_seconds(ppg_signal: np.ndarray, fs: float) -> np.ndarray:
    """Calculates the intervals between heartbeats in seconds from a PPG signal."""

    # Common processing steps:
    filtered_signal = bandpass_filter(ppg_signal, lowcut=0.5, highcut=4.0, fs=fs)
    normalized_signal = robust_normalize(filtered_signal)

    # Find the peaks in the normalized signal, expecting them to correspond to heartbeats.
    peaks, _ = find_peaks(normalized_signal, distance=fs*0.5)  # Minimum distance of 0.5 seconds between peaks
    if len(peaks) < 2:
        return 0.0  # Not enough peaks to calculate heart rate

    peak_intervals = np.diff(peaks) / fs  # Convert to seconds
    return peak_intervals


def calculate_cardiac_frequency(ppg_signal: np.ndarray, fs: float) -> float:
    """Calculates the cardiac frequency (heart rate) from a PPG signal."""

    intervals = intervals_in_seconds(ppg_signal, fs)
    average_interval = np.mean(intervals)  # Average interval between heartbeats in seconds
    heart_rate_bpm = 60 / average_interval  # Convert to BPM

    return heart_rate_bpm


def calculate_cardiac_frequency_variability(ppg_signal: np.ndarray, fs: float) -> float:
    """Calculates the variability of the cardiac frequency from a PPG signal."""

    intervals = intervals_in_seconds(ppg_signal, fs)
    variability = np.std(intervals)  # Standard deviation of the intervals as a measure of variability

    return variability


def is_tachycardic(ppg_signal: np.ndarray, fs: float) -> bool:
    """Determines if the cardiac frequency indicates tachycardia."""

    heart_rate_bpm = calculate_cardiac_frequency(ppg_signal, fs)
    return heart_rate_bpm > TACHYCARDIA_THRESHOLD
