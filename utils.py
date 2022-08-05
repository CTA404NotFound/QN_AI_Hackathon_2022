import torch
import numpy as np


def sigmoid(pred):
    """Custom Sigmoid function"""
    return 1 / (1 + np.exp(-pred))


def softmax(pred):
    """Custom Softmax function"""
    maxes = np.max(pred, axis=-1, keepdims=True)
    shifted_exp = np.exp(pred - maxes)
    return shifted_exp / shifted_exp.sum(axis=-1, keepdims=True)


def word_segmentation(text, segmenter):
    """
    Custom word segmentation using VnCoreNLP toolkit
    """
    output = segmenter.tokenize(text)
    tokens = [t for ts in output for t in ts]
    processed_review = " ".join(tokens)
    return processed_review


def convert_tokens_to_features(texts, tokenizer, segmenter, max_seq_length=256, labels=None):
    """Tokenizing sentences into input ids and attention_mask

    Args:
        texts (list): list of reviews.
        tokenizer: tokenizer of specific pre-trained model.
        segmenter: word segmentation toolkit.
        max_seq_length (int, optional): Sequence length of vectors. Defaults to 256.
        labels (int, optional): _description_. Defaults to None.

    Returns:
        Tensor: input ids, attention_masks of reviews and their respective labels.
    """
    input_ids, attention_masks = [], []
    for text in texts:
        text = word_segmentation(text, segmenter)
        encodings = tokenizer.encode_plus(
            text, padding="max_length", max_length=max_seq_length, truncation=True)
        input_ids.append(encodings["input_ids"])
        attention_masks.append(encodings["attention_mask"])

    if labels is not None:
        return torch.tensor(input_ids, dtype=torch.float32), torch.tensor(attention_masks, dtype=torch.float32), \
            torch.tensor(labels, dtype=torch.float32)

    return torch.tensor(input_ids, dtype=torch.float32), \
        torch.tensor(attention_masks, dtype=torch.float32)

def convert_output_format(output_onehot_tensor):
    """Convert the model's output vector into standard vector format following the organizer's ones

    Args:
        output_onehot_tensor (Tensor): The model's output vector

    Returns:
        List: List of sentimental polarity scores of aspects following the organizer's format
    """
    output_tensor = torch.reshape(output_onehot_tensor, shape = (-1,))
    standard_output = []
    for i in range(0, len(output_tensor), 5):
        if not any(output_tensor[i: i + 5]):
            standard_output.append(0)
        for j in range(1, 5):
            if output_tensor[i + j] == 1:
                standard_output.append(j)
    return standard_output
