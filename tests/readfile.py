from plantcv import plantcv as pcv
import numpy as np
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
    
    
    if selection == "Standard Normal Variate":
        snvData = snv(data)
        return snvData
        
    elif selection == "Multiplicative Scatter Correction":
        mscData = msc (data)
        return mscData
        
    elif selection == "Savitzky-Golay (first)":
        w = 5
        p = 1
        sgoneData= savgol_filter(data, w, polyorder = p, deriv=0)
        return sgoneData
       
    elif selection == "Savitzky-Golay (second)":
        w = 5
        p = 1
        sgtwoData = savgol_filter(data, w, polyorder = p, deriv=2)
        return sgtwoData
        
    elif selection == "Normalization":
        X_one_column = data.reshape([-1,1])
        scaler = MinMaxScaler()
        result_one_column = scaler.fit_transform(X_one_column)
        result = result_one_column.reshape(data.shape)
        return result
    elif selection == "None (pass)":
        return data
    
    
    
def snv(input_data):
    # """
    #     :snv: A correction technique which is done on each
    #     individual spectrum, a reference spectrum is not
    #     required
    #     :param input_data: Array of spectral data
    #     :type input_data: DataFrame
        
    #     :returns: data_snv (ndarray): Scatter corrected spectra
    # """

    input_data = np.asarray(input_data)
    
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
    eps = np.finfo(np.float32).eps
    input_data = np.array(input_data, dtype=np.float64)
    ref = []
    sampleCount = int(len(input_data))

    # mean centre correction
    for i in range(input_data.shape[0]):
        input_data[i,:] -= input_data[i,:].mean()
    
    # Get the reference spectrum. If not given, estimate it from the mean
    # Define a new array and populate it with the corrected data    
    data_msc = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        for j in range(0, sampleCount, 10):
            ref.append(np.mean(input_data[j:j+10], axis=0))
            # Run regression
            fit = np.polyfit(ref[i], input_data[i,:], 1, full=True)
            # Apply correction
            data_msc[i,:] = (input_data[i,:] - fit[0][1]) / fit[0][0]
    
    return (data_msc)