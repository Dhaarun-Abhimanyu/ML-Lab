import numpy as np
arr = np.arange(1, 10)
arr[arr % 2 != 0] = -1
print(arr)