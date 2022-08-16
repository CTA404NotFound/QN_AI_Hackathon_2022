from transformers import AutoModel,BertPreTrainedModel
import torch
import torch.nn as nn
import time
from transformers import RobertaModel, RobertaConfig, AutoConfig, AutoTokenizer
from transformers.models.roberta.modeling_roberta import RobertaPreTrainedModel
import torch

from config import *

class MaskClassifier(RobertaPreTrainedModel):
    """Custom PhoBert model

    Args:
        RobertaPreTrainedModel (object): Pre-trained model
    """
    def __init__(self, config):
        super().__init__(config=config)
        self.bert = RobertaModel(config)
        # self.bert = BertModel(config)
        self.dropout = nn.Dropout(p=0.1)
        self.classifier1 = nn.Linear(config.hidden_size, config.hidden_size)
        self.classifier = nn.Linear(config.hidden_size, 30)

        nn.init.normal_(self.classifier.weight, std=0.02)
        nn.init.normal_(self.classifier.bias, 0)

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
    ):

        last_hidden_state, output = self.bert(
        input_ids=input_ids,
        attention_mask=attention_mask,
        return_dict=False # Dropout will errors if without this
        )
        x = self.dropout(output)
        x = self.classifier1(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.classifier(x)
        return x

model_path = MODEL_FILE_NAME
model = MaskClassifier.from_pretrained("D:/AI Camp/QN_AI_Hackathon_2022/Final_Folder/hackathon-example-submit/PhoBert_train/")
# model.load_state_dict(
#             torch.load(model_path,
#                        map_location=torch.device('cpu')),
#             strict=False)
# model.to(torch.device(DEVICE))

def predict(input_ids, input_mask):
    global model
    cls_output = model(input_ids, input_mask)
    # output_one_hot_vector = torch.where(torch.sigmoid(cls_output) > 0.99, 1., 0.)
    return cls_output

# class ReviewClassifierModel(nn.Module):

#     def __init__(self, model_path):
#         super(ReviewClassifierModel, self).__init__()
#         self.model = PhoBertSentimentClassification()
#         self.setup(model_path)

#     def setup(self, model_path):
#         self.model.load_state_dict(
#             torch.load(model_path,
#                        map_location=torch.device('cpu')),
#             strict=False)
#         self.model.to(torch.device(DEVICE))
    
#     def predict(self, input_ids, input_mask):
#         cls_output = self.model(input_ids, input_mask)
#         # output_one_hot_vector = torch.where(torch.sigmoid(cls_output) > 0.99, 1., 0.)
#         return cls_output