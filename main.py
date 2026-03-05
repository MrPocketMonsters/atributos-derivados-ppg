import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.oximetry import calculate_spo2
from src.cardiac_freq import (
    calculate_cardiac_frequency,
    calculate_cardiac_frequency_variability,
    is_tachycardic,
)
from src.common import (
  calculate_frequency,
  bandpass_filter,
  robust_normalize,
)
from src.config import (
  COLUMNS,
  COLUMNS_COLORS,
)



def process(in_df: pd.DataFrame, fs: float) -> pd.DataFrame:
    """Processes the input DataFrame to calculate cardiac frequency attributes."""

    # Process each row in the DataFrame
    results = []
    for col in COLUMNS:
        ppg_signal = in_df[col].values
        heart_rate = calculate_cardiac_frequency(ppg_signal, fs)
        variability = calculate_cardiac_frequency_variability(ppg_signal, fs)
        tachycardic = is_tachycardic(ppg_signal, fs)

        results.append({
            "Column": col,
            "Heart Rate (BPM)": heart_rate,
            "Frequency Variability (s)": variability,
            "Tachycardic": tachycardic,
        })

    return pd.DataFrame(results)


def draw_plot(input: pd.DataFrame, name: str, output_path: str) -> None:
    """Draws a plot of the PPG signals from the input DataFrame and saves it to the specified output path."""

    x_axis = input.index.values
    x_axis_seconds = (x_axis - x_axis[0]) / 1000.0  # Convert to seconds
    x_axis_seconds = x_axis_seconds - x_axis_seconds[0]  # Normalize to start at 0 seconds
    plt.figure(figsize=(12, 6))
    for col in COLUMNS:
        plt.plot(x_axis_seconds, input[col], label=col, color=COLUMNS_COLORS[col])
    plt.title(f"PPG Signals - {name}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.savefig(output_path)


def main():
    """Main function to execute the cardiac frequency analysis pipeline."""

    # Load PPG data from CSV
    file_names = os.listdir(os.path.join("data", "input"))
    for file_name in file_names:
        input_path = os.path.join("data", "input", file_name)
        in_df = pd.read_csv(input_path, index_col=0)

        if not all(col in in_df.columns for col in COLUMNS):
            raise ValueError(f"Input CSV must contain the following columns: {COLUMNS}")

        # if the index is float, it means it has been converted to seconds. Multiply by 1000 and convert to int
        if in_df.index.dtype == float:
            in_df.index = (in_df.index * 1000).astype(int)

        # Calculate sampling frequency from index timestamps
        fs = calculate_frequency(in_df.index.values)

        # Process the input DataFrame
        out_df = process(in_df, fs)

        # Calculate SpO2 using the RED and IR signals
        spo2 = calculate_spo2(in_df["RED"].values, in_df["IR"].values, fs)
        out_df["Estimated SpO2"] = spo2

        # Do common processing on the input
        proc_in_df = in_df.copy()
        for col in COLUMNS:
            proc_in_df[col] = bandpass_filter(proc_in_df[col].values, fs)
            proc_in_df[col] = robust_normalize(proc_in_df[col].values)

        # Get name of the input file without extension for output naming
        file_name_prefix = os.path.splitext(file_name)[0]

        # Draw processed input DataFrame
        img_output_name = file_name_prefix + "_processed-plot.png"
        img_output_path = os.path.join("data", "output", img_output_name)
        draw_plot(proc_in_df, file_name, img_output_path)
        print(f"Plot saved to {img_output_path}")

        # Save results to output CSV
        csv_output_path = os.path.join("data", "output", file_name_prefix + "_derived-data.csv")
        out_df.to_csv(csv_output_path, index=False)
        print(f"Results saved to {csv_output_path}")


if __name__ == "__main__":
    main()
