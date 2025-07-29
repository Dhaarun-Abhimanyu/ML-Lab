import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import griddata

df = pd.read_csv("move-data.csv", usecols=range(9))

plt.figure(figsize=(8,5))
plt.plot(df['PP'], df['Power'], marker='o')
plt.title('Line Chart: PP vs Power')
plt.xlabel('PP')
plt.ylabel('Power')
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.scatter(df['Power'], df['Accuracy'], c='blue')
plt.title('Scatter Plot: Power vs Accuracy')
plt.xlabel('Power')
plt.ylabel('Accuracy')
plt.show()

plt.figure(figsize=(8,5))
plt.errorbar(df['PP'], df['Power'], yerr=(100 - df['Accuracy']), fmt='o', ecolor='red', capsize=5)
plt.title('Error Bars: Power with Accuracy error margin vs PP')
plt.xlabel('PP')
plt.ylabel('Power')
plt.show()

plt.figure(figsize=(8,5))
sns.kdeplot(df['Power'], fill=True)
plt.title('Density Plot of Power')
plt.xlabel('Power')
plt.show()

df = df.dropna(subset=['Power', 'Accuracy', 'PP'])

x = df['Power']
y = df['Accuracy']
z = df['PP']
xi = np.linspace(x.min(), x.max(), 100)
yi = np.linspace(y.min(), y.max(), 100)
xi, yi = np.meshgrid(xi, yi)
zi = griddata((x, y), z, (xi, yi), method='cubic')

plt.figure(figsize=(8,6))
contour = plt.contourf(xi, yi, zi, cmap='viridis')
plt.colorbar(contour, label='PP')
plt.title('Contour Plot: PP over Power and Accuracy')
plt.xlabel('Power')
plt.ylabel('Accuracy')
plt.show()
