# import libraries and Python file: calculations
import numpy as np
import time
import pandas as pd
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier
import os
from calculations import *

start_time = time.time()
# setup base estimator: feature variables & class labels
feature_variables = ["measured_rt",
                     "predicted_rt",
                     "engine_score",
                     "measured_mz",
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
                     "enzymatic",
                     "rt_Abs_error",
                     "rt_Square_error",
                     "rt_Log_error",
                     "matched_peaks",
                     "spectra_log",
                     "spectra_cos_similarity",
                     "spectra_angular_similarity",
                     "spectra_cross_entropy",
                     "b_ion_coverage",
                     "b_ion_matched_peaks",
                     "b_ion_spectra_log",
                     "b_ion_spectra_cos_similarity",
                     "b_ion_spectra_angular_similarity",
                     "b_ion_spectra_cross_entropy",
                     "y_ion_coverage",
                     "y_ion_matched_peaks",
                     "y_ion_spectra_log",
                     "y_ion_spectra_cos_similarity",
                     "y_ion_spectra_angular_similarity",
                     "y_ion_spectra_cross_entropy"]

# stratification setup and selected feature variable
stratified_kfold_setup = StratifiedKFold(n_splits=3, random_state=1, shuffle=True)
selected_feature_variable = ['pep']
processed_iPSC_directory_confusion_matrix_only = 'Decoy Variant: iPSCs processed confusion matrix only'
merged_processed_iPSCs_with_input_files = 'Decoy Variant: iPSCs merged dataframes'


def grid_search_best_parameters(parameter_list):
    counter = 0
    num = parameter_list[0]

    for item in parameter_list:
        curr_frequency = parameter_list.count(item)
        if curr_frequency > counter:
            counter = curr_frequency
            num = item

    return num


def extra_trees_main_predictor(psm_input_file):

    # create list variables for PSM selection and hyperparameter tuning
    best_scoring_psms_list = []
    hyperparameter_grid_search_list = []

    # select PSMs from dataset for a single feature variable
    psm_dataset_single_feature_variable_sample = psm_input_file[selected_feature_variable]
    psm_dataset_single_feature_labels_sample = np.array(psm_input_file['Label'])

    # 3-fold cross-validation
    for fold, (train_index, test_index) in (
            enumerate(stratified_kfold_setup.split(psm_dataset_single_feature_variable_sample,
                                                   psm_dataset_single_feature_labels_sample))):
        # 2 folds for training
        training_folds = psm_input_file.iloc[train_index]
        # 1 fold for validation
        validation_fold = psm_input_file.iloc[test_index]

        # select target PSMs within 1% FDR threshold from training folds
        # select all random decoy PSMs from input file
        # combine selected target and decoy PSMs for hyperparameter tuning
        psms_within_fdr_threshold = training_folds[training_folds['FDR'] <= 0.01]
        target_psms_within_fdr_threshold = psms_within_fdr_threshold[psms_within_fdr_threshold['Label'] == 1]
        decoy_psms = training_folds[training_folds['Label'] == -1]
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

            grid = {'n_estimators': [100, 200], 'min_samples_leaf': [20, 100], 'max_depth': [3, 5]}

            extra_trees_hyperparameter_search = (GridSearchCV(estimator=ExtraTreesClassifier(warm_start=False),
                                                              param_grid=grid))

            extra_trees_hyperparameter_search.fit(nested_cross_validation_training_feature,
                                                  nested_cross_validation_training_labels)
            best_parameters_compiled = extra_trees_hyperparameter_search.best_params_
            hyperparameter_grid_search_list.append(best_parameters_compiled)

        # select most common occurring parameters
        best_parameters = grid_search_best_parameters(hyperparameter_grid_search_list)

        # training model using selected PSMs of a single feature variable
        # validate model using validation fold PSMs of a single feature variable
        training_single_feature_variable_sample = selected_psms_feature_variable
        training_single_feature_labels_sample = np.array(selected_psms_labels)

        testing_single_feature_variable_sample = validation_fold[selected_feature_variable]
        testing_single_feature_labels_sample = np.array(validation_fold['Label'])

        # fit model and obtain PSM class type predictions and probability scores
        extra_trees_cross_validation_model = ExtraTreesClassifier(warm_start=False, **best_parameters)
        extra_trees_cross_validation_model.fit(training_single_feature_variable_sample,
                                               training_single_feature_labels_sample)

        cross_validation_predictions = (extra_trees_cross_validation_model.predict
                                        (testing_single_feature_variable_sample))
        cross_validation_probability_scores = (extra_trees_cross_validation_model.predict_proba
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

    # training model using selected PSMs of all feature variables
    # full-set PSM dataset is validated using all feature variables
    training_all_feature_variables_sample = selected_target_and_decoy_psms_combined[feature_variables]
    training_all_feature_labels_sample = np.array(selected_target_and_decoy_psms_combined['Label'])

    testing_all_feature_variables_sample = psm_input_file[feature_variables]
    testing_all_feature_labels_sample = np.array(psm_input_file['Label'])

    # select best overall parameters from gridsearch
    best_hyperparameters = grid_search_best_parameters(hyperparameter_grid_search_list)

    # fit model and obtain psm class type predictions and probability scores
    extra_trees_final_model = ExtraTreesClassifier(warm_start=False, **best_hyperparameters)
    extra_trees_final_model.fit(training_all_feature_variables_sample, training_all_feature_labels_sample)

    main_predictor_predictions = extra_trees_final_model.predict(testing_all_feature_variables_sample)
    main_predictor_probability_scores = (extra_trees_final_model.predict_proba
                                         (testing_all_feature_variables_sample))
    main_predictor_probability_scores = main_predictor_probability_scores.round(6)

    # aggregate results into a dataframe for analysis, include psm identification indices
    validated_psm_identification_index = psm_input_file['PSMId'].to_numpy()
    main_predictor_complete_dataframe = pd.DataFrame({'PSMId': validated_psm_identification_index,
                                                      'Label': testing_all_feature_labels_sample,
                                                      'Predicted': main_predictor_predictions,
                                                      'Probability P(-1)': main_predictor_probability_scores[:, 0]})

    main_predictor_complete_dataframe = main_predictor_complete_dataframe.sort_values(by=['Probability P(-1)'])
    main_predictor_complete_dataframe = fdr_calculation(main_predictor_complete_dataframe)

    return main_predictor_complete_dataframe


def counting_system(input_psms_original, targets_count_list, predictor_dataframe_list, df_number):
    # run main predictor function using ranked PSM dataset, append to the appropriate list
    predictor_output = extra_trees_main_predictor(input_psms_original)
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
        counting_system(new_input_data, targets_count_list, predictor_dataframe_list, df_number)

    else:

        iPSC_file_number = str(df_number)

        # select previous dataframe from the main predictor output list
        best_predictor_output = predictor_dataframe_list[-2]
        # remove columns from previous run to prevent duplicates/redundancy
        predictor_output_dropped_fdr_df = best_predictor_output.drop(columns=['Target Counter', 'Decoy Counter',
                                                                              'Target', 'Decoy', 'FDR'])

        # calculate the confusion matrix for further analysis
        best_predictor_output_confusion_matrix = confusion_matrix_dataframe(predictor_output_dropped_fdr_df)
        best_predictor_output_pep_cm = pep_calculation(best_predictor_output_confusion_matrix)
        best_predictor_output_pep_cm.to_csv(os.path.join(processed_iPSC_directory_confusion_matrix_only,
                                                         iPSC_file_number + ' confusion matrix.csv'))

        return best_predictor_output_pep_cm


# assign directory
iPSCs_directory = 'iPSC files'
# reference tonsil file * unused in thesis results, scribed for future works
tonsil_file = 'tonsil file'

# iterate over files (12) in iPSC directory
for filename in os.scandir(iPSCs_directory):
    if filename.is_file():

        stem_file_name = str(os.path.basename(filename))
        iPSC_file = pd.read_csv(filename, header=0)
        decoy_canonical_PSM_labels = []

        # create class labels for psm type
        # setup for decoy variant as decoy PSM, assign negative class label
        for PSM in iPSC_file['psm_type']:
            if PSM == 'target_seq_decoy_var':
                random_label = -1
                decoy_canonical_PSM_labels.append(random_label)
            else:
                target_label = 1
                decoy_canonical_PSM_labels.append(target_label)

        iPSC_file['Label'] = decoy_canonical_PSM_labels

        # remove decoy seq PSMs
        stem_psm_dataset = iPSC_file[iPSC_file['psm_type'] != 'decoy_seq']

        # rank by pep and estimate FDR
        pep_ranked_dataset = stem_psm_dataset.sort_values(by=['pep'])
        fdr_dataset_pep = fdr_calculation(pep_ranked_dataset)

        # setup main predictor. new archives are created for each iPSC file
        # create list variable of target PSM sum and predictor dataframe output
        cumulated_target_psms_list = [0]
        main_predictor_output_list = []
        # initiate main prediction by calling the counting system to begin the conditional target PSM counting loop
        final_output = counting_system(fdr_dataset_pep, cumulated_target_psms_list, main_predictor_output_list,
                                       stem_file_name)

        # access directory of processed iPSCs and merge with appropriate input file to align with gene names
        processed_iPSC_df = '/' + stem_file_name + ' confusion matrix.csv'
        processed_iPSC_csv = pd.read_csv(processed_iPSC_directory_confusion_matrix_only + processed_iPSC_df, header=0)
        merged_iPSC_processed_and_input_file = iPSC_file.merge(processed_iPSC_csv, on='PSMId', how='left')

        merged_iPSC_processed_and_input_file.to_csv(os.path.join(merged_processed_iPSCs_with_input_files, stem_file_name
                                                                 + ' merged_stem_and_cm_decoy_seq.csv'))

end_time = time.time()
ft = (end_time - start_time) / 60
print('run time: ', ft, ' min')
