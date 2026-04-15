import numpy as np

X = np.array([[1,0,1], [0,1,1], [1,1,0]], dtype=float)

pos_enc = np.array([[0,0.1,0.2], [0.1,0.2,0.3],[0.2,0.3,0.4]])
X_pos = X + pos_enc

np.random.seed(42)
W_q, W_k, W_v = np.random.randn(3,3), np.random.randn(3,3), np.random.randn(3,3)

#attention scores
Q, K, V = X_pos @ W_q, X_pos @ W_k, X_pos @ W_v
scores = (Q @ K.T) / np.sqrt(3)

W = np.exp(scores - np.max(scores, axis=-1)) #softmax
W /= np.sum(scores, axis=-1)

attention_score = W @ V
print("Manual Attention Scores:\n", np.round(attention_score, 2))

def norm(x): return (x - np.mean(x, axis=-1)) / (np.std(x, axis=-1) + 1e-6)

#add and norm
norm1 = norm(X_pos + attention_score)

#Feed forward mlp with relu
W1, W2 = np.random.randn(3,4), np.random.randn(4,3)
ffn_out = np.maximum(0, norm1 @ W1) @ W2

# Add + Norm
encoder_out = norm(norm1 + ffn_out)
print("\nFinal encoder output:\n", np.round(encoder_out, 2))

W_pred = np.random.randn(3,3)
next_vec_raw = encoder_out[-1:] @ W_pred
next_vec = 1 / (1 + np.exp(-next_vec_raw))

print("\nPredicted next vector:\n", np.round(next_vec, 2))


