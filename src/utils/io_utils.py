import glob
import os

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from plantcv import plantcv as pcv
from scipy.signal import savgol_filter
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


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