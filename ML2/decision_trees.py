import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, KFold
from collections import Counter
import matplotlib.pyplot as plt

def entropy(y):
    counts = np.bincount(y)
    probs = counts[counts > 0] / len(y)
    return -np.sum(probs * np.log2(probs))

def gini(y):
    counts = np.bincount(y)
    probs = counts / len(y)
    return 1 - np.sum(probs**2)

def information_gain(X_col, y, criterion):
    if criterion == "gini":
        impurity = gini
    else:
        impurity = entropy
    parent = impurity(y)
    vals, counts = np.unique(X_col, return_counts=True)
    weighted = sum((counts[i] / len(y)) * impurity(y[X_col == v]) for i, v in enumerate(vals))
    return parent - weighted

def gain_ratio(X_col, y):
    ig = information_gain(X_col, y, "entropy")
    vals, counts = np.unique(X_col, return_counts=True)
    split_info = -np.sum((counts / len(y)) * np.log2(counts / len(y)))
    return ig / split_info if split_info != 0 else 0

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, criterion="information_gain", max_depth=None, min_samples_split=2):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X, y):
        self.n_classes_ = len(set(y))
        self.n_features_ = X.shape[1]
        self.root = self._grow_tree(X, y)

    def _best_split(self, X, y):
        best_gain = -1
        split_idx, split_thr = None, None
        for idx in range(self.n_features_):
            thresholds = np.unique(X[:, idx])
            for thr in thresholds:
                left_idx = X[:, idx] <= thr
                right_idx = X[:, idx] > thr
                if sum(left_idx) == 0 or sum(right_idx) == 0:
                    continue
                if self.criterion == "information_gain":
                    gain = information_gain((X[:, idx] <= thr).astype(int), y, "entropy")
                elif self.criterion == "gini":
                    gain = information_gain((X[:, idx] <= thr).astype(int), y, "gini")
                else:
                    gain = gain_ratio((X[:, idx] <= thr).astype(int), y)
                if gain > best_gain:
                    best_gain = gain
                    split_idx = idx
                    split_thr = thr
        return split_idx, split_thr

    def _grow_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))
        if depth == self.max_depth or num_labels == 1 or num_samples < self.min_samples_split:
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value)
        idx, thr = self._best_split(X, y)
        if idx is None:
            leaf_value = Counter(y).most_common(1)[0][0]
            return Node(value=leaf_value)
        indices_left = X[:, idx] <= thr
        left = self._grow_tree(X[indices_left], y[indices_left], depth + 1)
        right = self._grow_tree(X[~indices_left], y[~indices_left], depth + 1)
        return Node(idx, thr, left, right)

    def predict(self, X):
        return [self._predict(inputs, self.root) for inputs in X]

    def _predict(self, inputs, node):
        if node.is_leaf():
            return node.value
        if inputs[node.feature] <= node.threshold:
            return self._predict(inputs, node.left)
        return self._predict(inputs, node.right)

def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)

iris = load_iris()
X, y = iris.data, iris.target
criteria = ["information_gain", "gain_ratio", "gini"]

for crit in criteria:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = DecisionTree(criterion=crit, max_depth=5)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(f"{crit}: {accuracy(y_test, preds):.3f}")

kf = KFold(n_splits=5, shuffle=True, random_state=42)
depths = range(1, 11)
avg_acc = []
for d in depths:
    acc = []
    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        clf = DecisionTree(criterion="information_gain", max_depth=d)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_val)
        acc.append(accuracy(y_val, preds))
    avg_acc.append(np.mean(acc))

plt.plot(depths, avg_acc, marker='o')
plt.xlabel("Max Depth (Pruning Aggressiveness)")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Pruning")
plt.show()
