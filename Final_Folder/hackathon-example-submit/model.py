import torch.nn as nn
import torch

from transformers import AutoModel, AutoTokenizer
from config import *

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

class ReviewClassifierModel(nn.Module):

    def __init__(self, model_path, tokenizer):
        super(ReviewClassifierModel, self).__init__()
        self.tokenizer = tokenizer
        self.model = PhoBertSentimentClassification()
        self.setup(model_path)

    def setup(self, model_path):
        self.model.load_state_dict(
            torch.load(model_path,
                       map_location=torch.device('cpu')),
            strict=False)
        self.model.to(torch.device(DEVICE))
    def convert_output_format(output_one_hot_vector):
        output_tensor = torch.reshape(output_one_hot_vector, shape = (-1,))
        standard_output = []
        for i in range(0, len(output_tensor), 5):
            if not any(output_tensor[i: i + 5]):
                standard_output.append(0)
            for j in range(0, 5):
                if output_tensor[i + j] == 1:
                    standard_output.append(j + 1)
        return standard_output

    def predict(self, ids_tensor, mask_tensor):
        # self.model.eval()
        # with torch.no_grad():
        results = self.model(ids_tensor, mask_tensor)
        output_one_hot_vector = torch.where(torch.sigmoid(results) > 0.99, 1., 0.)
        output = self.convert_output_format(output_one_hot_vector)
        return output
