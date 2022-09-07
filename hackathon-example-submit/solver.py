# from transformers import AutoModel
from transformers import AutoTokenizer
from processing import encode_review, format_label
# from model import ReviewClassifierModel
from model import predict
from config import BERT_NAME
# import torch

# def inference(input_ids, input_mask, BERT_NAME):
#     bert_config = AutoConfig.from_pretrained(BERT_NAME)
#     bert_config.max_position_embeddings = 258
#     # classifier_model = ReviewClassifierModel(model_path = MODEL_FILE_NAME)
    
#     # output_one_hot_vector = classifier_model.predict(input_ids, input_mask)
#     output_one_hot_vector = predict(input_ids, input_mask)
#     standard_output = format_label(output_one_hot_vector)
#     return standard_output

# def solve(text, device, BERT_NAME):
#     tokenizer = AutoTokenizer.from_pretrained(BERT_NAME)
#     input_ids, attention_mask = encode_review(text, tokenizer, device)
#     output = inference(input_ids, attention_mask, BERT_NAME)
#     return output

def inference(input_ids, input_mask):
    output_one_hot_vector = predict(input_ids, input_mask)
    standard_output = format_label(output_one_hot_vector)
    return standard_output

def solve(text, device):
    tokenizer = AutoTokenizer.from_pretrained(BERT_NAME, use_fast=False)
    input_ids, attention_mask = encode_review(text, tokenizer, device)
    output = inference(input_ids, attention_mask)
    return output



