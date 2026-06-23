import pandas as pd
import glob
import os
import re

folder1 = "/mnt/cargo/lorensha/PXD010154_tonsil_trypsin/reversed_decoys/percolator/"      # where *_combined.txt files live
folder2 = "/mnt/cargo/lorensha/PXD010154_tonsil_trypsin/reversed_decoys"    # where *_percolator_input_extended.tsv files live
output_folder = "/mnt/cargo/lorensha/Percolator_results/"

# Get all combined.txt files
subfolders = [f.path for f in os.scandir(folder1) if f.is_dir()]

for combined_path in subfolders:
    filename = os.path.basename(combined_path)

    # Extract the ID prefix, e.g. 'SAMEA7718756'
    match = re.match(r"(.+)_combined\.txt", filename)
    if not match:
        print(f"Could not extract ID from {filename}")
        continue

    sample_id = match.group(1)

    # Build the matching percolator file path
    percolator_path = os.path.join(folder2, f"{sample_id}_percolator_input_extended.tsv")

    if not os.path.exists(percolator_path):
        print(f"No matching percolator file for {sample_id}")
        continue

    # Read both files
    df_combined = pd.read_csv(combined_path, sep="\t")
    df_wFV = pd.read_csv(percolator_path, sep="\t")
    df_wFV = df_wFV.rename(columns={"PSMiD": "PSMId"})

    # merge
    merged_results = df_wFV.merge(df_combined, on='PSMId', how='inner')

    # Save with sample ID in the name
    output_path = os.path.join(output_folder, f"{sample_id}_wFV.csv")
    merged_results.to_csv(output_path, sep="\t", index=False)

    print(f"Combined: {sample_id} -> {output_path} ({merged_results.shape[0]} rows)")
