import numpy as np
arr = np.array([2,5,10,3,8])
arr = (arr - np.min(arr))/(np.max(arr) - np.min(arr))
print(arr)