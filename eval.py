# import numpy as np
from sklearn.metrics import f1_score

def generate_format_array(aspect_idx, prediction, label):
    """Function to generate format arrays of prediction and ground truth values.

    Args:
        aspect_idx: (Int): Number indicates index of aspect detected in the output vector
        prediction (List): List of predicted aspects along with their polarity scores
        label (List): List of ground truth aspects along with their polarity scores
    Returns:
        Format array indicates which aspects appear in this sample.
    """
    format_pred = [0] * len(prediction)
    format_label = [0] * len(label)
    num_elements = len(prediction)
    
    for i in range(num_elements):
        if prediction[i][aspect_idx] != 0:
            format_pred[i] = 1
    
    for i in range(num_elements):
        if label[i][aspect_idx] != 0:
            format_label[i] = 1
    return format_pred, format_label

def is_different_vectors(pred_vector, gt_vector):
    """Function to judge whether values in two vectors are totally different

    Args:
        pred_vector (List): Format vector of predictions
        gt_vector (List): Format vector of labels
    Returns:
        The Boolean value indicates whether two vectors are totally different
    """
    flag = True
    for i in range(len(pred_vector)):
        if pred_vector[i] == gt_vector[i]:
            flag = False
    return flag

def eval_metrics(aspect_idx, prediction, label):
    """Custom function for evaluating prediction performance.
    Calculate the f1_score and r2_score of a specify aspect.

    Args:
        aspect_idx: (Int): Number indicates index of aspect detected in the output vector
        prediction (List): List of predicted aspects along with their polarity scores
        label (List): List of ground truth aspects along with their polarity scores
    Returns:
        F1 score and R2 score of an aspect
    """
    numerator, denominator = [], []
    format_pred, format_label = generate_format_array(aspect_idx, prediction, label)
    if is_different_vectors(format_pred, format_label):
        aspect_r2_score = 1
    else:
        num_examples = len(prediction) # Number of predictions equals to number of labels
        for i in range(num_examples):
            numerator.append((prediction[i][aspect_idx] - label[i][aspect_idx])**2)
            denominator.append(16)
        aspect_r2_score = 1 - float(sum(numerator) / sum(denominator))
    
    aspect_f1_score = f1_score(format_pred, format_label)
    
    return aspect_f1_score, aspect_r2_score
