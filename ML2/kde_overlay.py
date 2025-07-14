import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("warframe.csv")

import numpy as np
df.replace([np.inf, -np.inf], np.nan, inplace=True)
for col in ['CritChance', 'StatusChance']:
    if df[col].dtype == object:
        df[col] = df[col].str.rstrip('%').astype(float) / 100

df = df[df['AttackName'] == 'Normal Attack']

plt.figure(figsize=(8, 5))
sns.histplot(df['BaseDamage'].dropna(), kde=True, bins=30, color='skyblue', edgecolor='black')
plt.title('Histogram + KDE of BaseDamage')
plt.xlabel('BaseDamage')
plt.ylabel('Density')
plt.grid(True)
plt.tight_layout()
plt.show()
