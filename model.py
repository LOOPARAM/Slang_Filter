import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from konlpy.tag import Okt
from soynlp.noun import LRNounExtractor

data = pd.read_csv("train.csv")

t_df = pd.DataFrame(data)

t_df = t_df[['text', 'hate']]

# print(t_df['text'])

t_df['ko_text'] = t_df['text'].str.replace(
    pat=r'[^ ㄱ-ㅣ가-힣]+', repl=r'', regex=True)

a = 0
for i in t_df['hate']:
    if i == True:
        a += 1
print(f"Hate : {a}")
print(f"NHate : {164192 - a}")

# t_df.to_csv("train2.csv")s