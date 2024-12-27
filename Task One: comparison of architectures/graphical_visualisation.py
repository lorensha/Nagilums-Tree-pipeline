from Calculations import *
from plots_and_figures import *

# setup all csv files of each architecture
# round p(-1) and FDR to 3 for better resolution/graphical visualisation
# add names of architecture to title each plot produced
extra_trees_df = pd.read_csv('confusion matrix extra trees.csv', header=0)
extra_trees_df['Probability P(-1)'] = extra_trees_df['Probability P(-1)'].round(3)
extra_trees_df['FDR'] = extra_trees_df['FDR'].round(3)
extra_trees_df.index.name = 'Extra Trees'

gradient_boosting_df = pd.read_csv('confusion matrix gradient boosting.csv', header=0)
gradient_boosting_df['Probability P(-1)'] = gradient_boosting_df['Probability P(-1)'].round(3)
gradient_boosting_df['FDR'] = gradient_boosting_df['FDR'].round(3)
gradient_boosting_df.index.name = 'Gradient Boosting'

histogram_gb_df = pd.read_csv('confusion matrix histogram gb.csv', header=0)
histogram_gb_df['Probability P(-1)'] = histogram_gb_df['Probability P(-1)'].round(3)
histogram_gb_df['FDR'] = histogram_gb_df['FDR'].round(3)
histogram_gb_df.index.name = 'Histogram Gradient Boosting'

random_forest_df = pd.read_csv('confusion matrix random forest.csv', header=0)
random_forest_df['Probability P(-1)'] = random_forest_df['Probability P(-1)'].round(3)
random_forest_df['FDR'] = random_forest_df['FDR'].round(3)
random_forest_df.index.name = 'Random Forest'

xgboost_df = pd.read_csv('confusion matrix xgboost.csv', header=0)
xgboost_df['Probability P(-1)'] = xgboost_df['Probability P(-1)'].round(3)
xgboost_df['FDR'] = xgboost_df['FDR'].round(3)
xgboost_df.index.name = 'XGBoost'

df_list = [extra_trees_df, gradient_boosting_df, random_forest_df, xgboost_df, histogram_gb_df]
cumulative_count_non_random_spectra_fdr_01(df_list)
cumulative_count_below_01(df_list)
cumulative_count_above_p_05(df_list)    # supplementary plot*
cumulative_count_below_p_05(df_list)
task_one_histogram_plots(df_list)
task_one_AUROC_curve(df_list)
task_one_precision_recall_curve(df_list)
