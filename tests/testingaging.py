import numpy as np

# Create a numpy array of size 20,4
array = np.random.rand(5, 4)
 
unfoldedData = array[:, [2,3]]
print(array)
print(unfoldedData)
