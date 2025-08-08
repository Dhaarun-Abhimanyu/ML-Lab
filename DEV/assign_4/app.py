import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import seaborn as sns

df = pd.read_csv("move-data.csv")

positive_skew = np.random.exponential(scale=2, size=1000)
negative_skew = -np.random.exponential(scale=2, size=1000)
outliers_data = np.append(np.random.normal(50, 5, 100), [120, 130, 150])

plt.figure(figsize=(15, 4))
plt.subplot(1, 3, 1)
plt.hist(positive_skew, bins=30, color='skyblue', edgecolor='black')
plt.title('Positive Skew')
plt.subplot(1, 3, 2)
plt.hist(negative_skew, bins=30, color='lightgreen', edgecolor='black')
plt.title('Negative Skew')
plt.subplot(1, 3, 3)
plt.boxplot(outliers_data)
plt.title('Outliers Example')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.hist(df['Power'], bins=10, color='orange', edgecolor='black', label='Power')
plt.xlabel('Power')
plt.ylabel('Frequency')
plt.title('Power Distribution')
plt.legend()
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(10,4))
axs[0].hist(df['PP'], color='purple')
axs[0].set_title('PP Distribution')
axs[1].hist(df['Accuracy'], color='red')
axs[1].set_title('Accuracy Distribution')
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
plt.scatter(df['Power'], df['Accuracy'], color='teal')
plt.xlabel('Power')
plt.ylabel('Accuracy')
plt.title('Power vs Accuracy')
max_power_idx = df['Power'].idxmax()
plt.annotate(df.loc[max_power_idx, 'Name'],
             (df.loc[max_power_idx, 'Power'], df.loc[max_power_idx, 'Accuracy']),
             xytext=(df.loc[max_power_idx, 'Power']+5, df.loc[max_power_idx, 'Accuracy']+5),
             arrowprops=dict(facecolor='black', arrowstyle="->"))
plt.show()

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['PP'], df['Power'], df['Accuracy'], c='r', marker='o')
ax.set_xlabel('PP')
ax.set_ylabel('Power')
ax.set_zlabel('Accuracy')
ax.set_title('3D Plot of PP, Power, Accuracy')
plt.show()

plt.figure(figsize=(10, 6))
m = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=80,
            llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='lightyellow', lake_color='lightblue')
m.drawmapboundary(fill_color='lightblue')

lons = np.random.uniform(-180, 180, 10)
lats = np.random.uniform(-60, 80, 10)
x, y = m(lons, lats)
m.scatter(x, y, marker='o', color='red', zorder=5)
plt.title("Random Points on World Map")
plt.show()

plt.figure(figsize=(6,4))
sns.boxplot(x='Type', y='Power', data=df, palette='pastel')
plt.title('Power by Move Type')
plt.show()

sns.barplot(x='Category', y='Accuracy', data=df, palette='muted')
plt.title('Accuracy by Category')
plt.show()
