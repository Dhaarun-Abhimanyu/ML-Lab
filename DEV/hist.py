import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("move-data.csv")

df['Accuracy'] = pd.to_numeric(df['Accuracy'], errors='coerce')
df = df.dropna(subset=['Accuracy'])

plt.hist(df['Accuracy'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribution of Move Accuracy')
plt.xlabel('Accuracy')
plt.ylabel('Number of Moves')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()