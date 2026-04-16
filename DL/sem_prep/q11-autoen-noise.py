import tensorflow as tf
import numpy as np

clean_img = tf.constant([[1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]])
noisy_img = tf.constant([[1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]])
lrate = [0.001, 0.01]

for lr in lrate:
    print(f"Training with learning rate: {lr}")

    autoencoder = tf.keras.Sequential([
        tf.keras.layers.Dense(4, activation='relu', input_shape=(9,)),
        tf.keras.layers.Dense(9, activation='sigmoid')
    ])
    autoencoder.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr), loss='mse')

    history = autoencoder.fit(noisy_img, clean_img, epochs=10, verbose=0)

    initial_loss = history.history['loss'][0]
    final_loss = history.history['loss'][-1]
    loss_diff = initial_loss - final_loss
    
    print(f"Initial Loss (Epoch 1):  {initial_loss:.4f}")
    print(f"Final Loss (Epoch 10):   {final_loss:.4f}")
    print(f"Loss Difference:         {loss_diff:.4f}")

    denoised_raw = autoencoder.predict(noisy_img, verbose=0)
    denoised_rounded = np.round(denoised_raw).reshape(3,3)

    print("\nTarget cleaned image:")
    print(clean_img.numpy().reshape(3,3))
    print("\nActual Denoised Output:")
    print(denoised_rounded)