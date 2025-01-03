import matplotlib.pyplot as plt
from sklearn import metrics
from matplotlib.pyplot import *


def task_one_histogram_plots(dataframe_list):

    for df in dataframe_list:
        df_title = str(df.index.name)
        fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
        fig.suptitle(df_title, y=0.95)
        fig.tight_layout(pad=2.5)

        # setup is for 100 bins, to adjust to 10 bins: bins=np.arrange(0, 1.01, step=0.1)
        target_psms = df[df['Label'] == 1]
        decoy_psms = df[df['Label'] == -1]
        plt1.hist([target_psms['Probability P(-1)'], decoy_psms['Probability P(-1)']], edgecolor='black',
                  bins=np.arange(0, 1.01, step=0.01), color=['cornflowerblue', 'coral'], ec='none')

        plt1.set_title('prediction probability $p(-1)$: 0.0 - 1.0', loc='center')
        plt1.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
        plt1.set_ylabel('Number of spectra', labelpad=15.0)
        plt1.set_xticks(np.arange(0, 1.01, step=0.1))

        dataframe_close_up = df[df['Probability P(-1)'] <= 0.1]
        target_psms = dataframe_close_up[dataframe_close_up['Label'] == 1]
        decoy_psms = dataframe_close_up[dataframe_close_up['Label'] == -1]

        plt2.hist([target_psms['Probability P(-1)'], decoy_psms['Probability P(-1)']], edgecolor='black',
                  bins=np.arange(0, 0.101, step=0.001), color=['cornflowerblue', 'coral'], ec='none')

        plt2.set_title('prediction probability ' + r'$p(-1) \leq 0.1$', loc='center')
        plt2.set_xlabel('prediction probability $p(-1)$', labelpad=15.0)
        plt2.set_xticks(np.arange(0, 0.11, step=0.01))

        fig.legend(["non-random", "random"], bbox_to_anchor=(0.965, 0.878), loc='upper left', title='PSM class type')

        plt.savefig(df_title + ' histograms.png', bbox_inches='tight', dpi=600)
        plt.show()


def task_one_AUROC_curve(dataframe):
    auc_scores_list = []
    df_titles_list = []

    fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
    fig.suptitle('AUROC curve: comparison of ensemble architectures', y=1.005)
    fig.subplots_adjust(top=10)
    fig.tight_layout(pad=1.0)

    colours = ['indianred', 'royalblue', 'mediumblue', 'sandybrown', 'forestgreen']
    lines = ['solid', 'dashed', 'dashdot', 'solid', 'dotted']

    for line_type, line_colour, df in zip(lines, colours, dataframe):
        df = df[df['Label'] == 1]
        df_titles_list.append(str(df.index.name))
        auc_score = metrics.auc(df['1 - Specificity'], df['Sensitivity'])
        auc_scores_list.append(auc_score)
        plt1.plot(df['1 - Specificity'], df['Sensitivity'], color=line_colour, alpha=0.5, linestyle=line_type)

    plt1.plot([0, 1], [0, 1], color="black", lw=2, linestyle="--")
    plt1.set_title('prediction probability $p(-1)$: 0.0 - 1.0')
    plt1.set_ylabel('sensitivity ' + r'$\left(\frac{TP} {TP + FN}\right)$', labelpad=15.0)
    plt1.set_xlabel('1 - specificity ' + r'$\left(\frac{FP} {FP + TN}\right)$', labelpad=15.0)

    for line_type, line_colour, df in zip(lines, colours, dataframe):
        df = df[df['Label'] == 1]

        df = df[df['Probability P(-1)'] <= 0.1]
        plt2.plot(df['1 - Specificity'], df['Sensitivity'], color=line_colour, alpha=0.5, linestyle=line_type)

    plt2.set_title('prediction probability ' + r'$p(-1) \leq 0.1$')
    plt2.set_xlabel('1 - specificity ' + r'$\left(\frac{FP} {FP + TN}\right)$', labelpad=15.0)

    dict_auc = ['%.2f' % score for score in auc_scores_list]

    plot_legend_classifier_name = fig.legend(df_titles_list, bbox_to_anchor=[0.98, 0.93], title='Architecture',
                                             loc='upper left', prop={'size': 8})
    plot_legend_auc_score = fig.legend(dict_auc, title='AUC score', handlelength=0, handletextpad=0, ncol=1,
                                       bbox_to_anchor=[1.137, 0.93], loc='upper left', prop={'size': 8})
    gca().add_artist(plot_legend_classifier_name)
    gca().add_artist(plot_legend_auc_score)

    plt.savefig('AUROC curve.png', bbox_inches='tight', dpi=600)
    # plt.show()

    return plt.show()


def task_one_precision_recall_curve(dataframe):

    df_titles_list = []
    colours = ['indianred', 'royalblue', 'mediumblue', 'sandybrown', 'forestgreen']
    lines = ['solid', 'dashed', 'dashdot', 'solid', 'dotted']

    fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, figsize=(13, 7), sharey=True)
    fig.suptitle('Precision Recall curve: comparison of ensemble architectures', y=1.005)
    fig.tight_layout(pad=1.0)

    for line_type, line_color, df in zip(lines, colours, dataframe):
        df_titles_list.append(str(df.index.name))
        plt1.plot(df['Recall'], df['Precision'], alpha=0.5, color=line_color, linestyle=line_type)

    plt1.set_title('prediction probability $p(-1)$: 0.0 - 1.0')
    plt1.set_ylabel('Precision ' + r'$\left(\frac{TP} {TP + FP}\right)$', labelpad=15.0)
    plt1.set_xlabel('Recall ' + r'$\left(\frac{TP} {TP + FN}\right)$', labelpad=15.0)

    for line_type, line_color, df in zip(lines, colours, dataframe):

        df = df[df['Probability P(-1)'] <= 0.1]
        plt2.plot(df['Recall'], df['Precision'], linestyle=line_type, alpha=0.5, color=line_color)

    plt2.set_title('prediction probability ' + r'$p(-1) \leq 0.1$')
    plt2.set_xlabel('Recall ' + r'$\left(\frac{TP} {TP + FN}\right)$', labelpad=15.0)

    plot_legend_classifier_name = fig.legend(df_titles_list, bbox_to_anchor=[0.98, 0.93], title='Architecture',
                                             loc='upper left', prop={'size': 8})

    gca().add_artist(plot_legend_classifier_name)

    plt.savefig('Precision Recall curve.png', bbox_inches='tight', dpi=600)

    return plt.show()


def cumulative_count_below_01(dataframe_list):

    df_title_list = []
    targets_count_list = []
    decoys_count_list = []

    for df in dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        targets = df[df['Label'] == 1]
        decoys = df[df['Label'] == -1]

        target_psms = targets[targets['Probability P(-1)'] < 0.1].shape[0]
        targets_count_list.append(target_psms)

        decoy_psms = decoys[decoys['Probability P(-1)'] < 0.1].shape[0]
        decoys_count_list.append(decoy_psms)

    x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list, targets_count_list, 0.4, color='lightsteelblue')
    plt.bar(df_title_list, decoys_count_list, 0.4, color='coral')
    plt.legend(['non-random', 'random'], bbox_to_anchor=(1, 1), title='PSM class type')

    plt.xticks(x_axis, df_title_list)
    plt.xlabel('Architecture', fontweight='bold', labelpad=15.0)
    plt.ylabel('Number of spectra', fontweight='bold', labelpad=15.0)
    plt.title('Cumulative count of decision-tree architectures: ' + r'$p(-1) < 0.1$')

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center', bbox=dict(facecolor='white', alpha=.8))

    addlabels(df_title_list, targets_count_list)
    addlabels(df_title_list, decoys_count_list)

    plt.savefig('target and decoy cumulative count p(-1) < 0.1.png', bbox_inches='tight', dpi=600, pad_inches=0.1)
    plt.show()


def cumulative_count_below_p_05(dataframe_list):

    df_title_list = []
    targets_count_list = []
    decoys_count_list = []

    for df in dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        targets = df[df['Label'] == 1]
        decoys = df[df['Label'] == -1]

        target_psms = targets[targets['Probability P(-1)'] < 0.5].shape[0]
        targets_count_list.append(target_psms)

        decoy_psms = decoys[decoys['Probability P(-1)'] < 0.5].shape[0]
        decoys_count_list.append(decoy_psms)

    x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list, targets_count_list, 0.4, color='lightsteelblue')
    plt.bar(df_title_list, decoys_count_list, 0.4, color='coral')
    plt.legend(['non-random', 'random'], bbox_to_anchor=(1, 1), loc="upper left", title='PSM class type')

    plt.xticks(x_axis, df_title_list)
    plt.xlabel('Architecture', fontweight='bold', labelpad=15.0)
    plt.ylabel('Number of spectra', fontweight='bold', labelpad=15.0)
    plt.title('cumulative count of decision-tree architectures: ' + r'$p(-1) < 0.5$')

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center', bbox=dict(facecolor='white', alpha=.8))

    addlabels(df_title_list, targets_count_list)
    addlabels(df_title_list, decoys_count_list)

    plt.savefig('target and decoy cumulative count p(-1) < 05.png', bbox_inches='tight', dpi=600)
    plt.show()


def cumulative_count_above_p_05(dataframe_list):

    df_title_list = []
    targets_count_list = []
    decoys_count_list = []

    for df in dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        targets = df[df['Label'] == 1]
        decoys = df[df['Label'] == -1]

        target_psms = targets[targets['Probability P(-1)'] >= 0.5].shape[0]
        targets_count_list.append(target_psms)

        decoy_psms = decoys[decoys['Probability P(-1)'] >= 0.5].shape[0]
        decoys_count_list.append(decoy_psms)

    x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list, targets_count_list, 0.4, color='lightsteelblue')
    plt.bar(df_title_list, decoys_count_list, 0.4, color='coral')
    plt.legend(['non-random', 'random'], bbox_to_anchor=(1, 1), loc="upper left", title='PSM class type')

    plt.xticks(x_axis, df_title_list)
    plt.xlabel('Architecture', fontweight='bold', labelpad=15.0)
    plt.ylabel('Number of spectra', fontweight='bold', labelpad=15.0)
    plt.title('cumulative count of decision-tree classifiers: ' + r'$p(-1) \geq 0.5$')

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center', bbox=dict(facecolor='white', alpha=.8))

    addlabels(df_title_list, targets_count_list)
    addlabels(df_title_list, decoys_count_list)

    plt.savefig('target and decoy cumulative count p(-1) > 05.png', bbox_inches='tight', dpi=600)
    plt.show()


def cumulative_count_non_random_spectra_fdr_01(dataframe_list):

    df_title_list = []
    spectra_below_p_05_count_list = []
    spectra_below_p_01_count_list = []
    redundant_psms_count_list = []

    for df in dataframe_list:
        df_title = str(df.index.name)
        df_title_list.append(df_title)

        target_psms = df[df['Label'] == 1]

        fdr_01 = target_psms[target_psms['FDR'] <= 0.01]

        spectra_below_p_05 = fdr_01[fdr_01['Probability P(-1)'] < 0.5].shape[0]
        spectra_below_p_05_count_list.append(spectra_below_p_05)

        spectra_below_p_01 = fdr_01[fdr_01['Probability P(-1)'] < 0.1].shape[0]
        spectra_below_p_01_count_list.append(spectra_below_p_01)

        spectra_above_05 = fdr_01[fdr_01['Probability P(-1)'] >= 0.5].shape[0]
        redundant_psms_count_list.append(spectra_above_05)

    x_axis = np.arange(len(df_title_list))

    plt.figure(figsize=(13, 7))

    plt.bar(df_title_list, spectra_below_p_05_count_list, 0.4, color='lightsteelblue'),
    plt.bar(df_title_list, spectra_below_p_01_count_list, 0.4, color='cornflowerblue'),
    plt.bar(df_title_list, redundant_psms_count_list, 0.4, color='mediumblue')

    plt.legend([r'$p(-1) < 0.5$', r'$p(-1) < 0.1$', r'$p(-1) \geq 0.5$'], bbox_to_anchor=(1, 1), loc="upper left",
               title='intervals')

    plt.xticks(x_axis, df_title_list)
    plt.xlabel('Architecture', fontweight='bold', labelpad=15.0)
    plt.ylabel('Number of spectra', fontweight='bold', labelpad=15.0)
    plt.title('Cumulative count of non-random PSMs: 1% FDR')

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center', bbox=dict(facecolor='white', alpha=.8))

    addlabels(df_title_list, spectra_below_p_05_count_list)
    addlabels(df_title_list, spectra_below_p_01_count_list)
    addlabels(df_title_list, redundant_psms_count_list)

    plt.savefig('Target spectra with 1% FDR probability p(-1) distribution.png', bbox_inches='tight', dpi=600)
    plt.show()
