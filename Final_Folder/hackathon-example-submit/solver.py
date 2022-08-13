from transformers import AutoModel
from transformers import AutoTokenizer, AutoConfig
from processing import encode_review
from model import ReviewClassifierModel
from config import *

def classify_model(bert_name):
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    bert_config = AutoConfig.from_pretrained(bert_name)
    bert_config.max_position_embeddings = 258
    base_model = AutoModel.from_pretrained(bert_name,
                                           config = bert_config)
    classifier_model = ReviewClassifierModel(model = base_model,
                                             model_path = MODEL_FILE_NAME,
                                             tokenizer = tokenizer)
    return classifier_model

def solve(text):
    input_ids, attention_mask = encode_review(text)
    output = classify_model(input_ids, attention_mask)
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