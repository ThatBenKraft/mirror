import numpy as np

test = np.array([[0, 1], [0, 1]])

print(f"Array: {test}")

mask = test == 0

print(f"Mask: {mask}")

filled = np.array([[3, 3], [3, 3]])

filled[mask] = test[mask]

print(f"Array: {filled}")
