import spectral.io.envi as envi
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import cv2
import sys
import torch
import h5py


from plantcv import plantcv as pcv
from PIL import Image as im
from tkinter import filedialog
from skimage import data
from spectral import *




def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

def get_coordinates(event,x,y,flags,param):
    # global coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates =(x,y)
        print(f'x = {x},y = {y}')
        return coordinates
        
def applybinning(raw_data,value):
    if raw_data.shape[-1]!= 224:
        array=raw_data
        newsize=array.shape[-1]//value
        newshape=array.shape[:-1] + (newsize,value)
        
        binned_data =np.mean(array.reshape(newshape),axis=-1)

        return binned_data
    else:
        return raw_data
      
def calibrate(raw_data, white_reference, dark_reference):

    # Average dark reference over the first axis (repeated line scans) -> float64
    # Converts the input shape from (y, x, z) to (1, x, z)
    dark = np.mean(dark_reference, axis=0, keepdims=True)

    # Average white reference over the first axis (repeated line scans) -> float64
    # Converts the input shape from (y, x, z) to (1, x, z)
    white = np.mean(white_reference, axis=0, keepdims=True)

    # Convert the raw data to float64
    raw = raw_data.astype("float64")

    # Calibrate using reflectance = (raw data - dark reference) / (white reference - dark reference)
    # Note that dark and white are broadcast over each line (y) in raw
    cal = (raw - dark) / (white - dark)
    print('Image calibrated')

    # Clip the calibrated values to the range 0 - 1
    np.clip(cal, a_min=0, a_max=1, out=cal)
    return cal

def image(df, index):
    # image function to read image directory from the dataframe and read time return the array data.
    df=df;
    
    white = (pcv.readimage((df.iloc[index]['whiteref_image']), mode='envi')).array_data
    dark = (pcv.readimage((df.iloc[index]['darkref_image']), mode='envi')).array_data
    raw = (pcv.readimage((df.iloc[index]['raw_image']), mode='envi')).array_data
    
    calibrateData = calibrate(raw,white,dark)
    
    return calibrateData

def create_pseudo_rgb(arr, r_band, g_band, b_band):
    # Normalize the bands to the range [0, 255]
    r = (arr[:,:,r_band] - np.min(arr[:,:,r_band])) / (np.max(arr[:,:,r_band]) - np.min(arr[:,:,r_band])) * 255
    g = (arr[:,:,g_band] - np.min(arr[:,:,g_band])) / (np.max(arr[:,:,g_band]) - np.min(arr[:,:,g_band])) * 255
    b = (arr[:,:,b_band] - np.min(arr[:,:,b_band])) / (np.max(arr[:,:,b_band]) - np.min(arr[:,:,b_band])) * 255
    
    # Stack the bands along the last dimension
    rgb = np.dstack((r,g,b)).astype(np.uint8)
    
    return rgb