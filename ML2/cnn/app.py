import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

def condensed_nearest_neighbor(X, y):
    X, y = np.array(X), np.array(y)
    Z_X, Z_y = [X[0]], [y[0]]
    changed = True
    while changed:
        changed = False
        for i in range(1, len(X)):
            xi, yi = X[i], y[i]
            clf = KNeighborsClassifier(n_neighbors=1)
            clf.fit(Z_X, Z_y)
            if clf.predict([xi])[0] != yi:
                Z_X.append(xi)
                Z_y.append(yi)
                changed = True
    return np.array(Z_X), np.array(Z_y)

iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
y_pred_orig = knn.predict(X_test)
acc_orig = accuracy_score(y_test, y_pred_orig)

Z_X, Z_y = condensed_nearest_neighbor(X_train, y_train)
knn_cnn = KNeighborsClassifier(n_neighbors=1)
knn_cnn.fit(Z_X, Z_y)
y_pred_cnn = knn_cnn.predict(X_test)
acc_cnn = accuracy_score(y_test, y_pred_cnn)

print(f"Original 1-NN Accuracy: {acc_orig:.2f}")
print(f"CNN Reduced 1-NN Accuracy: {acc_cnn:.2f}")
print(f"Original training size: {len(X_train)}")
print(f"Reduced training size: {len(Z_X)}")

pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
Z_X_pca = pca.transform(Z_X)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
for label in np.unique(y_train):
    plt.scatter(X_train_pca[y_train == label, 0], X_train_pca[y_train == label, 1], label=iris.target_names[label], alpha=0.5)
plt.title('Original Dataset (PCA)')
plt.legend()

plt.subplot(1, 2, 2)
for label in np.unique(Z_y):
    plt.scatter(Z_X_pca[Z_y == label, 0], Z_X_pca[Z_y == label, 1], label=iris.target_names[label], alpha=0.8)
plt.title('Reduced Set (CNN, PCA)')
plt.legend()

plt.tight_layout()
plt.show()
