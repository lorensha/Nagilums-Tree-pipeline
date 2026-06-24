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

output_folder_violin_plot = "/mnt/cargo/lorensha/Percolator_results/violin_plots"

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
    reversed_decoy_df['q-value'] = reversed_decoy_df['q-value'].round(3)
    rd_qvalue_01 = reversed_decoy_df[reversed_decoy_df['q-value'] <= 0.01]

    # remove contaminant and redundant psms
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['psm_type1'] != 'canonical-no-ref']
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['psm_type1'] != 'contaminant']

    # select psms with target label = canonical psms only
    rd_qvalue_01 = rd_qvalue_01[rd_qvalue_01['Label_perc'] == 1]
    set1 = set(rd_qvalue_01['PSMId'])

    ## decoy variant setup
    # round q-value and filter df for 1%
    decoy_variant_df['q-value'] = decoy_variant_df['q-value'].round(3)
    dv_qvalue = decoy_variant_df[decoy_variant_df['q-value'] <= 0.01]

    # remove contaminant and redundant psms
    dv_qvalue = dv_qvalue[dv_qvalue['psm_type1'] != 'canonical-no-ref']
    dv_qvalue = dv_qvalue[dv_qvalue['psm_type1'] != 'contaminant']

    # select psms with target label = canonical psms only
    dv_qvalue = dv_qvalue[dv_qvalue['Label_perc'] == 1]
    set2 = set(dv_qvalue['PSMId'])

    ## making the venn

    venn2_unweighted([set1, set2], set_labels=('reversed decoys PSMs', 'decoy variant PSMs'),
                     set_colors=('gold', 'cornflowerblue'), alpha=0.7)
    title = f"{sample_id} Venn diagram (1% q-value)"
    plt.title(title)

    #save figure

    output_path = os.path.join(output_folder, f"{sample_id}_venn.png")

    plt.savefig(output_path,bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Saved venn diagram to: {output_path}")

    ## violin plot - reversed decoys

    df_title = title

    df = reversed_decoy_df[reversed_decoy_df['q-value'] <= 0.01]
    yaxis = "rt_Abs_error"
    xaxis_psmtype = "psm_type1"

    order = ["canonical", "single-variant", "multi-variant", "frameshift", "decoy"]

    counts = df[xaxis_psmtype].value_counts()

    labels = [f"{uid}\n(n={counts.get(uid, 0)})" for uid in order]

    data_per_id = [
        df.loc[df[xaxis_psmtype] == uid, yaxis].dropna().values
        for uid in order
    ]

    # Warn if any identifier has too few points
    for uid, d in zip(order, data_per_id):
        if len(d) < 2:
            print(f"Warning: '{uid}' has only {len(d)} rows — violin will not render")

    fig, ax = plt.subplots(figsize=(max(8, len(order) * 0.8), 6))

    parts = ax.violinplot(
        data_per_id,
        positions=range(len(order)),
        showmedians=True,
        showextrema=True,
    )

    decoy_idx = order.index("decoy")

    for i, body in enumerate(parts["bodies"]):
        if i == decoy_idx:
            body.set_facecolor("coral")
            body.set_edgecolor("darkred")
        else:
            body.set_facecolor("cornflowerblue")
            body.set_edgecolor("black")
        body.set_alpha(0.75)

    parts["cmedians"].set_color("white")
    parts["cmaxes"].set_color("black")
    parts["cmins"].set_color("black")
    parts["cbars"].set_color("black")

    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(labels, rotation=45, ha="center", fontsize=9)
    ax.set_xlabel("PSM type", fontsize=12)
    ax.set_ylabel("rt_Abs_error", fontsize=12)
    ax.set_title(df_title + " reversed decoys: Abs error distribution per PSM type (q-value 1%)", fontsize=13)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    # save figure

    output_path = os.path.join(output_folder_violin_plot, f"{sample_id}_violin_plot.png")

    plt.savefig(output_path, bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Saved violin diagram rd to: {output_path}")

    ## violin plot - decoy variants
    df_title = title

    df_dv = decoy_variant_df[decoy_variant_df['q-value'] <= 0.01]
    yaxis = "rt_Abs_error"
    xaxis_psmtype = "psm_type1"

    order = ["canonical", "single-variant", "multi-variant", "frameshift", "decoy"]

    counts = df_dv[xaxis_psmtype].value_counts()

    labels = [f"{uid}\n(n={counts.get(uid, 0)})" for uid in order]

    data_per_id = [
        df_dv.loc[df_dv[xaxis_psmtype] == uid, yaxis].dropna().values
        for uid in order
    ]

    # Warn if any identifier has too few points
    for uid, d in zip(order, data_per_id):
        if len(d) < 2:
            print(f"Warning: '{uid}' has only {len(d)} rows — violin will not render")

    fig, ax = plt.subplots(figsize=(max(8, len(order) * 0.8), 6))

    parts = ax.violinplot(
        data_per_id,
        positions=range(len(order)),
        showmedians=True,
        showextrema=True,
    )

    decoy_idx = order.index("decoy")

    for i, body in enumerate(parts["bodies"]):
        if i == decoy_idx:
            body.set_facecolor("coral")
            body.set_edgecolor("darkred")
        else:
            body.set_facecolor("cornflowerblue")
            body.set_edgecolor("black")
        body.set_alpha(0.75)

    parts["cmedians"].set_color("white")
    parts["cmaxes"].set_color("black")
    parts["cmins"].set_color("black")
    parts["cbars"].set_color("black")

    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(labels, rotation=45, ha="center", fontsize=9)
    ax.set_xlabel("PSM type", fontsize=12)
    ax.set_ylabel("rt_Abs_error", fontsize=12)
    ax.set_title(df_title + " decoy variant: Abs error distribution per PSM type (q-value 1%)", fontsize=13)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    # save figure

    output_path = os.path.join(output_folder_violin_plot, f"{sample_id}_violin_plot.png")

    plt.savefig(output_path, bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Saved violin diagram dv to: {output_path}")
