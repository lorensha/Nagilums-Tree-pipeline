import pandas as pd
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

# MODY gene .txt file to list for iteration
MODY_file = pd.read_table('MD_genes_new.txt', header=None)
MODY_file_to_List = MODY_file.values.tolist()
MODY_list = [item for sublist in MODY_file_to_List for item in sublist]

# create dataframe of all MODY genes
MODY_df = pd.DataFrame(MODY_list, columns=['gene_id'])
MODY_df = MODY_df.set_index("gene_id")

# STEM FILE 01
stem_file_01_df = pd.read_csv('Decoy Variant Stem Cell File 1.csv', header=0)
stem_file_01_df = stem_file_01_df[stem_file_01_df['pep_scores'] <= 1.0]
# stem_file_01_df = stem_file_01_df[stem_file_01_df['Probability P(-1)'] < 0.5]
# remove decoys of canonical and variants
stem_file_01_df = stem_file_01_df[stem_file_01_df['psm_type'] != 'target_seq_decoy_var']
stem_file_01_df = stem_file_01_df[stem_file_01_df['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_01_df.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_01_df.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_01_df.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: wild type_01'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 02
stem_file_02_df = pd.read_csv('Decoy Variant Stem Cell File 2.csv', header=0)
stem_file_02_df = stem_file_02_df[stem_file_02_df['pep_scores'] <= 1.0]

# remove decoys of canonical and variants
stem_file_02_df = stem_file_02_df[stem_file_02_df['psm_type'] != 'target_seq_decoy_var']
stem_file_02_df = stem_file_02_df[stem_file_02_df['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_02_df.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_02_df.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_02_df.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: wild type_02'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)
# df3 = pd.merge(MODY_df, append_filtered_genes_to_MODY, left_index=True, right_index=True)

# STEM FILE 03
stem_file_df_03 = pd.read_csv('Decoy Variant Stem Cell File 3.csv', header=0)
stem_file_df_03 = stem_file_df_03[stem_file_df_03['pep_scores'] <= 1.0]
# stem_file_df_03 = stem_file_df_03[stem_file_df_03['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_03 = stem_file_df_03[stem_file_df_03['psm_type'] != 'target_seq_decoy_var']
stem_file_df_03 = stem_file_df_03[stem_file_df_03['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_03.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_03.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_03.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: wild type_03'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 04
stem_file_df_04 = pd.read_csv('Decoy Variant Stem Cell File 4.csv', header=0)
stem_file_df_04 = stem_file_df_04[stem_file_df_04['pep_scores'] <= 1.0]
# stem_file_df_04 = stem_file_df_04[stem_file_df_04['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_04 = stem_file_df_04[stem_file_df_04['psm_type'] != 'target_seq_decoy_var']
stem_file_df_04 = stem_file_df_04[stem_file_df_04['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_04.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_04.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_04.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: Mutant_01'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 05
stem_file_df_05 = pd.read_csv('Decoy Variant Stem Cell File 5.csv', header=0)
stem_file_df_05 = stem_file_df_05[stem_file_df_05['pep_scores'] <= 1.0]
# stem_file_df_05 = stem_file_df_05[stem_file_df_05['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_05 = stem_file_df_05[stem_file_df_05['psm_type'] != 'target_seq_decoy_var']
stem_file_df_05 = stem_file_df_05[stem_file_df_05['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_05.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_05.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_05.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: Mutant_02'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 06
stem_file_df_06 = pd.read_csv('Decoy Variant Stem Cell File 6.csv', header=0)
stem_file_df_06 = stem_file_df_06[stem_file_df_06['pep_scores'] <= 1.0]
# stem_file_df_06 = stem_file_df_06[stem_file_df_06['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_06 = stem_file_df_06[stem_file_df_06['psm_type'] != 'target_seq_decoy_var']
stem_file_df_06 = stem_file_df_06[stem_file_df_06['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_06.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_06.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_06.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 0: Mutant_03'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 07
stem_file_df_07 = pd.read_csv('Decoy Variant Stem Cell File 7.csv', header=0)
stem_file_df_07 = stem_file_df_07[stem_file_df_07['pep_scores'] <= 1.0]
# stem_file_df_07 = stem_file_df_07[stem_file_df_07['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_07 = stem_file_df_07[stem_file_df_07['psm_type'] != 'target_seq_decoy_var']
stem_file_df_07 = stem_file_df_07[stem_file_df_07['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_07.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_07.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_07.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: wild type_01'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 08
stem_file_df_08 = pd.read_csv('Decoy Variant Stem Cell File 8.csv', header=0)
stem_file_df_08 = stem_file_df_08[stem_file_df_08['pep_scores'] <= 1.0]
# stem_file_df_08 = stem_file_df_08[stem_file_df_08['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_08 = stem_file_df_08[stem_file_df_08['psm_type'] != 'target_seq_decoy_var']
stem_file_df_08 = stem_file_df_08[stem_file_df_08['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_08.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_08.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_08.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: wild type_02'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 09
stem_file_df_09 = pd.read_csv('Decoy Variant Stem Cell File 9.csv', header=0)
stem_file_df_09 = stem_file_df_09[stem_file_df_09['pep_scores'] <= 1.0]
# stem_file_df_09 = stem_file_df_09[stem_file_df_09['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_09 = stem_file_df_09[stem_file_df_09['psm_type'] != 'target_seq_decoy_var']
stem_file_df_09 = stem_file_df_09[stem_file_df_09['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_09.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_09.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_09.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: wild type_03'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 10
stem_file_df_10 = pd.read_csv('Decoy Variant Stem Cell File 10.csv', header=0)
stem_file_df_10 = stem_file_df_10[stem_file_df_10['pep_scores'] <= 1.0]
# stem_file_df_10 = stem_file_df_10[stem_file_df_10['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_10 = stem_file_df_10[stem_file_df_10['psm_type'] != 'target_seq_decoy_var']
stem_file_df_10 = stem_file_df_10[stem_file_df_10['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_10.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_10.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_10.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: mutant_01'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 11
stem_file_df_11 = pd.read_csv('Decoy Variant Stem Cell File 11.csv', header=0)
stem_file_df_11 = stem_file_df_11[stem_file_df_11['pep_scores'] <= 1.0]
# stem_file_df_11 = stem_file_df_11[stem_file_df_11['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_11 = stem_file_df_11[stem_file_df_11['psm_type'] != 'target_seq_decoy_var']
stem_file_df_11 = stem_file_df_11[stem_file_df_11['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_11.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_11.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_11.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: mutant_02'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

# STEM FILE 12
stem_file_df_12 = pd.read_csv('Decoy Variant Stem Cell File 12.csv', header=0)
stem_file_df_12 = stem_file_df_12[stem_file_df_12['pep_scores'] <= 1.0]
# stem_file_df_12 = stem_file_df_12[stem_file_df_12['Probability P(-1)'] < 0.5]

# remove decoys of canonical and variants
stem_file_df_12 = stem_file_df_12[stem_file_df_12['psm_type'] != 'target_seq_decoy_var']
stem_file_df_12 = stem_file_df_12[stem_file_df_12['psm_type'] != 'decoy_seq']

# separate matching gene names if there are multiple entries and make each gene into its own row with duplicate info
# reset index for PSMIs and make new column names (avoid redundancy later)
separated_gene_ids_df = pd.DataFrame(stem_file_df_12.matching_gene_names.str.split(';').tolist(),
                                     index=stem_file_df_12.PSMId).stack()
separated_gene_ids_df = separated_gene_ids_df.reset_index([0, 'PSMId'])
separated_gene_ids_df.columns = ["PSMId", "gene_id"]

# merge with stem file to include confusion matrix info, merge on PSMId
merged_stem = stem_file_df_12.merge(separated_gene_ids_df, on='PSMId', how='left')

# create new df with pep scores only and remove duplicate gene identifiers for now ***
filter_for_pep_only = merged_stem[['gene_id', 'pep_scores']].copy()
filter_for_pep_only = filter_for_pep_only.drop_duplicates(subset=['gene_id'])
filter_for_pep_only = filter_for_pep_only.rename(columns={'pep_scores': 'Stage 4: mutant_03'})
append_filtered_genes_to_MODY = filter_for_pep_only[filter_for_pep_only['gene_id'].isin(MODY_list)]
append_filtered_genes_to_MODY = append_filtered_genes_to_MODY.set_index("gene_id")

# merge with MODY df
MODY_df = MODY_df.join(append_filtered_genes_to_MODY)

plt.figure(figsize=(13, 20))
plt.rc('axes', axisbelow=True)
plt.scatter(x=MODY_df['Stage 0: wild type_01'], y=MODY_df.index, c='orange', s=90)
plt.scatter(x=MODY_df['Stage 0: wild type_02'], y=MODY_df.index, c='orange', s=90)
plt.scatter(x=MODY_df['Stage 0: wild type_03'], y=MODY_df.index, c='orange', s=90)
plt.scatter(x=MODY_df['Stage 0: Mutant_01'], y=MODY_df.index, c='olivedrab', s=90)
plt.scatter(x=MODY_df['Stage 0: Mutant_02'], y=MODY_df.index, c='olivedrab', s=90)
plt.scatter(x=MODY_df['Stage 0: Mutant_03'], y=MODY_df.index, c='olivedrab', s=90)
plt.scatter(x=MODY_df['Stage 4: wild type_01'], y=MODY_df.index, c='turquoise', s=50)
plt.scatter(x=MODY_df['Stage 4: wild type_02'], y=MODY_df.index, c='turquoise', s=50)
plt.scatter(x=MODY_df['Stage 4: wild type_03'], y=MODY_df.index, c='turquoise', s=50)
plt.scatter(x=MODY_df['Stage 4: mutant_01'], y=MODY_df.index, c='violet', s=30)
plt.scatter(x=MODY_df['Stage 4: mutant_02'], y=MODY_df.index, c='violet', s=30)
plt.scatter(x=MODY_df['Stage 4: mutant_03'], y=MODY_df.index, c='violet', s=30)

plt.margins(y=0.05)

plt.grid(axis='y', color='gainsboro', linewidth=0.7)
plt.xlim(-0.02, 0.5)
plt.xticks(np.arange(0, 0.5, step=0.1))
plt.xlabel('posterior error probability score', labelpad=7)
plt.ylabel('MODY proteins')

# plt.title('MODY gene expression in iPSCs')
plt.legend(MODY_df.columns, bbox_to_anchor=(1, 1), loc='upper left', title='iPSCs growth stage and type')
plt.savefig('iPSCs MODY plus interacting proteins pep distribution decoy variant search.png', bbox_inches='tight', dpi=600)
plt.show()
