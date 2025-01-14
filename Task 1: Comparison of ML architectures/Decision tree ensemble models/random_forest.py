# import libraries and Python file: Calculations
import numpy as np
import time
import pandas as pd
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from Calculations import *

# PSM dataset: Tonsil pp (Wang et al)
psm_dataset = pd.read_table('Chapter_One_Tonsil_Input_File.txt', header=0)
start_time = time.time()

# Setup base estimator: Feature variable & class labels
feature_variables = ["measured_mz",
                     "mz_error",
                     "pep",
                     "delta_pep",
                     "ion_fraction",
                     "peptide_length",
                     "charge_2",
                     "charge_3",
                     "charge_4",
                     "isotope_0",
                     "isotope_1",
                     "isotope_2",
                     "isotope_3",
                     "isotope_4",
                     "unspecific",
                     "enzymatic_N",
                     "enzymatic_C",
                     "enzymatic"]

# stratification setup and selected feature variable
stratified_kfold_setup = StratifiedKFold(n_splits=3, random_state=1, shuffle=True)
selected_feature_variable = ['pep']


# function to extract most common variables after hyperparameter tuning
def grid_search_best_parameters(parameter_list):
    counter = 0
    best_parameters = parameter_list[0]

    for variables in parameter_list:
        frequent_parameters = parameter_list.count(variables)
        if frequent_parameters > counter:
            counter = frequent_parameters
            best_parameters = variables

    return best_parameters


# function of main predictor
def random_forest_main_predictor(psm_input_file):

    # create list variables for PSM selection and hyperparameter tuning
    best_scoring_psms_list = []
    hyperparameter_grid_search_list = []

    # select PSMs from dataset for a single feature variable
    psm_dataset_single_feature_variable_sample = psm_input_file[selected_feature_variable]
    psm_dataset_single_feature_labels_sample = np.array(psm_input_file['Label'])

    input_check_fdr = psm_input_file[psm_input_file['FDR'] <= 0.01]
    target_psms_within_fdr_threshold = input_check_fdr[input_check_fdr['Label'] == 1]

    # 3-fold cross-validation
    for fold_01, (train_index_01, test_index_01) in (
            enumerate(stratified_kfold_setup.split(psm_dataset_single_feature_variable_sample,
                                                   psm_dataset_single_feature_labels_sample))):
        # 2 folds for training
        training_folds = psm_input_file.iloc[train_index_01]
        # 1 fold for validation
        validation_fold = psm_input_file.iloc[test_index_01]

        # select target PSMs within 1% FDR threshold from training folds
        # select all decoy PSMs from input file
        # combine selected target and decoy PSMs for hyperparameter tuning
        psms_within_fdr_threshold = training_folds[training_folds['FDR'] <= 0.01]
        target_psms_within_fdr_threshold = psms_within_fdr_threshold[psms_within_fdr_threshold['Label'] == 1]
        decoy_psms = psm_input_file[psm_input_file['Label'] == -1]
        selected_target_and_decoy_psms_combined = pd.concat([target_psms_within_fdr_threshold, decoy_psms])

        # feature variables and labels of selected psms for nested cross-validation
        selected_psms_feature_variable = selected_target_and_decoy_psms_combined[selected_feature_variable]
        selected_psms_labels = selected_target_and_decoy_psms_combined['Label']

        # nested 3-fold cross-validation for hyperparameter search using psms of a single feature variable
        for fold_02, (train_index_02, test_index_02) in (
                enumerate(stratified_kfold_setup.split(selected_psms_feature_variable, selected_psms_labels))):

            # 2-folds for training
            nested_cross_validation_training_sample = training_folds.iloc[train_index_02]
            # 1-fold for validation *unneeded for further use as the outer layers are validated only
            nested_cross_validation_testing_sample = training_folds.iloc[test_index_02]

            nested_cross_validation_training_feature = (
                nested_cross_validation_training_sample)[selected_feature_variable]
            nested_cross_validation_training_labels = np.array(nested_cross_validation_training_sample['Label'])

            grid = {'max_depth': [3, 10], 'max_leaf_nodes': [10, 31], 'min_samples_leaf': [2, 10],
                    'max_features': [2, 5, 8]}

            random_forest_hyperparameter_search = (GridSearchCV(estimator=RandomForestClassifier(warm_start=False),
                                                                param_grid=grid))

            random_forest_hyperparameter_search.fit(nested_cross_validation_training_feature,
                                                    nested_cross_validation_training_labels)
            best_parameters_compiled = random_forest_hyperparameter_search.best_params_
            hyperparameter_grid_search_list.append(best_parameters_compiled)

        # select most common occurring parameters
        best_parameters = grid_search_best_parameters(hyperparameter_grid_search_list)

        # training model using selected PSMs of a single feature variable
        # validate model using validation fold PSMs of a single feature variable
        training_single_feature_variable_sample = selected_psms_feature_variable
        # training_single_feature_labels_sample = selected_psms_labels
        training_single_feature_labels_sample = np.array(selected_psms_labels)

        testing_single_feature_variable_sample = validation_fold[selected_feature_variable]
        testing_single_feature_labels_sample = np.array(validation_fold['Label'])

        # fit model and obtain PSM class type predictions and probability scores
        random_forest_cross_validation_model = RandomForestClassifier(warm_start=False, **best_parameters)
        random_forest_cross_validation_model.fit(training_single_feature_variable_sample,
                                                 training_single_feature_labels_sample)

        cross_validation_predictions = (random_forest_cross_validation_model.predict
                                        (testing_single_feature_variable_sample))
        cross_validation_probability_scores = (random_forest_cross_validation_model.predict_proba
                                               (testing_single_feature_variable_sample))
        cross_validation_probability_scores = cross_validation_probability_scores.round(6)

        # aggregate results into a dataframe for analysis
        cross_validation_complete_dataframe = pd.DataFrame({'Label': testing_single_feature_labels_sample,
                                                            'Predicted': cross_validation_predictions,
                                                            'Probability P(-1)':
                                                                cross_validation_probability_scores[:, 0]})

        # sort dataframe by prediction probability score in ascending order
        # calculate FDR and select psms with an 1% FDR threshold
        cross_validation_complete_dataframe = cross_validation_complete_dataframe.sort_values(by=['Probability P(-1)'])
        cross_validation_complete_dataframe = fdr_calculation(cross_validation_complete_dataframe)
        psms_within_fdr_threshold_cross_val = cross_validation_complete_dataframe[cross_validation_complete_dataframe
                                                                                  ['FDR'] <= 0.01]
        # add selected PSMs to the appropriate list
        best_scoring_psms_list.append(psms_within_fdr_threshold_cross_val)

    # concat all selected PSMs and extract from dataset using their indices
    best_scoring_psms_list = pd.concat(best_scoring_psms_list)
    index_list_of_best_scoring_psms_list = best_scoring_psms_list.index.tolist()
    best_scoring_psms_sample = psm_input_file.iloc[index_list_of_best_scoring_psms_list]

    # select target PSMs within the 1% FDR threshold and all decoy PSMs from the psm dataset
    target_psms_within_fdr_threshold = best_scoring_psms_sample[best_scoring_psms_sample['Label'] == 1]
    decoy_psms = psm_input_file[psm_input_file['Label'] == -1]
    selected_target_and_decoy_psms_combined = pd.concat([target_psms_within_fdr_threshold, decoy_psms])

    # training model using selected PSMs with all feature variables
    # full-set PSM dataset is validated using all feature variables
    training_all_feature_variables_sample = selected_target_and_decoy_psms_combined[feature_variables]
    training_all_feature_labels_sample = np.array(selected_target_and_decoy_psms_combined['Label'])

    testing_all_feature_variables_sample = psm_input_file[feature_variables]
    testing_all_feature_labels_sample = np.array(psm_input_file['Label'])

    # select best overall parameters from gridsearch
    best_hyperparameters = grid_search_best_parameters(hyperparameter_grid_search_list)

    # fit model and obtain psm class type predictions and probability scores
    random_forest_final_model = RandomForestClassifier(warm_start=False, **best_hyperparameters)
    random_forest_final_model.fit(training_all_feature_variables_sample, training_all_feature_labels_sample)
    main_predictor_predictions = random_forest_final_model.predict(testing_all_feature_variables_sample)
    main_predictor_probability_scores = (random_forest_final_model.predict_proba
                                         (testing_all_feature_variables_sample))
    main_predictor_probability_scores = main_predictor_probability_scores.round(6)

    # aggregate results into a dataframe for analysis, include psm identification indices
    validated_psm_identification_index = psm_input_file['PSMId'].to_numpy()
    main_predictor_complete_dataframe = pd.DataFrame({'PSMiD': validated_psm_identification_index,
                                                      'Label': testing_all_feature_labels_sample,
                                                      'Predicted': main_predictor_predictions,
                                                      'Probability P(-1)': main_predictor_probability_scores[:, 0]})

    main_predictor_complete_dataframe = main_predictor_complete_dataframe.sort_values(by=['Probability P(-1)'])
    main_predictor_complete_dataframe = fdr_calculation(main_predictor_complete_dataframe)

    return main_predictor_complete_dataframe


def counting_system(input_psms_original, targets_count_list, predictor_dataframe_list):
    # run main predictor function using ranked PSM dataset, append to the appropriate list
    predictor_output = random_forest_main_predictor(input_psms_original)
    predictor_dataframe_list.append(predictor_output)

    # count the number of target PSMs with a prediction probability score <= 0.1, append to appropriate list
    most_confidently_predicted_psms = predictor_output[predictor_output['Probability P(-1)'] <= 0.1]
    number_of_confident_targets_df = most_confidently_predicted_psms[most_confidently_predicted_psms['Label'] == 1]
    number_of_confident_targets_df = len(number_of_confident_targets_df)
    targets_count_list.append(number_of_confident_targets_df)

    # compare target PSM count of current main prediction and that of the previous run
    # if the count is more, run the main prediction again using the current main predictors ranked PSM dataset
    # if the count is less, proceed with the ranked PSM dataframe of the previous main prediction run
    last_iteration_target_count = targets_count_list[-1]
    second_last_iteration_target_count = targets_count_list[-2]

    if last_iteration_target_count >= second_last_iteration_target_count:
        # use PSM indices in their current ranking to obtain a re-ranked PSM dataset
        index_list_of_predictor_output = predictor_output.index.tolist()
        new_input_data = input_psms_original.iloc[index_list_of_predictor_output]

        # copy FDR from previous run over to re-ranked dataset
        new_input_data['FDR'] = predictor_output['FDR'].values

        # call the counting system function within itself to initiate the main predictor function
        # submit the re-ranked PSM dataset, updated target PSM count list and updated preditor dataframe list
        counting_system(new_input_data, targets_count_list, predictor_dataframe_list)

    else:
        # select previous dataframe from the main predictor output list
        best_predictor_output = predictor_dataframe_list[-2]
        # remove columns from previous run to prevent duplicates
        predictor_output_dropped_fdr_df = best_predictor_output.drop(columns=['Target Counter', 'Decoy Counter',
                                                                              'Target', 'Decoy'])
        # calculate the confusion matrix for further analysis
        best_predictor_output_confusion_matrix = confusion_matrix_dataframe(predictor_output_dropped_fdr_df)
        best_predictor_output_confusion_matrix.to_csv('confusion matrix random forest.csv')
        return best_predictor_output_confusion_matrix


# rank in ascending order by pep feature variable and estimate FDR
pep_ranked_dataset = psm_dataset.sort_values(by=['pep'])
fdr_dataset_pep = fdr_calculation(pep_ranked_dataset)

# create list variable of target PSM sum and predictor dataframe output
cumulated_target_psms_list = [0]
main_predictor_output_list = []

# initiate main prediction by calling the counting system to begin the conditional target PSM counting loop
final_output = counting_system(fdr_dataset_pep, cumulated_target_psms_list, main_predictor_output_list)

end_time = time.time()
ft = (end_time - start_time) / 60
print('run time: ', ft, ' min')
