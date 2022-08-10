import emoji
import pandas as pd
import re
import torch
import os

from eval import *
from modify_data import *
from utils import convert_output_format
from models import *
from transformers import AutoTokenizer

path_train = "Dataset/train_final.csv"
col = "Review"

def remove_symbol(text):
    """
        Remove the symbols in per review
    Args:
        text (str): a review of "Review" column

    Returns:
        str: a review after remove symbols
    """    

    regex_list = ['#', '@', '^', '&','*','-','=','+','/','%','~','$','(',')','|','{','}']
    for regex in regex_list:
        if regex in text:
            text = text.replace(regex, "")
            text = re.sub("\s\s+", " ", text)
        else:
            pass
    text = text.strip()
    return text
    
def remove_emoji(text):
    """
        Remove the emojis in per review
    Args:
        text (_type_): a review of "Review" column

    Returns:
        str: a review after remove emojis
    """    

    icon = emoji.distinct_emoji_list(text)
    for ic in icon:
        text = text.replace(ic,"")
    return text

def remove_symbol_data(path_data, col):
    """
        Read data from .csv file and Implement the two above remove function. Then save to new .csv file
    Args:
        path_data (str): path of data train
        col (str): name of column  
    """    

    list = []
    data = pd.read_csv(path_data)

    for i,sentence in enumerate(data[col]):
        sentence = remove_symbol(sentence)
        sentence = remove_emoji(sentence)
        data[col][i] = sentence

    data.to_csv("./dataset/data_processed.csv", encoding="utf-8")

def decode_lbl(tensor_d):
    aspect = ['giai_tri', 'luu_tru', 'nha_hang','an_uong','di_chuyen','mua_sam']
    sent = ['very_negative','negative','normal','postive','very_postive']
    temp = []
    for i in range(len(aspect)):
        for j in range(len(sent)):
            temp.append('{'+aspect[i]+'#'+sent[j]+'},')
    for i in range(len(temp)):
        temp[i] = temp[i][:-1] 
    final = ''
    test = tensor_d.tolist()
    # print(temp)
    for i in range(len(test[0])):
        # print(i)
        if(test[0][i]==1):
            lbl=temp[i]
            final+=lbl
    return final

def inference(text, model, tokenizer, device, max_len = 150):
    """Predict sample

    Args:
        text (string): The input text
        model : Model weights
        tokenizer : Tokenizer for input text
        max_len (int, optional): maximum sequence's length for all input vectors. Defaults to 150.

    Returns:
        Output vector and its label
    """
    encoded_review = tokenizer.encode_plus(text, max_length = max_len,
                                           truncation = True,
                                           add_special_tokens = True,
                                           padding = "max_length",
                                           return_attention_mask = True,
                                           return_token_type_ids = False,
                                           return_tensors = "pt")
    
    input_ids = encoded_review['input_ids'].to(device)
    attention_mask = encoded_review['attention_mask'].to(device)
    
    cls_output = model(input_ids, attention_mask)
    output_one_hot_vector = torch.where(torch.sigmoid(cls_output) > 0.99, 1., 0.)
    
    label = decode_lbl(output_one_hot_vector)
    return output_one_hot_vector, label


if __name__=="__main__":
    ASPECT_DICT = {
        0: "giai_tri",
        1: "luu_tru",
        2: "nha_hang",
        3: "an_uong",
        4: "di_chuyen",
        5: "mua_sam"
    }
    num_classes = 30
    predictions = []
    device = torch.device('cpu')
    model = PhoBertSentimentClassification()
    # os.environ["CUDA_VISIBLE_DEVICES"]= "0,1,2,3"
    # if torch.cuda.device_count() >1:
    #     model = torch.nn.DataParallel(model,device_ids=[0,1,2,3]).cuda()

    model.to(device)
    model.load_state_dict(torch.load(f'model_weights\last_step.pth',map_location=torch.device('cpu')))
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast = False)
    test_df = pd.read_csv("./dataset/test_dataset.csv")
    labels = convert_labels_format(test_df)
    texts = test_df.clean_review.tolist()

    sample_text = "Bệnh_viện rất đẹp, nơi khám chữa bệnh uy_tín và chất_lượng"
    outputs = inference(sample_text, model, tokenizer, device)
    output_one_hot_vector, label = outputs
    print(output_one_hot_vector)

    # print(labels[0])
    # print(type(labels[0]))
    # for i, text in enumerate(texts):
    #     print(f"----Inferencing text number {i + 1}----")
    #     outputs = inference(text, model, tokenizer, device)
    #     output_one_hot_vector, label = outputs[0], outputs[1]
    #     standard_output = convert_output_format(output_one_hot_vector)
    #     predictions.append(standard_output)
    
    # f1_scores, r2_scores = [], []
    # aspect_f1, aspect_r2 = eval_metrics(0, predictions, labels)
    # # print(aspect_f1, aspect_r2)
    # for j in range(6):
    #     aspect_f1, aspect_r2 = eval_metrics(j, predictions, labels)
    #     print(f"F1 score and R2 score of aspect {ASPECT_DICT[j]}: {aspect_f1}, {aspect_r2}")
    #     f1_scores.append(aspect_f1)
    #     r2_scores.append(aspect_r2)
    # final_res = 1/6 * float(sum([a*b for a, b in zip(f1_scores, r2_scores)]))
    # print(f"Final metric: {final_res}") 
            