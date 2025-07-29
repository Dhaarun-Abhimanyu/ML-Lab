import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

def knn_density_estimate(data, query, k):
    data = np.array(data)
    query = np.array(query)
    dists = np.linalg.norm(data - query, axis=1)
    sorted_dists = np.sort(dists)
    rk = sorted_dists[k - 1]
    volume = (np.pi ** (data.shape[1] / 2)) / np.math.gamma(data.shape[1] / 2 + 1) * (rk ** data.shape[1])
    density = k / (len(data) * volume)
    return density

data_3d = np.array([(1, 1, 1), (2, 2, 2), (3, 3, 3), (6, 6, 6), (7, 7, 7)])
queries_3d = [np.array([2, 2, 2]), np.array([8, 8, 8])]
print("3D Density Estimates:")
for k in [1, 2, 3]:
    for q in queries_3d:
        print(f"k={k}, query={q}, density={knn_density_estimate(data_3d, q, k):.5f}")

data_2d = np.array([(1, 1), (2, 2), (3, 3), (5, 5)])
x_range = np.linspace(0, 6, 100)
y_range = np.linspace(0, 6, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        query = np.array([X[i, j], Y[i, j]])
        Z[i, j] = knn_density_estimate(data_2d, query, k=2)

plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.scatter(*zip(*data_2d), c='red', label='Data Points')
plt.title('2D k-NN Density Estimate (k=2)')
plt.colorbar(label='Density')
plt.legend()
plt.show()

data_1d = np.array([1, 2, 3, 6, 7]).reshape(-1, 1)
queries_1d = np.linspace(0, 8, 100).reshape(-1, 1)
densities_1d = [knn_density_estimate(data_1d, q, k=2) for q in queries_1d]

plt.plot(queries_1d, densities_1d, label='k=2')
plt.scatter(data_1d, [0]*len(data_1d), c='red', label='Data Points')
plt.title('1D k-NN Density Estimate')
plt.xlabel('x')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.show()
