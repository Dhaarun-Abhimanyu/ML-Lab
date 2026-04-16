import tensorflow as tf

X = tf.constant([[[1,0,1,0], [1,1,1,0], [1,0,1,1]], [[0,1,1,1], [1,1,0,1], [1,1,1,1]], 
                 [[0,0,0,1], [0,1,0,0], [0,0,1,0]], [[1,0,0,0], [0,0,1,0], [0,1,0,0]]], dtype=tf.float32)
Y = tf.constant([[1], [1], [0], [0]], dtype=tf.float32)

for lr in [0.001, 0.01]:
    inp = tf.keras.layers.Input(shape=(3,4))
    x = inp + tf.keras.layers.Embedding(3,4)(tf.range(3))

    attn = tf.keras.layers.MultiHeadAttention(num_heads=2, key_dim=4)(x,x)
    x1 = tf.keras.layers.LayerNormalization()(inp + attn)

    ffn = tf.keras.layers.Dense(4)(tf.keras.layers.Dense(8, activation='relu')(x1))
    enc_out = tf.keras.layers.LayerNormalization()(x1 + ffn)

    pool = tf.keras.layers.GlobalAveragePooling1D()(enc_out)
    out = tf.keras.layers.Dense(1, activation='sigmoid')(pool)

    model = tf.keras.Model(inp, out)
    model.compile(optimizer=tf.keras.optimizers.Adam(lr), loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, Y, epochs=10, verbose=0)

    acc = model.evaluate(X, Y, verbose=0)[1]
    print(f"LR {lr} - Final Accuracy: {acc * 100}%")

new_review = tf.ones((1, 3, 4)) 
pred = model.predict(new_review, verbose=0)[0][0]
print(f"New Review Prediction: {'Positive' if pred > 0.5 else 'Negative'} (Prob: {pred:.2f})")