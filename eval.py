import numpy as np

def generate_format_array(aspect_idx, prediction, label):
    """Function to generate format arrays of prediction and ground truth values

    Args:
        aspect_idx: (Int): Number indicates index of aspect detected in the output vector
        prediction (List): List of predicted aspects along with their polarity scores
        label (List): List of ground truth aspects along with their polarity scores
    """
    format_pred = [0] * len(prediction)
    format_label = [0] * len(label)
    num_eles = len(prediction)
    
    for i in range(num_eles):
        if prediction[i][aspect_idx] != 0:
            format_pred[i] = 1
    
    for i in range(num_eles):
        if label[i][aspect_idx] != 0:
            format_label[i] = 1
    return format_pred, format_label

def is_different_vectors(pred_vector, gt_vector):
    """Function to judge whether values in two vectors are totally different

    Args:
        pred_vector (List): Format vector of predictions
        gt_vector (List): Format vector of labels
    """
    flag = True
    for i in range(len(pred_vector)):
        if pred_vector[i] == gt_vector[i]:
            flag = False
    return flag

def eval_metrics(aspect_idx, prediction, label):
    """Custom function for evaluating prediction performance

    Args:
        aspect_idx: (Int): Number indicates index of aspect detected in the output vector
        prediction (List): List of predicted aspects along with their polarity scores
        label (List): List of ground truth aspects along with their polarity scores
    """
    numerator, denominator = [], []
    format_pred, format_label = generate_format_array(aspect_idx, prediction, label)
    if is_different_vectors(format_pred, format_label):
        r2_score = 1
    else:
        num_examples = len(prediction) # Number of predictions equals to number of labels
        for i in range(num_examples):
            if prediction[i] != 0 and label[i] != 0:
                numerator.append((prediction[i] - label[i])**2)
        r2_score = 1 - float(sum(numerator) / sum(denominator))
    
    return r2_score
    


pred = [[1, 0, 3, 4, 2, 0], [0, 2, 2, 5, 1, 0], [2, 3, 1, 5, 4, 0]]
gt = [[1, 1, 3, 5, 3, 1], [0, 0, 3, 4, 0, 0], [2, 1, 1, 5, 3, 0]]
# print(pred[1][0])