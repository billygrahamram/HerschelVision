from plantcv import plantcv as pcv
import numpy as np

def readData(raw_img_dir):
    # reads the data and returns a 3 D numpy array
    spectral_array = pcv.readimage(raw_img_dir, mode = 'envi')
    spectral_array_data = spectral_array.array_data
    return spectral_array_data
    

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



 