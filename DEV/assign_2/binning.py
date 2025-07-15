import pandas as pd

df = pd.read_csv("move-data.csv")
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
bins = [0, 40, 70, 100, 150]
labels = ['Low', 'Medium', 'High', 'Very High']
df['Power_Level'] = pd.cut(df['Power'], bins=bins, labels=labels)
print(df[['Power', 'Power_Level']].head())
