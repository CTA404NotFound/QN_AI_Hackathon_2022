import pandas as pd

from preprocess_dataset import preprocessing

SENTI_DICT = {
    1: "very_negative",
    2: "negative",
    3: "neutral",
    4: "positive",
    5: "very_positive"
}

sentiment_dict = {
        "0": 0,
        "very_negative": 1,
        "negative": 2,
        "normal": 3,
        "postive": 4,
        "very_postive": 5
    }

def process_labels_csv(data_frame):
    labels_lst = []
    for i in range(len(data_frame)):
        sample_labels = []
        for col in data_frame.columns.values[1:7]:
            if data_frame[col][i] != 0:
                polarity = data_frame[col][i]
                label = f"{col}#{SENTI_DICT[polarity]}"
                sample_labels.append(f"{{{label}}}")
                label_str = ", ".join([ele for ele in sample_labels])
        
        labels_lst.append(label_str)
    data_frame["label"] = labels_lst
    return data_frame

def convert_labels_format(data_frame):
    labels_format = []
    aspects = ["giai_tri", "luu_tru", "nha_hang", "an_uong", "di_chuyen", "mua_sam"]
    for i in range(len(data_frame)):
        labels_arr = []
        for aspect in aspects:
            labels_arr.append(sentiment_dict[data_frame[aspect][i]])
        labels_format.append(labels_arr) 

    return labels_format
    

if __name__ == '__main__':
    # df_train = pd.read_csv("./dataset/train_v1.csv")
    # df_test = pd.read_csv("./dataset/test_v1.csv")
    # data = pd.read_csv("./dataset/data_final_problem2.csv")
    # data = process_labels_csv(data)
    
    # train_raw_reviews = data.Review.tolist()
    # train_clean_reviews = [preprocessing(review) for review in train_raw_reviews]
    
    test_df = pd.read_csv("./dataset/test_dataset.csv")
    labels_format = convert_labels_format(test_df)
    print(type(labels_format))
    
    # test_df.to_csv("./dataset/clean_test_dataset_v2.csv")
    