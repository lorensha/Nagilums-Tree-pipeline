import pandas as pd
import glob
import os
import re

folder1 = "/mnt/cargo/lorensha/PXD010154_tonsil_trypsin/reversed_decoys/percolator/"      # where *_combined.txt files live
folder2 = "/mnt/cargo/lorensha/PXD010154_tonsil_trypsin/reversed_decoys"    # where *_percolator_input_extended.tsv files live
output_folder = "/mnt/cargo/lorensha/Percolator_results/"

# Get all combined.txt files
subfolders = [f.path for f in os.scandir(folder1) if f.is_dir()]

for subfolder in subfolders:
    combined_files = glob.glob(os.path.join(subfolder, "*_combined.txt"))

    if not combined_files:
        print(f"No combined file in {subfolder}")
        continue

    combined_path = combined_files[0]  # assuming one per folder
    filename = os.path.basename(combined_path)

    print(f"Processing file: {filename}")

    # Extract sample ID
    match = re.match(r"(.+)_combined\.txt", filename)
    if not match:
        print(f"Could not extract ID from {filename}")
        continue

    sample_id = match.group(1)

    # Build matching file
    percolator_path = os.path.join(folder2, f"{sample_id}_percolator_input_extended.tsv")

    print(f"Looking for: {percolator_path}")

    if not os.path.exists(percolator_path):
        print(f"No matching percolator file for {sample_id}")
        continue

    # Read files
    df_combined = pd.read_csv(combined_path)
    print(df_combined.head())
    df_wFV = pd.read_csv(percolator_path)
    print(df_wFV.head())
    df_wFV = df_wFV.rename(columns={"PSMiD": "PSMId"})

    # Merge
    merged_results = df_wFV.merge(df_combined, on='PSMId', how='inner')

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, f"{sample_id}_wFV.csv")
    merged_results.to_csv(output_path, index=False)

    print(f"Combined: {sample_id} -> {output_path} ({merged_results.shape[0]} rows)")
