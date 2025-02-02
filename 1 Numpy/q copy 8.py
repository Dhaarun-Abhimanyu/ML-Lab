import numpy as np
matrix = np.random.random((3,3))
normalized_matrix = (matrix - np.mean(matrix)) / np.std(matrix)
print(normalized_matrix)