import tensorflow as tf

real_data = tf.constant([[1.,0.,1.,0.], [0.,1.,0.,1.]])
bce = tf.keras.losses.BinaryCrossentropy()

for lr in [0.001, 0.01]:

    G = tf.keras.Sequential(
        [tf.keras.layers.Dense(8, activation='relu'),
         tf.keras.layers.Dense(4, activation='sigmoid')
    ])
    D = tf.keras.Sequential(
        [tf.keras.layers.Dense(8, activation='relu'),
         tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    opt_G, opt_D = tf.keras.optimizers.Adam(lr), tf.keras.optimizers.Adam(lr)

    for epoch in range(10):
        noise = tf.random.normal((2,2))

        with tf.GradientTape() as tape_D, tf.GradientTape() as tape_G:
            fake_data = G(noise)
            loss_D = bce(tf.ones((2,1)), D(real_data)) + bce(tf.zeros((2,1)), D(fake_data))
            loss_G = bce(tf.ones((2,1)), D(fake_data))

        opt_D.apply_gradients(zip(tape_D.gradient(loss_D, D.trainable_weights), D.trainable_weights))
        opt_G.apply_gradients(zip(tape_G.gradient(loss_G, G.trainable_weights), G.trainable_weights))

    print(f"Generated pattern in LR={lr}: ", tf.round(G(tf.random.normal((1,2)))).numpy())