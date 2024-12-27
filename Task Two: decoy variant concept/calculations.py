import numpy as np


def fdr_calculation(dataframe):

    counter = 0
    target = []
    decoy = []

    for item in dataframe['Label']:
        if item == 1:
            target.append(counter + 1)
            decoy.append(0)

        else:
            decoy.append(counter + 1)
            target.append(0)

    # Counter for Target and Decoy hits
    dataframe['Target Counter'] = target
    dataframe['Decoy Counter'] = decoy

    # Cumulative sum of each ID for Target and Decoy Counter
    dataframe['Target'] = np.cumsum(target)
    dataframe['Decoy'] = np.cumsum(decoy)

    fdr_list = []
    for PSMiD in dataframe.index:
        try:
            fdr_score = (dataframe['Decoy'][PSMiD]) / (dataframe['Target'][PSMiD])

        except ZeroDivisionError:
            fdr_score = 0

        fdr_list.append(fdr_score)

    dataframe['FDR'] = fdr_list

    return dataframe


def confusion_matrix_dataframe(dataframe):

    sorted_predicted_probability_dataframe = dataframe

    counter = 0
    target = []
    decoy = []

    for item in sorted_predicted_probability_dataframe['Label']:
        if item == 1:
            target.append(counter + 1)
            decoy.append(0)

        else:
            decoy.append(counter + 1)
            target.append(0)

    # Counter for Target and Decoy hits
    sorted_predicted_probability_dataframe['Target Counter'] = target
    sorted_predicted_probability_dataframe['Decoy Counter'] = decoy
    # Cumulative sum of each ID for Target and Decoy Counter
    sorted_predicted_probability_dataframe['Target'] = np.cumsum(target)
    sorted_predicted_probability_dataframe['Decoy'] = np.cumsum(decoy)

    # # # TP / FP / TN / FN
    # FP = Decoy cumulative sum
    sorted_predicted_probability_dataframe['FP'] = sorted_predicted_probability_dataframe['Decoy']

    # TP = Target (cumulative sum) - Decoy (Cumulative sum)
    true_positive = sorted_predicted_probability_dataframe['Target'] - sorted_predicted_probability_dataframe['FP']
    sorted_predicted_probability_dataframe['TP'] = true_positive

    # Total sum of Target and Decoy in Dataframe
    decoy_sum = sorted_predicted_probability_dataframe['Decoy Counter'].sum()
    target_sum = sorted_predicted_probability_dataframe['Target Counter'].sum()
    target_minus_decoy = target_sum - decoy_sum

    # TN  = Decoy Total Sum - Decoy(x)
    TN = []
    for Decoy_Score in sorted_predicted_probability_dataframe['Decoy']:
        true_negative = decoy_sum - Decoy_Score
        TN.append(true_negative)
    sorted_predicted_probability_dataframe['TN'] = TN

    # FN = (Target_Sum - Decoy_Sum) - (Target_Score - Decoy_Score)
    FN = []
    for Score in sorted_predicted_probability_dataframe.index:
        false_negative = target_minus_decoy - (sorted_predicted_probability_dataframe['Target'][Score] -
                                               sorted_predicted_probability_dataframe['Decoy'][Score])
        FN.append(false_negative)
    sorted_predicted_probability_dataframe['FN'] = FN

    # ROC Curve Calculations
    # Specificity = FP / (FP + TN)
    specificity = []
    for PSMiD in sorted_predicted_probability_dataframe.index:
        specificity_score = sorted_predicted_probability_dataframe['FP'][PSMiD] / (
                sorted_predicted_probability_dataframe
                ['FP'][PSMiD] +
                sorted_predicted_probability_dataframe
                ['TN'][PSMiD])

        specificity.append(specificity_score)

    # Sensitivity = TP / (TP + FN)
    sensitivity = []
    for PSMiD in sorted_predicted_probability_dataframe.index:
        sensitivity_score = sorted_predicted_probability_dataframe['TP'][PSMiD] / (
                sorted_predicted_probability_dataframe
                ['TP'][PSMiD] +
                sorted_predicted_probability_dataframe
                ['FN'][PSMiD])

        sensitivity.append(sensitivity_score)

    sorted_predicted_probability_dataframe['Sensitivity'] = sensitivity
    sorted_predicted_probability_dataframe['1 - Specificity'] = specificity

    # precision / recall curve calculations
    precision_scores = []
    for PSMiD in sorted_predicted_probability_dataframe.index:
        precision = sorted_predicted_probability_dataframe['TP'][PSMiD] / (sorted_predicted_probability_dataframe
                                                                           ['TP'][PSMiD] +
                                                                           sorted_predicted_probability_dataframe
                                                                           ['FP'][PSMiD])
        precision_scores.append(precision)

    recall_scores = []
    for PSMiD in sorted_predicted_probability_dataframe.index:
        recall = sorted_predicted_probability_dataframe['TP'][PSMiD] / (sorted_predicted_probability_dataframe
                                                                        ['TP'][PSMiD] +
                                                                        sorted_predicted_probability_dataframe
                                                                        ['FN'][PSMiD])
        recall_scores.append(recall)

    sorted_predicted_probability_dataframe['Precision'] = precision_scores
    sorted_predicted_probability_dataframe['Recall'] = recall_scores

    return sorted_predicted_probability_dataframe


def pep_calculation(dataframe):
    pep_score_list = []
    count = 0

    for PSMid in dataframe.index:
        count += 1

        PSMid_probability_scores = dataframe['Probability P(-1)'][PSMid]
        upper_range = PSMid_probability_scores + 0.01
        lower_range = PSMid_probability_scores - 0.01

        container = (dataframe['Probability P(-1)'] >= lower_range) & (dataframe['Probability P(-1)'] < upper_range)
        df_of_range = dataframe[container]

        targets = df_of_range[df_of_range['Label'] == 1].shape[0]
        decoys = df_of_range[df_of_range['Label'] == -1].shape[0]

        pep_score = (decoys / targets)
        pep_score_list.append(pep_score)

    dataframe['pep_scores'] = pep_score_list

    return dataframe
