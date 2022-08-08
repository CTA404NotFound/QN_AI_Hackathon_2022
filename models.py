from transformers import AutoModel

import torch
import torch.nn as nn


class PhoBertSentimentClassification(nn.Module):
    """
        PhoBert Pre-trained model for aspect and polarity score classification
    """

    def __init__(self):
        super(PhoBertSentimentClassification, self).__init__()
        self.bert = AutoModel.from_pretrained("vinai/phobert-base")
        self.dropout = nn.Dropout(p = 0.3)
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