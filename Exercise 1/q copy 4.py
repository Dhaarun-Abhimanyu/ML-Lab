import numpy as np
arr = np.arange(1, 11)
odd_numbers = arr[arr % 2 != 0]
print(odd_numbers)