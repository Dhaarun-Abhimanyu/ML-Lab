import pandas as pd

df = pd.read_csv("move-data.csv")
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
pivot_df = df.pivot(index='Name', columns='Category', values='Power')
print(pivot_df.head())
