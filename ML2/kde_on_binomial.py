import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
data1 = np.random.normal(loc=20, scale=2, size=500)
data2 = np.random.normal(loc=35, scale=2, size=500)
bimodal_data = np.concatenate([data1, data2])

plt.figure(figsize=(8, 5))
sns.histplot(bimodal_data, kde=True, bins=40, color='lightcoral', edgecolor='black')
plt.title('Histogram + KDE of Bimodal Distribution')
plt.xlabel('Value')
plt.ylabel('Density')
plt.grid(True)
plt.tight_layout()
plt.show()
