import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

X = tf.constant([[[1.0], [0.0], [1.0], [1.0], [0.0]]])

Y = tf.constant([[[0.0], [1.0], [1.0], [0.0], [1.0]]])

lrate = [0.001, 0.01]

for lr in lrate:
    print("Training with learning rate: ",lr)

    inputs = layers.Input(shape=(5,1))
    positions = tf.range(start=0, limit=5, delta=1)
    pos_encoding = layers.Embedding(input_dim=5, output_dim=1)(positions)

    x = inputs + pos_encoding
    attention_out = layers.MultiHeadAttention(num_heads=1, key_dim=1)(x,x)
    outputs = layers.Dense(1, activation='sigmoid')(attention_out)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr), loss='mse')

    model.fit(X, Y, epochs=10, verbose=0)

    preq_seq = model.predict(X, verbose=0)
    next_pixel_prob = preq_seq[0][-1][0]

    print(preq_seq)
    print(f"Predicted probability: {next_pixel_prob:.4f}")
    print(f"Predicted pixel: {int(np.round(next_pixel_prob))}")