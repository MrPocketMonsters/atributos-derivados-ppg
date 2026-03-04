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

# TODO: These fixtures must be calibrated based on empirical data
OXYMETRY_SLOPE_FIXTURE = 0.5  # Coefficient for calculating SpO2 from RED and IR signals
OXYMETRY_INTERCEPT_FIXTURE = 0.5  # Intercept for calculating SpO2 from RED and IR signals
