from config import *
import settings
from solver import solve

import torch

device = torch.device('cpu')
review_sentence = "Sạch_sẽ , yên_tĩnh , ấm_cúng"
predict_results = solve(review_sentence, device, BERT_NAME)
print(predict_results)