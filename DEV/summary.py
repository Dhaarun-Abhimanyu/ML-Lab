import pandas as pd

df = pd.read_csv("move-data.csv")

df['Accuracy'] = pd.to_numeric(df['Accuracy'], errors='coerce')
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')

df = df.dropna(subset=['Accuracy', 'Power'])

summary_stats = df[['Accuracy', 'Power']].agg(['mean', 'median', 'std'])
print("Summary Statistics:")
print(summary_stats)
