import numpy as np

#Each element in an array is 0-d
arr = np.array(42) 
print(arr)
print(arr.ndim)

#1-d array
one_arr = np.array([1,2,3,4,5])
print(one_arr)
print(one_arr.ndim)

#2-d array 
two_arr = np.array([[1,2,3],[4,5,6]])
print(two_arr)
print(two_arr.ndim)

#3-d array
three_arr = np.array([ 
    [[1,2,3],[4,5,6]], 
    [[7,8,9], [10, 11, 12]]
    ])
print(three_arr)
print(three_arr.ndim)

# Creating arrays with ndmin
# In this array the innermost dimension (5th dim) has 4 elements,
# the 4th dim has 1 element that is the vector, 
# the 3rd dim has 1 element that is the matrix with the vector,
# the 2nd dim has 1 element that is 3D array and 
# 1st dim has 1 element that is a 4D array.

five_arr = np.array([1,2,3,4,5], ndmin=5)
print(five_arr)
#Output: [[[[[1 2 3 4 5]]]]]