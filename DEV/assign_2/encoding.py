import pandas as pd

df = pd.read_csv("move-data.csv")
encoded_df = pd.get_dummies(df, columns=['Type', 'Category', 'Contest'])
print(encoded_df.head())
