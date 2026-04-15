import tensorflow as tf
import numpy as np

X = tf.constant([[[1.0,1.0,1.0], [0.0,1.0,0.0], [1.0,1.0,1.0]]])
Y = tf.constant([[1.0]])
lrate = [0.01, 0.1]

for lr in lrate:
    print("Training with learning rate: ",lr)

    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(4, input_shape=(3,3), activation='relu'),
        tf.keras.layers.Dense(1,activation='sigmoid')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr), loss='binary_crossentropy')
    model.fit(X, Y, epochs=10, verbose=0)

    pred_prob = model.predict(X, verbose=0)[0][0]
    pred_class = int(np.round(pred_prob))

    print(f"Predicted probability: {pred_prob:.4f}")
    print(f"Predicted Class: {pred_class}")