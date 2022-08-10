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

# class BERT_REGRESSION(nn.Module):
#     def __init__(self, bert_model, num_labels):
#         super(BERT_REGRESSION, self).__init__()
#         self.num_labels = num_labels
#         self.bert = bert_model
#         self.dropout = nn.Dropout(0.2)
#         self.classifier = nn.Linear(768, num_labels)

#     def forward_custom(self, input_ids, attention_mask=None, labels=None):
#         outputs = self.bert(input_ids = input_ids, attention_mask=attention_mask)
#         sequence_output = self.dropout(outputs[0])
#         logits = self.classifier(sequence_output)[:,0,:]

#         if labels is not None:
#             loss_fct = nn.MSELoss()
#             loss = loss_fct(logits, labels)
#             return logits,loss
#         return logits


class ReviewClassifierModel(nn.Module):

    def __init__(self, base_model, num_labels, model_path, tokenizer):
        super(ReviewClassifierModel, self).__init__()
        self.num_labels = num_labels
        self.model = PhoBertSentimentClassification()
        self.tokenizer = AutoTokenizer.from_pretrained(BERT_NAME, use_fast = False)
        self.setup(base_model, model_path)

    def setup(self, base_model, model_path):
        self.model = PhoBertSentimentClassification()
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
        output_one_hot_vector = torch.where(torch.sigmoid(results) > 0.98, 1., 0.)
        output = self.convert_output_format(output_one_hot_vector)
        return output.cpu().numpy().tolist()
