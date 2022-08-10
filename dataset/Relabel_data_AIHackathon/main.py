import pandas as pd

file = pd.read_csv("data_final_problem2.csv")

f = file.copy()

#Define csv to utf8 for vietnamese
f.to_csv("./data_final_pro_2.csv", encoding='utf-8-sig')