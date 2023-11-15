from plantcv import plantcv as pcv
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler

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


def preprocessing(selection, data):
    
    print(data.shape)
    if selection == "Standard Normal Variate":
        snvData = snv(data)
        return snvData
        
    elif selection == "Savitzky-Golay (first)":
        w = 13
        p = 2
        sgoneData= savgol_filter(data, w, polyorder = p, deriv=1)
        return sgoneData
       
    elif selection == "Savitzky-Golay (second)":
        w = 13
        p = 2
        sgtwoData = savgol_filter(data, w, polyorder = p, deriv=2)
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
    # """
    #     :snv: A correction technique which is done on each
    #     individual spectrum, a reference spectrum is not
    #     required
    #     :param input_data: Array of spectral data
    #     :type input_data: DataFrame
        
    #     :returns: data_snv (ndarray): Scatter corrected spectra
    # """
    # Define a new array and populate it with the corrected data  
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
    df = pd.DataFrame(numpyarray)
    if filename.endswith('.csv'):
        df.to_csv(filename, index=False)
    elif filename.endswith('.npy'):
        df.to_numpy().dump(filename)
    elif filename.endswith('.txt'):
        df.to_csv(filename, sep='\t', index=False)



