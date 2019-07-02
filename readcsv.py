# -*- coding: utf-8 -*-
import pandas as pd
from pprint import pprint

df = pd.read_csv('satire_tone_data.csv', sep='\t')
# pprint(df)
df.to_csv('satire.csv')
