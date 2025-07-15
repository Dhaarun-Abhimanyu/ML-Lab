import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("move-data.csv")
df[['Power', 'Accuracy']] = df[['Power', 'Accuracy']].apply(pd.to_numeric, errors='coerce')
scaler = StandardScaler()
df[['Power_Std', 'Accuracy_Std']] = scaler.fit_transform(df[['Power', 'Accuracy']])
print(df[['Power_Std', 'Accuracy_Std']].head())
