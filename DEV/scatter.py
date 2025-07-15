import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('move-data.csv')

df['Accuracy'] = pd.to_numeric(df['Accuracy'], errors='coerce')
df['Power'] = pd.to_numeric(df['Power'], errors='coerce')

df = df.dropna(subset=['Accuracy', 'Power'])

plt.scatter(df['Power'], df['Accuracy'], alpha=0.7, color='green', edgecolor='black')
plt.title('Move Accuracy vs Power')
plt.xlabel('Power')
plt.ylabel('Accuracy')
plt.grid(True)
plt.tight_layout()
plt.show()