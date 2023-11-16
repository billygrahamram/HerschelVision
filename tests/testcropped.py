import numpy as np
import matplotlib.pyplot as plt

# # Load your 3D numpy array
# # For the purpose of this example, let's create a random 3D array
# array_3d = np.random.rand(100, 100, 224)

# Specify the directory path
dir_path = '/Users/billygrahamram/Downloads/output/image4.npy'

# Load the 3D numpy array from the file
array_3d = np.load(dir_path)
print(array_3d.shape)



# Select the 50th channel
channel_50 = array_3d[:, :, 50]

# Display the image
plt.imshow(channel_50, cmap='gray')
plt.show()
