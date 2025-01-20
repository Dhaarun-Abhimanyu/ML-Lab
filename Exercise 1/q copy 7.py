import numpy as np
arr = np.arange(10)
arr[arr%2==0] = -arr[arr%2==0]
print(arr)