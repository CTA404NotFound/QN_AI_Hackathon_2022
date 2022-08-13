import torch
import re
import demoji

from base64 import encode
import encodings
from multiprocessing.spawn import _main
from unittest.main import main
from transformers import AutoTokenizer, T5ForConditionalGeneration
from tqdm import tqdm
import pandas as pd
import re
import demoji
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from vncorenlp import VnCoreNLP
from config import VN_STOP_WORD,VNCORENLP

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
    # tokens = [t for ts in tokens for t in ts]
    # word_segmented_text = " ".join(tokens)
    return tokens

def preprocessing(text):
    text = remove_url(text)
    text = handle_emoji(text)
    text = text.lower() 
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'(ks)', 'khách_sạn', text)
    # text = sc1(text)
    text = word_tokenizer(text)
    text = remove_stopwords(text)
    # print(text)
    text = " ".join(text[0])

    return text

def encode_review(text, tokenizer, max_seq_length=256):
    text = preprocessing(text)
    encodings = tokenizer.encode_plus(
        text, padding = "max_length", max_length = max_seq_length, truncation=True)
    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]
    return input_ids, attention_mask