import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.cardiac_freq import (
    calculate_cardiac_frequency,
    calculate_cardiac_frequency_variability,
    is_tachycardic
)
from src.common import calc_diff, bandpass_filter, robust_normalize
from src.config import COLUMNS, COLUMNS_COLORS

def process(input: pd.DataFrame) -> pd.DataFrame:
    """Processes the input DataFrame to calculate cardiac frequency attributes."""

    # Calculate sampling frequency from index timestamps
    fs = calc_diff(input.index.values)

    # Process each row in the DataFrame
    results = []
    for col in COLUMNS:
        ppg_signal = input[col].values
        heart_rate = calculate_cardiac_frequency(ppg_signal, fs)
        variability = calculate_cardiac_frequency_variability(ppg_signal, fs)
        tachycardic = is_tachycardic(ppg_signal, fs)

        results.append({
            "Column": col,
            "Heart Rate (BPM)": heart_rate,
            "Frequency Variability (s)": variability,
            "Tachycardic": tachycardic
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

    parser = argparse.ArgumentParser(description="Calculate cardiac frequency attributes from PPG data.")
    parser.add_argument(
        "input_csv",
        type=str,
        help="Name of the input CSV file containing PPG data with columns: RED, IR, GREEN. Must be in $PWD/data/input"
    )
    args = parser.parse_args()

    # Load PPG data from CSV
    input_relpath = os.path.join("data", "input", args.input_csv)
    in_df = pd.read_csv(input_relpath, index_col=0)
    if not all(col in in_df.columns for col in COLUMNS):
        raise ValueError(f"Input CSV must contain the following columns: {COLUMNS}")

    # Process the input DataFrame
    out_df = process(in_df)

    # Do common processing on the input
    proc_in_df = in_df.copy()
    for col in COLUMNS:
        proc_in_df[col] = bandpass_filter(proc_in_df[col].values, lowcut=0.5, highcut=4.0, fs=100)
        proc_in_df[col] = robust_normalize(proc_in_df[col].values)

    # Draw processed input DataFrame
    img_output_name = os.path.splitext(args.input_csv)[0] + ".png"
    img_output_path = os.path.join("data", "output", img_output_name)
    draw_plot(proc_in_df, args.input_csv, img_output_path)
    print(f"Plot saved to {img_output_path}")

    # Save results to output CSV
    csv_output_path = os.path.join("data", "output", args.input_csv)
    out_df.to_csv(csv_output_path, index=False)
    print(f"Results saved to {csv_output_path}")

if __name__ == "__main__":
    main()
