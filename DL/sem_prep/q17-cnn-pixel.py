import numpy as np

X0 = np.array([1,1,1,1,1, 
               1,0,0,0,1, 
               1,0,0,0,1, 
               1,0,0,0,1, 
               1,1,1,1,1]).reshape(5, 5)

X1 = np.array([0,0,1,0,0, 
               0,1,1,0,0, 
               1,0,1,0,0, 
               0,0,1,0,0, 
               1,1,1,1,1]).reshape(5, 5)

X_data = [X0, X1]
Y_data = [0,1]

def cnn_forward(X, K, W):
    conv = np.array([[np.sum(X[i:i+3, j:j+3] * K) for j in range(3)] for i in range(3)])
    conv = np.maximum(0, conv)

    pool = np.array([[np.max(X[i:i+2, j:j+2]) for j in range(2)] for i in range(2)])

    flat = pool.flatten()
    pred = 1 / (1 + np.exp(-np.dot(flat, W)))
    return pred, flat

for lr in [0.01, 0.1]:
    print("Training with learning rate: ",lr)
    np.random.seed(42)
    K = np.random.randn(3, 3)
    W = np.random.randn(4)
    for epoch in range(10):
        for x,y in zip(X_data, Y_data):
            pred, flat = cnn_forward(x, K, W)
            error = y - pred
            W += error*flat*lr

    print(f"Target [0, 1] | Guessed [{cnn_forward(X0, K, W)[0]:.2f}, {cnn_forward(X1, K, W)[0]:.2f}]")

X_new = np.array([0,1,1,1,0, 
                  1,0,0,0,1, 
                  1,0,0,0,1, 
                  1,0,0,0,1, 
                  0,1,1,1,0]).reshape(5, 5)

pred_new, _ = cnn_forward(X_new, K, W)
print(f"\nNew Pattern Prediction: {pred_new:.4f} -> Class {int(np.round(pred_new))}")