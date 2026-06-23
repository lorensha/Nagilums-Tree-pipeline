import pandas as pd
import glob
import os
import re

folder1 = "/mnt/cargo/lorensha/Percolator_results/"
folder2 = "/mnt/cargo/lorensha/reversed_decoys_results"
output_folder = "/mnt/cargo/lorensha/Percolator_results/"

combined_files = glob.glob(os.path.join(folder1, "*_wFV.csv"))

for combined_path in combined_files:
    filename = os.path.basename(combined_path)

    print(f"Processing file: {filename}")

    # Extract sample ID
    match = re.match(r"(.+)_wFV\.csv", filename)
    if not match:
        print(f"Could not extract ID from {filename}")
        continue

    sample_id = match.group(1)

    # Find matching file (robust)
    pattern = os.path.join(folder2, f"{sample_id}*_PSM_variant_info.csv")
    matches = glob.glob(pattern)

    if not matches:
        print(f"No matching file for {sample_id}")
        continue

    percolator_path = matches[0]
    print(f"Found: {percolator_path}")

    # Read files
    df_combined = pd.read_csv(combined_path)
    df_combined = df_combined.rename(columns={"PSMiD": "PSMId"})
    df_all = pd.read_csv(percolator_path)
    df_all = df_all.rename(columns={"PSMiD": "PSMId"})

    # Merge
    merged_results = df_all.merge(df_combined, on='PSMId', how='inner')

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, f"{sample_id}_final.csv")
    merged_results.to_csv(output_path, index=False)

    print(f"Combined: {sample_id} -> {output_path} ({merged_results.shape[0]} rows)")
