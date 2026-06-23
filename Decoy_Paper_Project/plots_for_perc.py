import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import *
from matplotlib_venn import venn2_unweighted
import glob
import os
import re

reversed_decoy_file = "/mnt/cargo/lorensha/Percolator_results/files/reversed_decoys"
decoy_variant_file = "/mnt/cargo/lorensha/Percolator_results/files/variant_decoys"
output_folder = "/mnt/cargo/lorensha/Percolator_results/venn_diagrams"

os.makedirs(output_folder, exist_ok=True)
combined_files = glob.glob(os.path.join(reversed_decoy_file, "*_final.csv"))

for reversed_decoy_path in combined_files:
    filename = os.path.basename(reversed_decoy_path)

    print(f"Processing file: {filename}")

    # Extract sample ID
    match = re.match(r"(.+)_final\.csv", filename)
    sample_id = match.group(1)

    # Find matching file (robust)
    pattern = os.path.join(decoy_variant_file, f"{sample_id}*_final.csv")
    matches = glob.glob(pattern)
    decoy_variant_path = matches[0]
    print(f"Found: {decoy_variant_path}")

    reversed_decoy_df = pd.read_csv(reversed_decoy_path)
    decoy_variant_df = pd.read_csv(decoy_variant_path)

    ## reversed decoy setup
    # round q-value and filter df for 1%
    # reversed_decoy_df['q-value'] = reversed_decoy_df['q-value'].round(3)
    # rd_qvalue_01 = reversed_decoy_df[reversed_decoy_df['q-value'] <= 0.01]
    rd_qvalue_01 = reversed_decoy_df
    # remove contaminant and redundant psms
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['psm_type1'] != 'canonical-no-ref']
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['psm_type1'] != 'contaminant']

    # select psms with target label = canonical psms only
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['Label_perc'] == 1]
    set1 = set(rd_qvalue_01['PSMId'])

    ## decoy variant setup
    # round q-value and filter df for 1%
    # decoy_variant_df['q-value'] = decoy_variant_df['q-value'].round(3)
    # dv_qvalue = decoy_variant_df[decoy_variant_df['q-value'] <= 0.01]
    dv_qvalue = decoy_variant_df
    # remove contaminant and redundant psms
    dv_qvalue = dv_qvalue[dv_qvalue['psm_type1'] != 'canonical-no-ref']
    dv_qvalue = dv_qvalue[dv_qvalue['psm_type1'] != 'contaminant']

    # select psms with target label = canonical psms only
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['Label_perc'] == 1]
    set2 = set(rd_qvalue_01['PSMId'])

    venn2_unweighted([set1, set2], set_labels=('reversed decoys PSMs', 'decoy variant PSMs'),
                     set_colors=('gold', 'cornflowerblue'), alpha=0.7)
    title = f"{sample_id} Venn diagram (1% q-value)"
    plt.title(title)

    #save figure

    output_path = os.path.join(output_folder, f"{sample_id}_venn.png")

    plt.savefig(output_path,bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Saved venn diagram to: {output_path}")
