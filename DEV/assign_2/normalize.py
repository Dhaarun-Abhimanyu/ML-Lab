import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("move-data.csv")
df[['Power', 'Accuracy']] = df[['Power', 'Accuracy']].apply(pd.to_numeric, errors='coerce')
scaler = MinMaxScaler()
df[['Power_Norm', 'Accuracy_Norm']] = scaler.fit_transform(df[['Power', 'Accuracy']])
print(df[['Power_Norm', 'Accuracy_Norm']].head())
