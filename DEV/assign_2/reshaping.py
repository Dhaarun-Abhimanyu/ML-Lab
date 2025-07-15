import pandas as pd

df = pd.read_csv("move-data.csv")
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')
df['Accuracy'] = pd.to_numeric(df['Accuracy'], errors='coerce')
reshaped = pd.melt(df, id_vars=['Name', 'Type'], value_vars=['Power', 'Accuracy', 'PP'], var_name='Stat', value_name='Value')
print(reshaped.head())
