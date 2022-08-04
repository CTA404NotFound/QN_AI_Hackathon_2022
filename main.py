import emoji
import pandas as pd
import re

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


if __name__=="__main__":
    remove_symbol_data(path_train,col)
   





    
            