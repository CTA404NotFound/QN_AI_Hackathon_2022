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

dataset = './dataset/public_final.csv'
df = pd.read_csv(dataset)
stop_word=[]
txt_file = open("./dataset/vietnamese-stopwords-dash.txt", "r")
file_content = txt_file.read()
content_list = file_content.split("\n")
stemmer = PorterStemmer()
vnp=VnCoreNLP("./vncorenlp/VnCoreNLP-1.1.1.jar",annotators="wseg,pos,parse")
dict_check = {}

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text

def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji].split(":")[0])

    return string

def remove_stopwords(text):
    text = [word for word in text if word not in content_list]
    return text

def stemming(text):

    text = [stemmer.stem(word) for word in text]
    return text

def word_tokenizer(text):
    word_segmented_text = vnp.tokenize(text)
    return word_segmented_text

def preprocessing(text):
    text = remove_url(text) 
    text = handle_emoji(text)
    text = text.lower() 
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'(ks)', 'khách sạn', text)
    # text = sc1(text)
    text = word_tokenizer(text)
    text = remove_stopwords(text)
    print(text)
    text = " ".join(text[0])

    return text

def process():

    df1 = df.drop(df[(df.giai_tri == 0) & (df.luu_tru == 0) & (df.nha_hang == 0) & (df.an_uong == 0) & (df.di_chuyen == 0) & (df.mua_sam == 0)].index)

    tqdm.pandas()

    df1['clean_review'] = df1['Review'].progress_map(preprocessing)
    df1.loc[df1.giai_tri ==5, 'giai_tri'] = 'very_postive'
    df1.loc[df1.luu_tru ==5, 'luu_tru'] = 'very_postive'
    df1.loc[df1.nha_hang ==5, 'nha_hang'] = 'very_postive'
    df1.loc[df1.an_uong ==5, 'an_uong'] = 'very_postive'
    df1.loc[df1.di_chuyen ==5, 'di_chuyen'] = 'very_postive'
    df1.loc[df1.mua_sam ==5, 'mua_sam'] = 'very_postive'


    df1.loc[df1.giai_tri ==4, 'giai_tri'] = 'postive'
    df1.loc[df1.luu_tru ==4, 'luu_tru'] = 'postive'
    df1.loc[df1.nha_hang ==4, 'nha_hang'] = 'postive'
    df1.loc[df1.an_uong ==4, 'an_uong'] = 'postive'
    df1.loc[df1.di_chuyen ==4, 'di_chuyen'] = 'postive'
    df1.loc[df1.mua_sam ==4, 'mua_sam'] = 'postive'

    df1.loc[df1.giai_tri ==3, 'giai_tri'] = 'normal'
    df1.loc[df1.luu_tru ==3, 'luu_tru'] = 'normal'
    df1.loc[df1.nha_hang ==3, 'nha_hang'] = 'normal'
    df1.loc[df1.an_uong ==3, 'an_uong'] = 'normal'
    df1.loc[df1.di_chuyen ==3, 'di_chuyen'] = 'normal'
    df1.loc[df1.mua_sam ==3, 'mua_sam'] = 'normal'

    df1.loc[df1.giai_tri ==2, 'giai_tri'] = 'negative'
    df1.loc[df1.luu_tru ==2, 'luu_tru'] = 'negative'
    df1.loc[df1.nha_hang ==2, 'nha_hang'] = 'negative'
    df1.loc[df1.an_uong ==2, 'an_uong'] = 'negative'
    df1.loc[df1.di_chuyen ==2, 'di_chuyen'] = 'negative'
    df1.loc[df1.mua_sam ==2, 'mua_sam'] = 'negative'

    df1.loc[df1.giai_tri ==1, 'giai_tri'] = 'very_negative'
    df1.loc[df1.luu_tru ==1, 'luu_tru'] = 'very_negative'
    df1.loc[df1.nha_hang ==1, 'nha_hang'] = 'very_negative'
    df1.loc[df1.an_uong ==1, 'an_uong'] = 'very_negative'
    df1.loc[df1.di_chuyen ==1, 'di_chuyen'] = 'very_negative'
    df1.loc[df1.mua_sam ==1, 'mua_sam'] = 'very_negative'

    labels=[]
    value = 0
    # temp = ""
    for i in range(len(a)):
        dict_check['giai_tri']=a[i]
        dict_check['luu_tru']=b[i]
        dict_check['nha_hang']=c[i]
        dict_check['an_uong']=d[i]
        dict_check['di_chuyen']=e[i]
        dict_check['mua_sam']=f[i]
        print(dict_check)
        for name, seq in dict_check.items():
            if(seq != 0):
                temp1 = "{"+name+"#"+seq+"},"
                temp+=temp1
        labels.append(temp)
        temp=''
        dict_check={}
        #print(names)
        # break

    for i in range(len(labels)):
        labels[i] = labels[i].rstrip(labels[i][-1])

    value = 0 
    df1['labels']=labels

    df1.to_csv('./dataset/clean_test_dataset.csv')

if __name__ == "__main__":
    process()