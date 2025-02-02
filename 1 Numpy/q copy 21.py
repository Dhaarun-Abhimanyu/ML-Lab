import numpy as np
matrix = np.array([[1,2,3,4,5],[6,7,8,9,10]])
row_mean = np.mean(matrix, axis=0)
print(row_mean)