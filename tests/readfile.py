from plantcv import plantcv as pcv
import numpy as np
from sklearn.cluster import KMeans

def readData(raw_img_dir):
    # reads the data and returns a 3 D numpy array
    spectral_array = pcv.readimage(raw_img_dir, mode = 'envi')
    spectral_array_data = spectral_array.array_data
    return spectral_array_data


def scatterPlotData(raw_img_dir):
    # reads the data and returns a 3 D numpy array
    spectral_array = pcv.readimage(raw_img_dir, mode = 'envi')
    spectral_array_data = spectral_array.array_data 
    unfoldedData = unfold(spectral_array_data)
    unfoldedData = unfoldedData[:500,:]
    # Create a KMeans instance with 2 clusters (since you have two types of spectral signatures)
    kmeans = KMeans(n_clusters=2, random_state=0, n_init=10)
    # Fit the model to your data
    kmeans.fit(unfoldedData)
    # The labels_ attribute holds the cluster labels for each data point
    labels = kmeans.labels_

    return labels, unfoldedData
    
def create_pseudo_rgb(arr, r_band, g_band, b_band):
    # Normalize the bands to the range [0, 255]
    r = (arr[:,:,r_band] - np.min(arr[:,:,r_band])) / (np.max(arr[:,:,r_band]) - np.min(arr[:,:,r_band])) * 255
    g = (arr[:,:,g_band] - np.min(arr[:,:,g_band])) / (np.max(arr[:,:,g_band]) - np.min(arr[:,:,g_band])) * 255
    b = (arr[:,:,b_band] - np.min(arr[:,:,b_band])) / (np.max(arr[:,:,b_band]) - np.min(arr[:,:,b_band])) * 255
    
    # Stack the bands along the last dimension
    rgb = np.dstack((r,g,b)).astype(np.uint8)
    
    return rgb


def single_band(arr, band):
    # Normalize the bands to the range [0, 255]
    band = (arr[:,:,band] - np.min(arr[:,:,band])) / (np.max(arr[:,:,band]) - np.min(arr[:,:,band])) * 255
    
    return band.astype(np.uint8)

def unfold(data):
    x,y,z = data.shape
    unfolded = data.reshape(x*y,z)
    for i in range(unfolded.shape[1]):
        col = unfolded[:,i]
        zero_indices = np.where(col == 0)[0]
        unfolded = np.delete(unfolded, zero_indices, axis=0)
        
    return unfolded
