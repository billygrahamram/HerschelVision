import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk, ImageSequence
from utils.data_preprocessing_utils import *


def rgbValues(self):
    
        if ctk.get_appearance_mode() == 'Light':
            color = self.workAreaFrame.cget('fg_color')[0]
        else:
            color = self.workAreaFrame.cget('fg_color')[1]
            
        if color == 'gray86':
            R = 219
            G = 219
            B = 219
            hexCode = '#DBDBDB'
            return hexCode
        
        elif color == 'gray17':
            R = 43
            G = 43
            B = 43
            hexCode = '#2B2B2B'
            return hexCode

def wavelengthsSlider_event(mobj,value=150):
        print("data type; ", type(mobj))
        print("value",mobj)
        if mobj.raw_img_dir == None:
            pass
        else:
      
            value = int(float(value))
            single_band_img = single_band(mobj.spectral_array, int(value))
            mobj.tk_image = Image.fromarray(np.uint8(single_band_img))

            # updates the current slider value
            mobj.wavelengthSliderCurrentValueLabel.configure(text= "Current Wavelength: " + str(int(value)))
            
            # destroy the left frame for new image
            for widget in mobj.leftOriginalImgFrame.winfo_children():
                widget.destroy()
            
            openCanvas = ctk.CTkCanvas(mobj.leftOriginalImgFrame, 
                            bg = rgbValues(mobj),
                            bd = 0,
                            highlightthickness = 0,
                            relief = 'ridge')
        
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            openCanvas.pack(expand =True, fill='both')        
            openCanvas.bind('<Configure>',lambda event: full_image(event,mobj, mobj.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: getresizedImageCoordinates(event,mobj, canvas = openCanvas, image = mobj.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

def band1ScatterSlider_event(mobj,value=150):
        print("data type; ", type(mobj))
        print("value",mobj)
        if mobj.raw_img_dir== None:
            pass
        else:
            mobj.band1ScatterSliderCurrentValueLabel.configure(text = "First Band: " + str(int(value)))
            mobj.band1Value = int(value)
            mobj.scatterPlotFigax.clear()
            mobj.scatterPlotFigax.scatter(mobj.kmeansData[:, mobj.band1Value], 
                                          mobj.kmeansData[:, mobj.band2Value], 
                                          c=mobj.kmeanslabels, s=10)
            mobj.scatterPlotFigax.set_title("Scatter Plot")
            mobj.scatterPlotFigax.set_xlabel("Band 1")
            mobj.scatterPlotFigax.set_ylabel("Band 2")
            mobj.scatterPlotFigax.figure.canvas.draw()

def band2ScatterSlider_event(mobj,value=150):
        if mobj.raw_img_dir == None:
            pass
        else:
            mobj.band2ScatterSliderCurrentValueLabel.configure(text= "Second Band: " + str(int(value)))
            mobj.band2Value = int(value)
            mobj.scatterPlotFigax.clear()
            mobj.scatterPlotFigax.scatter(mobj.kmeansData[:, mobj.band1Value], 
                                          mobj.kmeansData[:, mobj.band2Value], 
                                          c=mobj.kmeanslabels, s=10)
            mobj.scatterPlotFigax.set_title("Scatter Plot")
            mobj.scatterPlotFigax.set_xlabel("Band 1")
            mobj.scatterPlotFigax.set_ylabel("Band 2")
            mobj.scatterPlotFigax.figure.canvas.draw()

def full_image(event,mobj, tk_image, canvas):
        
        # this function takes in a image and calculates it's dimension and the window dimension
        # and then makes sure that the image is fit to the window frame.
       
        canvas_ratio = event.width / event.height
        img_ratio = tk_image.size[0]/tk_image.size[1]
        
        if canvas_ratio > img_ratio: 
            height = int(event.height)
            width = int(height * img_ratio)
        else: 
            width = int(event.width)
            height = int(width/img_ratio)
            
            
        resized_image = tk_image.resize((width, height))
        mobj.resized_tk = ImageTk.PhotoImage(resized_image)
        # resized_tk = ImageTk.PhotoImage(resized_image)
        canvas.create_image(
            int(event.width/2), 
            int(event.height/2), 
            anchor = 'center',
            image=mobj.resized_tk)
        canvas.image = mobj.resized_tk


def getresizedImageCoordinates(event,mobj, canvas, image):
    
    
        # The event object contains the x and y coordinates of the mouse click
        x, y = int(event.x), int(event.y)
        
        # Calculate the size of the borders
        border_x = (canvas.winfo_width() - mobj.resized_tk.width()) / 2
        border_y = (canvas.winfo_height() - mobj.resized_tk.height()) / 2
        
        if border_x == 0:
            if y <= int(border_y):
                pass
            elif y>= (int(border_y) + mobj.resized_tk.height()):
                pass
            elif int(border_y) <= y <= (int(border_y) + mobj.resized_tk.height()):
                imgX = x-int(border_x)
                imgY = y-int(border_y)
                
                x_scale_ratio = image.width / mobj.resized_tk.width()
                y_scale_ratio = image.height / mobj.resized_tk.height()
                
                scaled_imgX = round(imgX * x_scale_ratio)
                scaled_imgY = round(imgY * y_scale_ratio)
                wavelengthPlot(scaled_imgX, scaled_imgY)
                
        
        elif border_y == 0:
            if x <= int(border_x):
                pass
            elif x >= (int(border_x) + mobj.resized_tk.width()):
                pass
            elif int(border_x) <= x <= (int(border_x) + mobj.resized_tk.width()):
                imgX = x-int(border_x)
                imgY = y-int(border_y)
        
                
                x_scale_ratio = image.width / mobj.resized_tk.width()
                y_scale_ratio = image.height / mobj.resized_tk.height()
                
                scaled_imgX = round(imgX * x_scale_ratio)
                scaled_imgY = round(imgY * y_scale_ratio)
                wavelengthPlot(mobj,scaled_imgX, scaled_imgY)

def wavelengthPlot(mobj,scaled_imgX, scaled_imgY):
        print("***************************************")
        print(mobj.obj.default_properties)
        reflectance = mobj.spectral_array[int(scaled_imgY), int(scaled_imgX), :]
        mobj.wavelengthPlotFigax.clear()
        mobj.wavelengthPlotFigax.plot(np.arange(0, mobj.obj.noOfBandsEMR), reflectance)
        mobj.wavelengthPlotFigax.set_title("Wavelength Plot")
        mobj.wavelengthPlotFigax.set_xlabel("Wavelength")
        mobj.wavelengthPlotFigax.set_ylabel("Reflectance")
        mobj.wavelengthPlotFigCanvas.draw()