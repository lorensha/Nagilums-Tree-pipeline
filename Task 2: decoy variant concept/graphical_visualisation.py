import pandas as pd
from plots_and_figures import *

# import all processed iPSC files and title with stage number and cell type
# <processed iPSCs from decoy sequence search strategy>
# files 1 - 6: Stage 0, files 1 - 3: wild type, files: 4 - 6: mutant
decoy_seq_stem_file_01 = pd.read_csv('Decoy Seq Stem Cell File 1.csv', header=0)
decoy_seq_stem_file_01.index.name = 'Stage 0: wild type 01'
decoy_seq_stem_file_02 = pd.read_csv('Decoy Seq Stem Cell File 2.csv', header=0)
decoy_seq_stem_file_02.index.name = 'Stage 0: wild type 02'
decoy_seq_stem_file_03 = pd.read_csv('Decoy Seq Stem Cell File 3.csv', header=0)
decoy_seq_stem_file_03.index.name = 'Stage 0: wild type 03'

decoy_seq_stem_file_04 = pd.read_csv('Decoy Seq Stem Cell File 4.csv', header=0)
decoy_seq_stem_file_04.index.name = 'Stage 0: mutant 01'
decoy_seq_stem_file_05 = pd.read_csv('Decoy Seq Stem Cell File 5.csv', header=0)
decoy_seq_stem_file_05.index.name = 'Stage 0: mutant 02'
decoy_seq_stem_file_06 = pd.read_csv('Decoy Seq Stem Cell File 6.csv', header=0)
decoy_seq_stem_file_06.index.name = 'Stage 0: mutant 03'

decoy_seq_stem_file_07 = pd.read_csv('Decoy Seq Stem Cell File 7.csv', header=0)
decoy_seq_stem_file_07.index.name = 'Stage 4: wild type 01'
decoy_seq_stem_file_08 = pd.read_csv('Decoy Seq Stem Cell File 8.csv', header=0)
decoy_seq_stem_file_08.index.name = 'Stage 4: wild type 02'
decoy_seq_stem_file_09 = pd.read_csv('Decoy Seq Stem Cell File 9.csv', header=0)
decoy_seq_stem_file_09.index.name = 'Stage 4: wild type 03'

decoy_seq_stem_file_10 = pd.read_csv('Decoy Seq Stem Cell File 10.csv', header=0)
decoy_seq_stem_file_10.index.name = 'Stage 4: mutant 01'
decoy_seq_stem_file_11 = pd.read_csv('Decoy Seq Stem Cell File 11.csv', header=0)
decoy_seq_stem_file_11.index.name = 'Stage 4: mutant 02'
decoy_seq_stem_file_12 = pd.read_csv('Decoy Seq Stem Cell File 12.csv', header=0)
decoy_seq_stem_file_12.index.name = 'Stage 4: mutant 03'

# <iPSCs from decoy variant search strategy>
# files 1 - 6: Stage 0, files 1 - 3: wild type, files: 4 - 6: mutant
decoy_variant_stem_file_01 = pd.read_csv('Decoy Variant Stem Cell File 1.csv', header=0)
decoy_variant_stem_file_01.index.name = 'Stage 0: wild type 01'
decoy_variant_stem_file_02 = pd.read_csv('Decoy Variant Stem Cell File 2.csv', header=0)
decoy_variant_stem_file_02.index.name = 'Stage 0: wild type 02'
decoy_variant_stem_file_03 = pd.read_csv('Decoy Variant Stem Cell File 3.csv', header=0)
decoy_variant_stem_file_03.index.name = 'Stage 0: wild type 03'

decoy_variant_stem_file_04 = pd.read_csv('Decoy Variant Stem Cell File 4.csv', header=0)
decoy_variant_stem_file_04.index.name = 'Stage 0: Mutant 01'
decoy_variant_stem_file_05 = pd.read_csv('Decoy Variant Stem Cell File 5.csv', header=0)
decoy_variant_stem_file_05.index.name = 'Stage 0: Mutant 02'
decoy_variant_stem_file_06 = pd.read_csv('Decoy Variant Stem Cell File 6.csv', header=0)
decoy_variant_stem_file_06.index.name = 'Stage 0: Mutant 03'

decoy_variant_stem_file_07 = pd.read_csv('Decoy Variant Stem Cell File 7.csv', header=0)
decoy_variant_stem_file_07.index.name = 'Stage 4: wild type 01'
decoy_variant_stem_file_08 = pd.read_csv('Decoy Variant Stem Cell File 8.csv', header=0)
decoy_variant_stem_file_08.index.name = 'Stage 4: wild type 02'
decoy_variant_stem_file_09 = pd.read_csv('Decoy Variant Stem Cell File 9.csv', header=0)
decoy_variant_stem_file_09.index.name = 'Stage 4: wild type 03'

decoy_variant_stem_file_10 = pd.read_csv('Decoy Variant Stem Cell File 10.csv', header=0)
decoy_variant_stem_file_10.index.name = 'Stage 4: Mutant 01'
decoy_variant_stem_file_11 = pd.read_csv('Decoy Variant Stem Cell File 11.csv', header=0)
decoy_variant_stem_file_11.index.name = 'Stage 4: Mutant 02'
decoy_variant_stem_file_12 = pd.read_csv('Decoy Variant Stem Cell File 12.csv', header=0)
decoy_variant_stem_file_12.index.name = 'Stage 4: Mutant 03'

# setup tuple of decoy sequence and decoy variant iPSCs for histogram plots
iPSC_processed_files = [(decoy_seq_stem_file_01, decoy_variant_stem_file_01),
                        (decoy_seq_stem_file_02, decoy_variant_stem_file_02),
                        (decoy_seq_stem_file_03, decoy_variant_stem_file_03),
                        (decoy_seq_stem_file_04, decoy_variant_stem_file_04),
                        (decoy_seq_stem_file_05, decoy_variant_stem_file_05),
                        (decoy_seq_stem_file_06, decoy_variant_stem_file_06),
                        (decoy_seq_stem_file_07, decoy_variant_stem_file_07),
                        (decoy_seq_stem_file_08, decoy_variant_stem_file_08),
                        (decoy_seq_stem_file_09, decoy_variant_stem_file_09),
                        (decoy_seq_stem_file_10, decoy_variant_stem_file_10),
                        (decoy_seq_stem_file_11, decoy_variant_stem_file_11),
                        (decoy_seq_stem_file_12, decoy_variant_stem_file_12)]
# generate histograms
# for file in iPSC_processed_files:
#     decoy_sequence_file = file[0]
#     decoy_variant_file = file[1]
#     task_two_histogram_plots(decoy_sequence_file, decoy_variant_file)

# setup for cumulative count and pep plots
decoy_seq_stem_file_list = [decoy_seq_stem_file_01, decoy_seq_stem_file_02, decoy_seq_stem_file_03,
                            decoy_seq_stem_file_04, decoy_seq_stem_file_05, decoy_seq_stem_file_06,
                            decoy_seq_stem_file_07, decoy_seq_stem_file_08, decoy_seq_stem_file_09,
                            decoy_seq_stem_file_10, decoy_seq_stem_file_11, decoy_seq_stem_file_12]

decoy_variant_stem_file_list = [decoy_variant_stem_file_01, decoy_variant_stem_file_02, decoy_variant_stem_file_03,
                                decoy_variant_stem_file_04, decoy_variant_stem_file_05, decoy_variant_stem_file_06,
                                decoy_variant_stem_file_07, decoy_variant_stem_file_08, decoy_variant_stem_file_09,
                                decoy_variant_stem_file_10, decoy_variant_stem_file_11, decoy_variant_stem_file_12]

cumulative_count_pep_scores_of_canonical_psms(decoy_seq_stem_file_list, decoy_variant_stem_file_list)
cumulative_count_pep_scores_of_variant_psms(decoy_seq_stem_file_list, decoy_variant_stem_file_list)
PEP_probability_plot_decoy_sequence(decoy_seq_stem_file_list)
PEP_probability_plot_decoy_variant_search(decoy_variant_stem_file_list)

# setup for tonsil file as reference. Not used in thesis results. Setup for future works
decoy_seq_tonsil = pd.read_csv('Decoy Seq Tonsil File.csv', header=0)
decoy_seq_tonsil.index.name = 'Tonsil file'

decoy_variant_tonsil = pd.read_csv('Decoy Variant Tonsil file.csv', header=0)
decoy_variant_tonsil.index.name = 'Tonsil file'

task_two_histogram_tonsil_file(decoy_seq_tonsil, decoy_variant_tonsil)