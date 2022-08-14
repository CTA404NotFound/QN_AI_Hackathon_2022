from transformers import AutoModel
from transformers import AutoTokenizer, AutoConfig
from processing import encode_review, format_label
from model import ReviewClassifierModel
from config import *

import torch

def inference(input_ids, input_mask, BERT_NAME):
    bert_config = AutoConfig.from_pretrained(BERT_NAME)
    bert_config.max_position_embeddings = 258
    classifier_model = ReviewClassifierModel(model_path = MODEL_FILE_NAME)
    
    output_one_hot_vector = classifier_model.predict(input_ids, input_mask)
    standard_output = format_label(output_one_hot_vector)
    return standard_output

def solve(text, device, BERT_NAME):
    tokenizer = AutoTokenizer.from_pretrained(BERT_NAME)
    input_ids, attention_mask = encode_review(text, tokenizer, device)
    output = inference(input_ids, attention_mask, BERT_NAME)
    return output

# class ClassifyReviewSolver:
#     def __init__(self, config):
#         self.config = config
#         self.classify_model = None
#         self.processing_text = None
#         self.setup(bert_name = BERT_NAME)

#     def setup(self, bert_name):
#         tokenizer = AutoTokenizer.from_pretrained(bert_name,
#                                                   do_lower_case=False,
#                                                   use_fast=False)
#         # setup bert
#         bert_config = AutoConfig.from_pretrained(bert_name,
#                                              output_hidden_states=True)
#         bert_config.max_position_embeddings = 258

#         base_model = AutoModel.from_pretrained(
#             bert_name,
#             config=bert_config,
#             add_pooling_layer=False
#         )

#         self.classify_model = ReviewClassifierModel(base_model = base_model,
#                                                     model_path = self.config.MODEL_FILE_NAME,
#                                                     num_labels = NUM_LABEL,
#                                                     tokenizer = tokenizer)

#     def solve(self, text):
#         sub_words = self.processing_text.add_subword(text)
#         x_padding, attention_masks = self.processing_text.padding_data(sub_words)

#         output = self.classify_model.predict(x_padding, attention_masks)
#         return output