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