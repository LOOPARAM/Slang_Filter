import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#train데이터 생성
print("dddd")

data_1 = pd.read_table("./Data/Curse-detection-data/dataset.txt",error_bad_lines=False, sep='|')

df_1 = pd.DataFrame(data_1)

df_1['hate'] = df_1['hate'].astype(str)

df_1['hate'] = df_1['hate'].replace({'0': 'true', '1': 'false'})

data_2 = pd.read_table(
    "Data/korean-hate-speech/labeled/dev.tsv", error_bad_lines=False)

df_2 = pd.DataFrame(data_2)

df_2 = df_2[['text', 'hate']]

data_3 = pd.read_table(
    "Data/korean-hate-speech/labeled/train.tsv", error_bad_lines=False)

df_3 = pd.DataFrame(data_3)

df_3 = df_3[['text', 'hate']]

data_4 = pd.read_table("Data/nsmc/ratings_train.txt", error_bad_lines=False)

df_4 = pd.DataFrame(data_4)

df_4 = df_4[['text', 'hate']]

df_4['hate'] = df_4['hate'].astype(str)

df_4['hate'] = df_4['hate'].replace({'0': 'true', '1': 'false'})



df = pd.concat([df_1,df_2,df_3,df_4])

li = []

for a in range(0,len(df.index)):
    li.append(a)

df.index = li

df.to_csv("train.csv")

"""
#test데이터 생성
"""
data_5 = pd.read_table("Data/nsmc/ratings_test.txt", error_bad_lines=False)

df_5 = pd.DataFrame(data_5)

df_5 = df_5[['text', 'hate']]

df_5['hate'] = df_5['hate'].astype(str)

df_5['hate'] = df_5['hate'].replace({'0': 'true', '1': 'false'})

df_5.to_csv("test.csv")




print("d")
