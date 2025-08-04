import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("warframe.csv")

for col in data.columns:
    if data[col].dtype == object:
        data[col] = data[col].replace('inf', np.inf)

numerical_cols = data.select_dtypes(include=[np.number]).columns

for col in numerical_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

X = data[numerical_cols].copy()

X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(X.median(), inplace=True)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
y_pred = lof.fit_predict(X_scaled)
scores = -lof.negative_outlier_factor_

data['LOF_Score'] = scores
data['Outlier'] = y_pred == -1

sns.scatterplot(x=data['BaseDamage'], y=data['TotalDamage'], hue=data['Outlier'], palette={False: 'blue', True: 'red'})
plt.title('LOF Outlier Detection on Warframe Dataset')
plt.xlabel('BaseDamage')
plt.ylabel('TotalDamage')
plt.show()

print(data.loc[data['Outlier'], ['Name', 'AttackName', 'BaseDamage', 'TotalDamage', 'LOF_Score']])
