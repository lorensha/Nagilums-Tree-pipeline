import matplotlib.pyplot as plt
import numpy as np


def task_two_histogram_plots(decoy_sequence_df, decoy_variant_df):
    # histograms are setup for 100 bins, to set for 10 bins: bins=np.arrange(0, 1.01, step=0.01)

    df_title = str(decoy_sequence_df.index.name)
    fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
    fig.suptitle(df_title, y=0.95)
    fig.tight_layout(pad=2.5)

    # setup for decoy sequence histogram
    canonical_psm = decoy_sequence_df[decoy_sequence_df['psm_type'] == 'canonical']
    decoy_psm = decoy_sequence_df[decoy_sequence_df['psm_type'] == 'decoy_seq']
    variant_psm = decoy_sequence_df[decoy_sequence_df['psm_type'] == 'target_seq_target_var']

    plt1.hist([canonical_psm['Probability P(-1)'], decoy_psm['Probability P(-1)'], variant_psm['Probability P(-1)']],
              edgecolor='black', bins=np.arange(0, 1.01, step=0.01), color=['lightsteelblue', 'coral', 'limegreen'],
              ec='none')

    plt1.set_title('decoy sequence search', loc='center')
    plt1.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
    plt1.set_ylabel('Number of spectra', labelpad=15.0)
    plt1.set_xticks(np.arange(0, 1.01, step=0.1))
    plt1.set_ylim(0, 1000)

    # setup for decoy variant histogram
    canonical_psm = decoy_variant_df[decoy_variant_df['psm_type'] == 'canonical']
    decoy_psm = decoy_variant_df[decoy_variant_df['psm_type'] == 'target_seq_decoy_var']
    variant_psm = decoy_variant_df[decoy_variant_df['psm_type'] == 'target_seq_target_var']

    plt2.hist([canonical_psm['Probability P(-1)'], decoy_psm['Probability P(-1)'], variant_psm['Probability P(-1)']],
              edgecolor='black', bins=np.arange(0, 1.01, step=0.01), color=['lightsteelblue', 'coral', 'limegreen'],
              ec='none')

    plt2.set_title('decoy variant search', loc='center')
    plt2.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
    plt2.set_xticks(np.arange(0, 1.01, step=0.1))

    fig.legend(["canonical PSMs", "decoy PSMs", 'variant PSM'], bbox_to_anchor=(0.965, 0.878), loc='upper left')

    plt.savefig(df_title + '.png', bbox_inches='tight', dpi=600)
    plt.show()


# histogram for tonsil file as reference. Not in thesis results. Setup for future works
def task_two_histogram_tonsil_file(decoy_sequence_tonsil_df, decoy_variant_tonsil_df):

    df_title = str(decoy_sequence_tonsil_df.index.name)
    fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
    fig.suptitle(df_title, y=0.95)
    fig.tight_layout(pad=2.5)

    # setup for decoy sequence histogram
    canonical_psm = decoy_sequence_tonsil_df[decoy_sequence_tonsil_df['psm_type'] == 'canonical']
    decoy_psm = decoy_sequence_tonsil_df[decoy_sequence_tonsil_df['psm_type'] == 'decoy_seq']
    variant_psm = decoy_sequence_tonsil_df[decoy_sequence_tonsil_df['psm_type'] == 'target_seq_target_var']

    plt1.hist([canonical_psm['Probability P(-1)'], decoy_psm['Probability P(-1)'], variant_psm['Probability P(-1)']],
              edgecolor='black', bins=np.arange(0, 1.1, step=0.01), color=['lightsteelblue', 'coral', 'limegreen'],
              ec='none')

    plt1.set_title('decoy sequence search', loc='center')
    plt1.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
    plt1.set_ylabel('Number of spectra', labelpad=15.0)
    plt1.set_xticks(np.arange(0, 1.1, step=0.1))
    plt1.set_ylim(0, 5000)

    # setup for decoy variant histogram
    canonical_psm = decoy_variant_tonsil_df[decoy_variant_tonsil_df['psm_type'] == 'canonical']
    decoy_psm = decoy_variant_tonsil_df[decoy_variant_tonsil_df['psm_type'] == 'target_seq_decoy_var']
    variant_psm = decoy_variant_tonsil_df[decoy_variant_tonsil_df['psm_type'] == 'target_seq_target_var']

    plt2.hist([canonical_psm['Probability P(-1)'], decoy_psm['Probability P(-1)'], variant_psm['Probability P(-1)']],
              edgecolor='black', bins=np.arange(0, 1.1, step=0.01), color=['lightsteelblue', 'coral', 'limegreen'],
              ec='none')

    plt2.set_title('decoy variant search', loc='center')
    plt2.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
    plt2.set_xticks(np.arange(0, 1.1, step=0.1))

    fig.legend(["canonical PSMs", "decoy PSMs", 'variant PSM'], bbox_to_anchor=(0.965, 0.878), loc='upper left')

    plt.savefig(df_title + '.png', bbox_inches='tight', dpi=600)
    plt.show()


def cumulative_count_pep_scores_of_canonical_psms(decoy_seq_dataframe_list, decoy_variant_dataframe_list):

    df_title_list = []
    decoy_seq_canonical_count_list = []
    decoy_variant_canonical_count_list = []

    for df in decoy_seq_dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        canonical = df[df['psm_type'] == 'canonical']
        decoy_seq_canonical_count = canonical[canonical['pep_scores'] <= 0.5]
        decoy_seq_canonical_count = (
            decoy_seq_canonical_count[decoy_seq_canonical_count['Probability P(-1)'] <= 0.5].shape)[0]
        decoy_seq_canonical_count_list.append(decoy_seq_canonical_count)

    for df in decoy_variant_dataframe_list:

        canonical = df[df['psm_type'] == 'canonical']
        decoy_variant_canonical_count = canonical[canonical['pep_scores'] <= 0.5]
        decoy_variant_canonical_count =\
            decoy_variant_canonical_count[decoy_variant_canonical_count['Probability P(-1)'] <= 0.5].shape[0]
        decoy_variant_canonical_count_list.append(decoy_variant_canonical_count)

    df_title_list_x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list_x_axis - 0.2, decoy_seq_canonical_count_list, 0.4, color='lightsteelblue', label='canonical PSM')
    plt.bar(df_title_list_x_axis + 0.2, decoy_variant_canonical_count_list, 0.4, color='thistle', label='variant PSM')

    plt.legend(['decoy sequence search', 'decoy variant search'], bbox_to_anchor=(1, 1), title='Search strategy')

    plt.xticks(df_title_list_x_axis, df_title_list, rotation=45, ha='right')
    plt.xlabel('iPSC development stage and type', labelpad=15.0, fontweight='bold')
    plt.ylabel('Number of spectra', labelpad=15.0, fontweight='bold')
    plt.title('comparison of search strategies: number of classified canonical PSMs')

    plt.savefig('cumulative count canonical PSM.png', bbox_inches='tight', dpi=600, pad_inches=0.1)
    plt.show()


def cumulative_count_pep_scores_of_variant_psms(decoy_seq_dataframe_list, decoy_variant_dataframe_list):

    df_title_list = []
    decoy_seq_variant_count_list = []
    decoy_variant_true_variant_count_list = []

    for df in decoy_seq_dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        variant_psms = df[df['psm_type'] == 'target_seq_target_var']
        decoy_seq_canonical_count = variant_psms[variant_psms['pep_scores'] < 0.5]
        decoy_seq_canonical_count = \
            decoy_seq_canonical_count[decoy_seq_canonical_count['Probability P(-1)'] < 0.5].shape[0]
        decoy_seq_variant_count_list.append(decoy_seq_canonical_count)

    for df in decoy_variant_dataframe_list:

        variant_psms = df[df['psm_type'] == 'target_seq_target_var']
        decoy_variant_canonical_count = variant_psms[variant_psms['pep_scores'] < 0.5]
        decoy_variant_canonical_count = \
            decoy_variant_canonical_count[decoy_variant_canonical_count['Probability P(-1)'] < 0.5].shape[0]
        decoy_variant_true_variant_count_list.append(decoy_variant_canonical_count)

    df_title_list_x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list_x_axis - 0.2, decoy_seq_variant_count_list, 0.4, color='mediumseagreen')
    plt.bar(df_title_list_x_axis + 0.2, decoy_variant_true_variant_count_list, 0.4, color='yellowgreen')

    plt.legend(['decoy sequence search', 'decoy variant search'], bbox_to_anchor=(1, 1), title='Search strategy')

    plt.xticks(df_title_list_x_axis, df_title_list, rotation=45, ha='right')
    plt.xlabel('iPSC development stage and type', labelpad=15.0, fontweight='bold')
    plt.ylabel('Number of spectra', labelpad=15.0, fontweight='bold')
    plt.title('comparison of search strategies: number of classified variant PSMs')

    plt.savefig('cumulative count variant PSM.png', bbox_inches='tight', dpi=600, pad_inches=0.1)
    plt.show()


def PEP_probability_plot_decoy_sequence(dataframe_list):
    file_names = []
    for df in dataframe_list:
        df = df.sort_values(by=['Probability P(-1)'])
        df = df[df['Actual'] == 1]

        df_title = str(df.index.name)
        file_names.append(df_title)

        plt.plot(df['Probability P(-1)'], df['pep_scores'])
        plt.xlabel('prediction probability $p(-1)$')
        plt.ylabel('posterior error probability score')
        plt.title('PEP distribution of processed iPSCs: decoy sequence')
        plt.ylim([0, 2])
    plt.legend(file_names, bbox_to_anchor=(1, 1), title='iPSC stage and type')
    plt.xticks(np.arange(0, 1.1, step=0.1))
    plt.axvline(0.5, color='grey', lw=1, linestyle='--', alpha=0.7)
    plt.axhline(1.0, color='grey', lw=1, linestyle='--', alpha=0.7)
    plt.axhline(0.5, color='olive', lw=1, linestyle='--', alpha=0.7)
    plt.savefig('pep plot decoy sequence search.png', bbox_inches='tight', dpi=600)
    plt.show()


def PEP_probability_plot_decoy_variant_search(dataframe_list):
    file_names = []
    for df in dataframe_list:
        df = df.sort_values(by=['Probability P(-1)'])
        df = df[df['Actual'] == 1]

        df_title = str(df.index.name)
        file_names.append(df_title)

        plt.plot(df['Probability P(-1)'], df['pep_scores'])
        plt.xlabel('prediction probability $p(-1)$')
        plt.ylabel('posterior error probability score')
        plt.title('PEP distribution of processed iPSCs files: decoy sequence')
        plt.ylim([0, 2.0])
    plt.legend(file_names, bbox_to_anchor=(1, 1), title='iPSC stage and type')
    plt.xticks(np.arange(0, 1.1, step=0.1))
    plt.axvline(0.5, color='grey', lw=1, linestyle='--', alpha=0.7)
    plt.axhline(1.0, color='grey', lw=1, linestyle='--', alpha=0.7)
    plt.axhline(0.5, color='olive', lw=1, linestyle='--', alpha=0.7)
    plt.savefig('pep plot decoy variant search.png', bbox_inches='tight', dpi=600)
    plt.show()
