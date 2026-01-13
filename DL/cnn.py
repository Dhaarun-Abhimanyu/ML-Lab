import numpy as np
from tensorflow.keras.datasets import mnist


# ---------- Load MNIST ----------
(X_train, y_train), _ = mnist.load_data()
X_train = X_train[:1000] / 255.0
y_train = y_train[:1000]


# ---------- CNN Functions ----------

def conv2d(image, kernel, stride=1):
    h, w = image.shape
    kh, kw = kernel.shape

    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = image[
                i*stride : i*stride + kh,
                j*stride : j*stride + kw
            ]
            output[i, j] = np.sum(region * kernel)

    return output


def relu(x):
    return np.maximum(0, x)


def max_pool(image, size=2, stride=2):
    h, w = image.shape
    out_h = (h - size) // stride + 1
    out_w = (w - size) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = image[
                i*stride : i*stride + size,
                j*stride : j*stride + size
            ]
            output[i, j] = np.max(region)

    return output


def conv_layer(image, kernels):
    feature_maps = []
    for k in kernels:
        fm = conv2d(image, k)
        fm = relu(fm)
        feature_maps.append(fm)
    return np.array(feature_maps)


def flatten(x):
    return x.reshape(-1)


def dense(x, W, b):
    return np.dot(x, W) + b


def softmax(x):
    exp = np.exp(x - np.max(x))
    return exp / np.sum(exp)


# ---------- CNN Forward Pass ----------

kernels = np.random.randn(8, 3, 3)      # 8 convolution filters
W = np.random.randn(1352, 10)           # FC weights
b = np.zeros(10)

x = X_train[0]                          # one MNIST image

x = conv_layer(x, kernels)              # Conv + ReLU
x = np.array([max_pool(fm) for fm in x])# Pooling
x = flatten(x)                          # Flatten
logits = dense(x, W, b)                 # Fully connected
probs = softmax(logits)                 # Softmax

prediction = np.argmax(probs)

print("Predicted:", prediction)
print("Actual:   ", y_train[0])
