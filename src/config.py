"""Configuration constants for cardiac frequency analysis."""

COLUMNS = ["RED","IR","GREEN"]
COLUMNS_COLORS = {
    "RED": "red",
    "IR": "black",
    "GREEN": "green"
}

DEFAULT_LOWCUT = 0.5  # Hz
DEFAULT_HIGHCUT = 4.0  # Hz

TACHYCARDIA_THRESHOLD = 100  # BPM

DEFAULT_OXIMETRY_SLOPE = 1.4177638841095033 # Slope for calculating SpO2 from RED and IR signals
DEFAULT_OXIMETRY_INTERCEPT = -0.18531754985453078 # Intercept for calculating SpO2 from RED and IR signals
