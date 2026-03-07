"""Simple optimizer for SpO2 slope and intercept using polyfit on the AC/DC ratio and true SpO2 values from metadata."""

import os
import pandas as pd
import numpy as np
from typing import Callable
from src.common import calculate_frequency
from src.oximetry import calculate_spo2

def optimize_oxymetry_estimation(*,
    input_folder,
    metadata_file,
    verbose=False
) -> tuple[float, float]:
    """Compute slope and intercept by least-squares between ratio and true SpO2."""

    # Load metadata and collect samples
    metadata = pd.read_csv(metadata_file)
    samples: list[tuple[str, pd.DataFrame, float, float]] = []

    for file_name in os.listdir(input_folder):
        if not file_name.endswith(".csv"):
            continue
        file_path = os.path.join(input_folder, file_name)
        if file_path not in metadata['file'].values:
            if verbose:
                print(f"Archivo {file_path} no encontrado en metadata, omitiendo.")
            continue

        df = pd.read_csv(file_path, index_col=0)
        # If index is in seconds, convert to milliseconds for consistency
        if pd.api.types.is_float_dtype(df.index.dtype):
            df.index = (df.index * 1000).astype(int)

        fs = calculate_frequency(df.index.values)
        true_spo2 = float(metadata.loc[metadata['file'] == file_path, 'SpO2'].values[0])

        samples.append((file_path, df.copy(), fs, true_spo2))

    if not samples:
        raise ValueError("No se encontraron muestras válidas para optimizar.")

    # Compute AC/DC ratio and true SpO2 arrays using comprehensions
    ratios = [
        float(calculate_spo2(df_local["RED"].values, df_local["IR"].values, fs_local, slope=1.0, intercept=0.0))
        for _path, df_local, fs_local, _true_v in samples
    ]
    trues = [float(true_v) for _path, _df, _fs, true_v in samples]

    # Fit linear model ratio -> SpO2 using least squares
    slope_ls, intercept_ls = np.polyfit(ratios, trues, 1)

    if verbose:
        est_values = [
            calculate_spo2(df["RED"].values, df["IR"].values, fs, slope_ls, intercept_ls)
            for _p, df, fs, _ in samples
        ]
        mse = float(pd.Series([(e - t) ** 2 for e, t in zip(est_values, trues)]).mean())
        print("Least-squares solution:", {"slope": slope_ls, "intercept": intercept_ls, "mse": mse})

    return float(slope_ls), float(intercept_ls)


if __name__ == "__main__":
    slope, intercept = optimize_oxymetry_estimation(
            input_folder="./data/input/",
            metadata_file="./data/oximetry_metadata.csv",
            verbose=False
        )

    print(f"Optimized Slope: {slope}, Intercept: {intercept}")
