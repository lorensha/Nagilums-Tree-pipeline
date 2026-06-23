import pandas as pd
import os
import glob

percolator_files_dir = '/mnt/cargo/lorensha/PXD010154_tonsil_trypsin/decoy_variants/percolator/'
cols = ["PSMId", "score", "q-value", "posterior_error_prob", "peptide", "proteinIds"]

subfolders = [f.path for f in os.scandir(percolator_files_dir) if f.is_dir()]

for folder in subfolders:
    target_file = os.path.join(folder, "percolator.target.peptides.txt")
    decoy_file  = os.path.join(folder, "percolator.decoy.peptides.txt")

    target_psms = pd.read_table(target_file ,sep='\t',
                           names=cols, header=0, usecols=range(len(cols)))

    decoy_psms = pd.read_table(decoy_file ,sep='\t',
                           names=cols, header=0, usecols=range(len(cols)))
    decoy_psms["Label_perc"] = -1
    target_psms["Label_perc"] = 1

    Percolator_results = pd.concat([target_psms, decoy_psms], ignore_index=True)

    folder_name = os.path.basename(folder)
    output_path = os.path.join(folder, f"{folder_name}_combined.txt")
    Percolator_results.to_csv(output_path, index=False)

    print(f"Combined: {output_path}  ({Percolator_results.shape[0]} rows)")
