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
    
    

def readData(raw_img_dir):
    # Get the file extension
    # this allows the user to use plantcv for .raw format images and np.load for npy images.
    # with npy images the program does not support reference calibration
    _, file_extension = os.path.splitext(raw_img_dir)

    
    if file_extension == '.raw':
        
        # Get the directory of the image folder
        dir_name = os.path.dirname(raw_img_dir)
        
        # Construct the file paths for the white and dark reference images
        white_ref_path = glob.glob(os.path.join(dir_name, 'WHITEREF*.raw'))[0]
        dark_ref_path = glob.glob(os.path.join(dir_name, 'DARKREF*.raw'))[0]
        
        # reads the data 
        raw_img        = pcv.readimage(raw_img_dir, mode='envi')
        white_ref      = pcv.readimage(white_ref_path, mode='envi')
        dark_ref       = pcv.readimage(dark_ref_path, mode='envi')
        
        calibrateddata = pcv.hyperspectral.calibrate(raw_data = raw_img, white_reference= white_ref, dark_reference= dark_ref)
        calibrateddata = calibrateddata.array_data
        
        return calibrateddata

    elif file_extension == '.npy':
        # Load the .npy file
        data = np.load(raw_img_dir)
        return data

    else:
        print(f"Unsupported file type: {file_extension}")
        return None



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

def create_pseudo_rgb(data_ref_array):
    blue_band = data_ref_array[..., 24]
    green_band = data_ref_array[..., 70]
    red_band = data_ref_array[..., 95]

    blue_band_normalized = cv2.normalize(blue_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    green_band_normalized = cv2.normalize(green_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    red_band_normalized = cv2.normalize(red_band, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    rgb = cv2.merge((blue_band_normalized, green_band_normalized, red_band_normalized))

    return rgb


def single_band(arr, band):
    # Normalize the bands to the range [0, 255]
    band = (arr[:,:,band] - np.min(arr[:,:,band])) / (np.max(arr[:,:,band]) - np.min(arr[:,:,band])) * 255
    
    image = band.astype(np.uint8)
    return image

def unfold(data):
    x, y, z = data.shape
    unfolded = data.reshape(x*y, z)
    zero_rows = np.where(np.all(unfolded == 0, axis=1))
    unfolded = np.delete(unfolded, zero_rows, axis=0)
    return unfolded

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
    

def normalize(data):
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)
    
def snv(input_data):

    data_snv = np.zeros_like(input_data)
    for i in range(data_snv.shape[0]):
        # Apply correction
        data_snv[i,:] = (input_data[i,:] - np.mean(input_data[i,:])) / np.std(input_data[i,:])
    
    return data_snv


def msc(input_data, reference=None):
    """
        :msc: Scatter Correction technique performed with mean of the sample data as the reference.
        :param input_data: Array of spectral data
        :type input_data: DataFrame
        :returns: data_msc (ndarray): Scatter corrected spectra data
    """
    # Convert input data to a numpy array
    input_data = np.array(input_data, dtype=np.float64)

    # Mean center correction
    input_data -= np.mean(input_data, axis=0)

    # Get the reference spectrum. If not given, estimate it from the mean    
    if reference is None:
        reference = np.mean(input_data, axis=0)

    # Define a new array and populate it with the corrected data    
    data_msc = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        # Fit a linear model (y = mx + b) to the data
        m, b = np.polyfit(reference, input_data[i,:], 1)
        # Apply correction
        data_msc[i,:] = (input_data[i,:] - b) / m

    return data_msc


def saveDatatoComputer(numpyarray, filename):
    if filename.endswith('.csv'):
        # Flatten the array and save it as a CSV
        # flat_array = numpyarray.flatten()
        df = pd.DataFrame(numpyarray)
        df.to_csv(filename, index=False)
    elif filename.endswith('.npy'):
        # Save the 3D array as a .npy file
        np.save(filename, numpyarray)
    elif filename.endswith('.txt'):
        # Flatten the array and save it as a txt
        # flat_array = numpyarray.flatten() # removed this line as it converts 2d array to 1d array
        df = pd.DataFrame(numpyarray)
        df.to_csv(filename, sep='\t', index=False)


def crop_3d_image(image, top_left, bottom_right):
    """
    Crop a 3D numpy image using the coordinates of the top left and bottom right corners.

    Parameters:
    image (numpy.ndarray): The 3D image to crop.
    top_left (tuple): The (x, y) coordinates of the top left corner.
    bottom_right (tuple): The (x, y) coordinates of the bottom right corner.

    Returns:
    numpy.ndarray: The cropped 3D image.
    """
    x1, y1 = top_left
    x2, y2 = bottom_right
    z1, z2 = 0, image.shape[2]  # Take the entire range along the z-axis
    croppedCube = image[y1:y2, x1:x2, z1:z2]
    return croppedCube


def kmeansSegmentation(array, clusters, bands):
    overlookBand = int(160)
    array = array[:, :, overlookBand:(overlookBand + bands)]
    X = array.reshape(-1, bands)
    kmeans = KMeans(n_clusters=clusters, n_init=10)
    kmeans.fit(X)
    segmented_img = kmeans.cluster_centers_[kmeans.labels_]
    segmented_img = segmented_img.reshape(array.shape)
    
    return segmented_img