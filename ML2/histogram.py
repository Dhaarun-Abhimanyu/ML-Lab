import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

def plot_histogram(data, feature, bins=20, color='steelblue'):
    values = data[feature]
    
    values = values.replace([np.inf, -np.inf], np.nan).dropna()

    plt.figure(figsize=(8, 5))
    plt.hist(values, bins=bins, color=color, edgecolor='black')
    plt.title(f'Histogram of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


file_path = "warframe.csv" 
df = pd.read_csv(file_path)

percentage_columns = ['CritChance', 'StatusChance']
for col in percentage_columns:
    if df[col].dtype == object:
        df[col] = df[col].str.rstrip('%').astype(float) / 100

features_to_plot = [
    'TotalDamage',
    'CritChance',
    'CritMultiplier',
    'StatusChance',
    'FireRate',
    'Disposition',
]

for feature in features_to_plot:
    if feature in df.columns:
        plot_histogram(df, feature)
    else:
        print(f"Feature '{feature}' not found in dataset.")
