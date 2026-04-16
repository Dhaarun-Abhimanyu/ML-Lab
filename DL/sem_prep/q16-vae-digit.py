import tensorflow as tf

data = tf.constant([
    [1.,1.,1.,1., 1.,0.,0.,1., 1.,0.,0.,1., 1.,1.,1.,1.],
    [0.,1.,0.,0., 1.,1.,0.,0., 0.,1.,0.,0., 1.,1.,1.,0.],
    [1.,1.,1.,0., 0.,0.,1.,0., 1.,1.,1.,0., 0.,0.,1.,0.],
    [1.,1.,1.,1., 0.,0.,1.,0., 0.,1.,0.,0., 1.,1.,1.,1.]
])

class VAE(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.enc = tf.keras.layers.Dense(8, activation='relu')
        self.mu = tf.keras.layers.Dense(2)
        self.log_var = tf.keras.layers.Dense(2)
        self.dec = tf.keras.Sequential([
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(16, activation='sigmoid')
        ])

    def call(self, x):
        h = self.enc(x)
        m, v = self.mu(h), self.log_var(h)

        z = m + tf.exp(0.5*v) * tf.random.normal(tf.shape(m))
        return self.dec(z), m, v
    
for lr in [0.001, 0.01]:
    vae = VAE()
    opt = tf.keras.optimizers.Adam(lr)
    for epoch in range(10):
        with tf.GradientTape() as tape:
            recon, m, v = vae(data)
            recon_loss = tf.reduce_sum(tf.square(data-recon))
            kl_loss = -0.5 * tf.reduce_sum(1 + v - tf.square(m) - tf.exp(v))
            loss = recon_loss + kl_loss

        opt.apply_gradients(zip(tape.gradient(loss, vae.trainable_variables), vae.trainable_variables))

    print(f"Generated Pattern in {lr} LR")
    print(tf.round(vae.dec(tf.constant([[0.5, -0.5]]))).numpy().reshape(4,4))