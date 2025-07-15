import pandas as pd
import numpy as np

df = pd.read_csv("move-data.csv")
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
df['Log_Power'] = np.log1p(df['Power'])
print(df[['Power', 'Log_Power']].head())
