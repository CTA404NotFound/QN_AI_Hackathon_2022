import torch.nn as nn
import torch
from transformers import AutoModel
from config import *

class PhoBertSentimentClassification(nn.Module):
    """
        PhoBert Pre-trained model for aspect and polarity score classification
    """

    def __init__(self):
        super(PhoBertSentimentClassification, self).__init__()
        self.bert = AutoModel.from_pretrained(BERT_NAME)
        self.dropout = nn.Dropout(p = 0.1)

        # self.n_labels = n_labels
        self.fc = nn.Linear(self.bert.config.hidden_size, 30)
        nn.init.normal_(self.fc.weight, std = 0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False # Dropout will errors if without this
        )
        x = self.dropout(output)
        x = self.fc(x)
        return x

model_path = MODEL_FILE_NAME
model = PhoBertSentimentClassification()
model.load_state_dict(
            torch.load(model_path,
                       map_location=torch.device(DEVICE)),
            strict=False)
model.to(torch.device(DEVICE))
model.eval()

def predict(input_ids, input_mask):
    global model
    with torch.no_grad():
        cls_output = model(input_ids, input_mask)
        return cls_output