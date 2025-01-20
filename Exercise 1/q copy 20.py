import numpy as np
arr = np.array([2, 5, 8, 10, 12, 15])
count_within_range = np.sum(arr[(arr >= 2) & (arr <= 12)])
print(count_within_range)