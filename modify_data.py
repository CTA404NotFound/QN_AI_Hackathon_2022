import pandas as pd

from preprocess_dataset import preprocessing

SENTI_DICT = {
    1: "very_negative",
    2: "negative",
    3: "neutral",
    4: "positive",
    5: "very_positive"
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

if __name__ == '__main__':
    # df_train = pd.read_csv("./dataset/train_v1.csv")
    # df_test = pd.read_csv("./dataset/test_v1.csv")
    data = pd.read_csv("./dataset/data_final_problem2.csv")
    data = process_labels_csv(data)
    
    train_raw_reviews = data.Review.tolist()
    train_clean_reviews = [preprocessing(review) for review in train_raw_reviews]
    
    
    data["clean_review"] = train_clean_reviews
    data.to_csv("processed_data_v1.csv")
    