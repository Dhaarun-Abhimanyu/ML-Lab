import numpy as np
import matplotlib.pyplot as plt

X = np.array([500, 800, 1000, 1200, 1500]) / 1000
Y = np.array([150, 220, 300, 360, 450]) / 1000

w, b = 0.0, 0.0
lrate = 0.01
epochs = 1000

for epoch in range(epochs):
    Y_pred = w*X + b
    loss = np.mean((Y - Y_pred)**2) #MSE

    dw = -2 * np.mean(X*(Y-Y_pred))
    db = -2 * np.mean(Y-Y_pred)

    w -= lrate*dw
    b -= lrate*db

    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.4f}")

test_x = 1100 / 1000
pred_price = (w * test_x + b) * 1000
print(f"Predicted price for 1100 sq.feet: {pred_price:.2f}k")

plt.scatter(X*1000, Y*1000, color='red', label='Data')
plt.plot(X*1000, (w*X+b)*1000, color='blue', label='Regression')
plt.legend()
plt.show()