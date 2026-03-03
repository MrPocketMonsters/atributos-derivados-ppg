"""Common utility functions for signal processing."""

import numpy as np
from scipy.signal import butter, filtfilt



def calculate_frequency(x: np.ndarray) -> np.ndarray:
    """Calculates the estimated frequency of the input array x."""
    diff_time = np.mean(np.diff(x)) / 1000.0 # Convert to seconds
    return 1.0 / diff_time


def bandpass_filter(x: np.ndarray, lowcut: float, highcut: float, fs: float) -> np.ndarray:
    """Applies a Butterworth bandpass filter to the input signal x."""
    nyq = fs * 0.5
    b, a = butter(4, [lowcut / nyq, highcut / nyq], btype="band")
    return filtfilt(b, a, x)


def robust_normalize(x: np.ndarray) -> np.ndarray:
    """Applies robust normalization to the input signal x."""
    x = np.asarray(x, dtype=np.float32)
    med = np.median(x)
    mad = np.median(np.abs(x - med)) + 1e-8
    return (x - med) / mad
