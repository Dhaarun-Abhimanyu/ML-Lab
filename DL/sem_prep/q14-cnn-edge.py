import numpy as np

kernel = np.array([[1,1],[0,0],[-1,-1]])
W = np.random.randn(2)
X = np.array([[10,10,10],[0,0,0],[-10,-10,-10]])
Y = [1.0]
epochs = 10

for epoch in range(epochs):
    feature_map = np.zeros((1,2))
    for i in range(1):
        for j in range(2):
            feature_map[i,j] = np.sum(X[i:i+3, j:j+2] * kernel)

    act = np.maximum(0, feature_map)
    flat = act.flatten()

    pred = 1 / (1 + np.exp(-np.dot(flat, W)))
    error = Y - pred
    W += error*0.01*flat

print("Feature map output:\n", feature_map)
print("Prediction: ", pred)
