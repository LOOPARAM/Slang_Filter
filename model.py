import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from konlpy.tag import Okt

data = pd.read_csv("train.csv")

t_df = pd.DataFrame(data)

t_df = t_df[['text', 'hate']]

# print(t_df['text'])

t_df['ko_text'] = t_df['text'].str.replace(
    pat=r'[^ ㄱ-ㅣ가-힣]+', repl=r'', regex=True)

okt = Okt()


print(okt.pos("동해물과 백두산이 마르고 닳도록"))

print(t_df)