import numpy as np

cross = np.array([0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0]).reshape(4,4)

X_train = [cross]
Y_train = [1]

kernel = np.random.randn(3, 3)
w_dense = np.random.randn(4)

for epoch in range(10):
    for x, y in zip(X_train, Y_train):

        conv_out = np.zeros((2, 2))
        for i in range(2):
            for j in range(2):
                conv_out[i,j] = np.sum(x[i:i+3, j:j+3] * kernel)

        act = np.maximum(0, conv_out) #ReLu: turns -ve numbers to 0
        pred = 1 / (1 + np.exp(-(np.dot(act.flatten(), w_dense))))
        error = y - pred
        w_dense += 0.1 * error * act.flatten()

print("Activation Map:\n", np.round(act, 2))