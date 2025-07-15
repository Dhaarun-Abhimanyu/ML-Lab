import pandas as pd

df_moves = pd.read_csv("move-data.csv")
df_types = pd.DataFrame({
    'Type': ['Normal', 'Fire', 'Water', 'Electric'],
    'Effectiveness': [1.0, 2.0, 1.5, 2.0]
})

merged_df = pd.merge(df_moves, df_types, on='Type', how='left')
print(merged_df.head())