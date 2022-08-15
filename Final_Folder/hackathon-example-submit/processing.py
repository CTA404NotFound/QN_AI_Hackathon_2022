import torch
import re
import demoji

from base64 import encode
# import encodings
from multiprocessing.spawn import _main
from unittest.main import main
# from transformers import AutoTokenizer
# from tqdm import tqdm
import pandas as pd
import re
from nltk.stem.porter import PorterStemmer
# from nltk.stem.lancaster import LancasterStemmer
from vncorenlp import VnCoreNLP
# from underthesea import word_tokenize
from config import VN_STOP_WORD, VNCORENLP


stopwords_file = open(VN_STOP_WORD, "r", encoding = "utf-8")
stopwords_content = stopwords_file.read()
stopwords_list = stopwords_content.split("\n")
stemmer = PorterStemmer()
vnp = VnCoreNLP(VNCORENLP,annotators="wseg")

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text

def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji].split(":")[0])

    return string

def remove_stopwords(text):
    text = [word for word in text if word not in stopwords_list]
    # new_text = " ".join(text)
    return text

def stemming(text):
    text = [stemmer.stem(word) for word in text]
    # new_text = " ".join(text)
    return text

def word_tokenizer(text):
    tokens = vnp.tokenize(text)
    return tokens

#Underthesea segment
# def word_tokenizer(text):
#     text = text.replace(".", "")
#     tokens = word_tokenize(text)
#     return tokens

def preprocessing(text):
    text = remove_url(text)
    text = handle_emoji(text)
    text = text.lower() 
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'(ks)', 'khách_sạn', text)
    # text = sc1(text)
    text = word_tokenizer(text)
    text = remove_stopwords(text)
    # # print(text)
    text = " ".join(text[0])

    return text

def encode_review(text, tokenizer, device, max_seq_length=256):
    text = preprocessing(text)
    encodings = tokenizer.encode_plus(text, max_length = max_seq_length,
                                           truncation = True,
                                           add_special_tokens = True,
                                           padding = "max_length",
                                           return_attention_mask = True,
                                           return_token_type_ids = False,
                                           return_tensors = "pt")
    
    input_ids = encodings["input_ids"].to(device)
    attention_mask = encodings["attention_mask"].to(device)
    return torch.tensor(input_ids), torch.tensor(attention_mask)

def format_label(output_one_hot_tensor):
    """Convert the model's output vector into standard vector format following the organizer's ones

    Args:
        output_one_hot_tensor (Tensor): The model's output vector

    Returns:
        List: List of sentimental polarity scores of aspects following the organizer's format
    """
    lbl_real = []
    lbl_prefix = torch.where(torch.sigmoid(output_one_hot_tensor) > 0.99, torch.sigmoid(output_one_hot_tensor), 0.)
    split_tensor = list(torch.tensor_split(lbl_prefix[0], 6))
    for i in range(len(split_tensor)):
        if(torch.count_nonzero(split_tensor[i]).item()==0):
            continue
        else:
            split_tensor[i] = torch.where(split_tensor[i] == torch.max(split_tensor[i]), 1, 0.)
    for i in range(len(split_tensor)):
        split_tensor[i] = split_tensor[i].tolist()
        if 1 in split_tensor[i]:
            idx = split_tensor[i].index(1)
            lbl_real.append(idx+1)
        else:
            lbl_real.append(0)
    return lbl_real

# def convert_output_format(output_one_hot_tensor):
#     output_tensor = torch.reshape(output_one_hot_tensor, shape = (-1,))
#     standard_output = []
#     for i in range(0, len(output_tensor), 5):
#         if not any(output_tensor[i: i + 5]):
#             standard_output.append(0)
#         for j in range(0, 5):
#             if output_tensor[i + j] == 1:
#                 standard_output.append(j + 1)
#     return standard_output