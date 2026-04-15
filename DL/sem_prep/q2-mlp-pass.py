import numpy as np

def sigmoid(x) : return 1/(1+np.exp(-x))
def d_sigmoid(x): return x*(1-x)

X = np.array([[2,50], [4,60], [6,70], [8,80]])
X_max = np.max(X, axis=0)
X = X / X_max
Y = np.array([[0], [0], [1], [1]])

np.random.seed(42)
W1 = np.random.uniform(-1, 1, (2,3))
b1 = np.zeros((1,3))
W2 = np.random.uniform(-1, 1, (3, 1))
b2 = np.zeros((1,1))

lrate = 0.5
epochs = 50

for epoch in range(epochs):
    out_1 = sigmoid(np.dot(X, W1) + b1)
    out_2 = sigmoid(np.dot(out_1, W2) + b2)

    error = Y - out_2
    del2 = error * d_sigmoid(out_2)

    error_hidden = del2.dot(W2.T)
    del1 = error_hidden * d_sigmoid(out_1)

    W2 += out_1.T.dot(del2) * lrate
    b2 += np.sum(del2, axis=0)*lrate
    W1 += X.T.dot(del1) * lrate
    b1 += np.sum(del1, axis=0)*lrate


test_input = np.array([[5, 65]]) / X_max
output = sigmoid(np.dot(sigmoid(np.dot(test_input, W1)+b1), W2)+b2)

print(f"Prediction for 5 hours, 65 attendance: {output[0][0]:.4f}")