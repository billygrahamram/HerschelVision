import numpy as np
from plantcv import plantcv as pcv
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler
from PIL import Image, ImageTk
import cv2
import os
import glob

def applybinning(raw_data, value):
    print(raw_data.shape[-1])
    if raw_data.shape[-1]!=224:
        array = raw_data
        newsize = array.shape[-1]//value
        newshape = array.shape[:-1] + (newsize,value)
        binned_data = np.mean(array.reshape(newshape),axis=-1)
        return(binned_data)
    else:
        return(raw_data)
    
def create_pseudo_rgb(data_ref_array):
    blue_band = data_ref_array[..., 24]
    green_band = data_ref_array[..., 70]
    red_band = data_ref_array[..., 95]

    blue_band_normalized = cv2.normalize(blue_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    green_band_normalized = cv2.normalize(green_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    red_band_normalized = cv2.normalize(red_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    rgb = cv2.merge((blue_band_normalized, green_band_normalized, red_band_normalized))
    rgb_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)

    return rgb_image

def scatterPlotData(raw_img_dir):
    
    _, file_extension = os.path.splitext(raw_img_dir)

    if file_extension == '.raw':
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

    elif file_extension == '.npy':
        # Load the .npy file
        data = np.load(raw_img_dir)
        data = unfold(data)
        data = data[:500,:]
        # Create a KMeans instance with 2 clusters (since you have two types of spectral signatures)
        kmeans = KMeans(n_clusters=2, random_state=0, n_init=10)
        # Fit the model to your data
        kmeans.fit(data)
        # The labels_ attribute holds the cluster labels for each data point
        labels = kmeans.labels_

        return labels, data

    else:
        print(f"Unsupported file type: {file_extension}")
        return None
    
def unfold(data):
    x, y, z = data.shape
    unfolded = data.reshape(x*y, z)
    zero_rows = np.where(np.all(unfolded == 0, axis=1))
    unfolded = np.delete(unfolded, zero_rows, axis=0)
    return unfolded

def single_band(arr, band):
    # Normalize the bands to the range [0, 255]
    band = (arr[:,:,band] - np.min(arr[:,:,band])) / (np.max(arr[:,:,band]) - np.min(arr[:,:,band])) * 255
    
    image = band.astype(np.uint8)
    return image

def preprocessing(selection, data, w, p):
    
    print(data.shape)
    if selection == "Standard Normal Variate":
        snvData = snv(data)
        return snvData
        
    elif selection == "Savitzky-Golay (first)":
 
        sgoneData= savgol_filter(data, window_length=w, polyorder = p, deriv=1)
        return sgoneData
       
    elif selection == "Savitzky-Golay (second)":
   
        sgtwoData = savgol_filter(data, window_length=w, polyorder = p, deriv=2)
        return sgtwoData
        
    elif selection == "Normalization":
        normalizedData = normalize(data)
        return normalizedData
    elif selection == "None (pass)":
        return data
    
def snv(input_data):

    data_snv = np.zeros_like(input_data)
    for i in range(data_snv.shape[0]):
        # Apply correction
        data_snv[i,:] = (input_data[i,:] - np.mean(input_data[i,:])) / np.std(input_data[i,:])
    
    return data_snv

def normalize(data):
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)