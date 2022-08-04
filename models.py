from transformers import AutoTokenizer, AutoModel

import torch
import torch.nn as nn


class PhoBertSentimentClassification(nn.Module):
    """
        PhoBert Pre-trained model for aspect and polarity score classification
    """

    def __init__(self, n_labels):
        super(PhoBertSentimentClassification, self).__init__(n_labels)
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base")
        self.dropout = nn.Dropout(p = 0.3)
        self.n_labels = n_labels
        self.dense = torch.nn.Linear(self.phobert.hidden_size * 4, self.n_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.phobert(input_ids, attention_mask=attention_mask,
                               return_dict = False)
        cls_output = torch.cat((outputs[2][-1][:, 0, ...],
                                outputs[2][-2][:, 0, ...],
                                outputs[2][-3][:, 0, ...],
                                outputs[2][-4][:, 0, ...]), -1)
        features = self.dense(cls_output)
        return features
