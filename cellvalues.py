import pandas as pd
from random import randint

df = pd.read_csv('satire_tone_data_theme_text.csv')
print(list(df))

s = []
f = []
t = 'Analytical'

while(len(s)<15):
    x = randint(0, df.shape[0])
    if x not in s:
        if df.iloc[x]['sentences_count']>=25:
            if df.iloc[x]['class']=='Satire' and df.iloc[x]['sentences_tone_'+t]!=0:
                print(df.iloc[x]['sentences_tone_'+t]/df.iloc[x]['sentences_count'])
                s.append(x)

print()

while(len(f)<15):
    x = randint(0, df.shape[0])
    if x not in f:
        if df.iloc[x]['sentences_count']>=25:
            if df.iloc[x]['class']=='Fake' and df.iloc[x]['sentences_tone_'+t]!=0:
                print(df.iloc[x]['sentences_tone_'+t]/df.iloc[x]['sentences_count'])
                f.append(x)

print(s)
print(f)
