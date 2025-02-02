import numpy as np
arr = np.array([1,2,0,0,4,0])
index = np.arange(arr.size)
print(index[arr>0])