import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7])

print(arr[1:5])

print(arr[4:])

print(arr[:4])

print(arr[-3:-1])

print(arr[1:5:2])

print(arr[::2])

#Slicing 2-d array

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print(arr[1, 1:4])
#From the second element, slice elements from index 1 to index 4 (not included) 
