# from transformers import AutoModel
# import torch
# import torch.nn as nn
# import time
# class SentimentClassifier(nn.Module):
#     def __init__(self, n_classes):
#         super(SentimentClassifier, self).__init__()
#         self.bert = AutoModel.from_pretrained("vinai/phobert-base")
#         # self.bert = model.load_state_dict(torch.load(f'/content/content/phobert_fold10.pth'))
#         self.drop = nn.Dropout(p=0.3)
#         self.fc = nn.Linear(self.bert.config.hidden_size, 30)
#         nn.init.normal_(self.fc.weight, std=0.02)
#         nn.init.normal_(self.fc.bias, 0)

#     def forward(self, input_ids, attention_mask):
#         last_hidden_state, output = self.bert(
#             input_ids=input_ids,
#             attention_mask=attention_mask,
#             return_dict=False # Dropout will errors if without this
#         )

#         x = self.drop(output)
#         x = self.fc(x)
#         return x
# device = torch.device('cpu')
# model = SentimentClassifier(n_classes=7)
# model.to(device)
# model.load_state_dict(torch.load(f'model_weights\last_step.pth',map_location=torch.device('cpu')))
import numpy as np

lista = [1, 0, 1, 1, 0.67, 0]
listb = [1, 1, 0.96875, 0.9375, 0.9375, 1]

res = sum([a*b for a,b in zip(lista,listb)])
print(1/6 * res)