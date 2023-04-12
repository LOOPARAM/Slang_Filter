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

noun_extractor = LRNounExtractor()




print(t_df)