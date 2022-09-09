from transformers import AutoTokenizer
from processing import encode_review, format_label
from model import predict
from config import *

def inference(input_ids, input_mask):
    output_one_hot_vector = predict(input_ids, input_mask)
    standard_output = format_label(output_one_hot_vector)
    return standard_output

tokenizer = AutoTokenizer.from_pretrained(BERT_NAME)

def solve(text):
    global tokenizer
    input_ids, attention_mask = encode_review(text, tokenizer, DEVICE)
    output = inference(input_ids, attention_mask)
    return output

# def inference(input_ids, input_mask):
#     output_one_hot_vector = predict(input_ids, input_mask)
#     standard_output = format_label(output_one_hot_vector)
#     return standard_output

# def solve(text, device):
#     tokenizer = AutoTokenizer.from_pretrained(BERT_NAME, use_fast=False)
#     input_ids, attention_mask = encode_review(text, tokenizer, device)
#     output = inference(input_ids, attention_mask)
#     return output



