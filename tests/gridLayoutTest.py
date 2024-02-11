#####################################################################################
## Author: Billy G. Ram
## Linkedin: https://www.linkedin.com/in/billygrahamram/
## Twitter: https://twitter.com/billygrahamram
## Github: https://github.com/billygrahamram
## This code solely belongs to Billy G. Ram and is currently NOT open sourced. 
#####################################################################################




################ ISSUES THAT NEED TO BE FIXED ###################
## 1. The wavelength and scatter sliders 1 and 2 do not update depending on the input data.
## They only supports 224 bands data read in and if the input data is more than 224 the readfile.py will
## apply binning to it, bringing it down to 224.

import os
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk, ImageSequence
import time, threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt


### herschelVision modules ####
from readfile import *
### herschelVision modules ####

from plantcv import plantcv as pcv
import numpy as np
import cv2


ctk.set_appearance_mode("light") # light, dark, system


def button_event():
    print("button pressed")
    

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("Herchel Vision: Hyperspectral Image Analysis")
        self.geometry("1600x900")
        self.minsize(700,700)
        self.resizable(width=True, height=True)

    
        # default values
        self.raw_img_dir = None
        self.Dataloaded = False
        
        #savePreProSetting
        self.SGWinSizePrePro = 13
        self.SGPolyOrderPrePro = 2
        
        #saveSegmentationSetting
        self.KclusterNoSegPrePro = 2
        self.KClusterThresPrePro = 2
        self.selectedSAMModel = 'ViT-B SAM Model'
        self.defaultSegmentationMethod = 'K means clustering'
        
        #savePseudoRGBSetting
        self.RedbandNoPseudoRGB = 50
        self.greenBandNoPseudoRGB = 100
        self.blueBandNoPseudoRGB = 150
        
        
        #saveEMRSetting
        self.noOfBandsEMR = 224
        self.firstBandEMR = 300
        self.lastBandEMR =  1000
        self.spectralResolution = 5
  
        # Empty the img_dir_record.txt file at startup. Opens and closes it, making the file empty.
        data_path_file = os.path.join('history', 'img_dir_record.txt')
        with open(data_path_file, 'w') as f:
            pass
        
        ## children to main window
        self.menuBarFrame = ctk.CTkFrame(self)
        self.workAreaFrame = ctk.CTkFrame(self)

        self.menuBarFrame.place(x=0, y=0, relwidth = 1, relheight = 0.05)
        self.workAreaFrame.place(rely = 0.05, y =0, relwidth =1, relheight =0.95)

        
        # opens the home window by default
        self.mainMenu()
        self.homeWindow()
    


    def mainMenu(self):
        ## children to menuBarFrame. Menu bar buttons
        self.FileOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Home","New","Open","Save","Export","Exit"], command=self.optionmenu_callback)
        self.FileOptionMenu.set("File")
        self.FileOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.EditOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        self.EditOptionMenu.set("Edit")
        self.EditOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.ToolsOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Cropping/Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        self.ToolsOptionMenu.set("Tools")
        self.ToolsOptionMenu.pack(side= 'left',padx=5, pady=5)

        self.AboutOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Updates","Version","About","References", "Contact us"], command=self.optionmenu_callback)
        self.AboutOptionMenu.set("About")
        self.AboutOptionMenu.pack(side= 'left',padx=5, pady=5)
       
    def homeWindow(self):
        # method to show the home window.
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()

        data_path_file = os.path.join('history', 'img_dir_record.txt') 

        
        ## children to workMenuFrame 
        self.leftOriginalImgFrame = ctk.CTkFrame(master = self.workAreaFrame)
        self.rightPlotsImgFrame   = ctk.CTkFrame(master = self.workAreaFrame)
        self.bottomSliderFrame    = ctk.CTkFrame(master = self.workAreaFrame)

        
        self.leftOriginalImgFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        self.rightPlotsImgFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        self.bottomSliderFrame.place(rely = 0.9, y = 0, relwidth = 1, relheight = 0.1)


        self.rightPlotsImgFrame.rowconfigure((0,1), weight = 1)
        self.rightPlotsImgFrame.columnconfigure((0), weight = 1)
        self.bottomSliderFrame.rowconfigure((0,1), weight = 1)
        self.bottomSliderFrame.columnconfigure((0,1,2,3), weight = 1)
        

        # if the img_dir_record is empty. show the welcome image
        if os.path.exists(data_path_file) and os.path.getsize(data_path_file) == 0:
            lightThemeImgPath = 'data/welcomeLight.png'
            darkThemeImgPath = 'data/welcomeDark.png'
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
            else:
                welcomeImg = Image.open(darkThemeImgPath)
                

            homeCanvas = ctk.CTkCanvas(self.leftOriginalImgFrame, 
                            bg = self.rgbValues(),
                            bd = 0,
                            highlightthickness=0,
                            relief='ridge')
            
            homeCanvas.pack( expand =True, fill='both')
            homeCanvas.bind('<Configure>',lambda event: self.full_image(event, welcomeImg, canvas=homeCanvas))
        
        elif os.path.exists(data_path_file) and os.path.getsize(data_path_file) > 0:
            with open(data_path_file, 'r') as f:
                self.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.leftOriginalImgFrame, 
                        bg = self.rgbValues(),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand =True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: self.getresizedImageCoordinates(event, canvas = homeCanvas, image = self.tk_image))

        
        #### wavelength plot ######
        self.wavelengthPlotFig, self.wavelengthPlotFigax = plt.subplots()
        self.wavelengthPlotFig.set_facecolor(self.rgbValues())
        self.wavelengthPlotFigax.set_facecolor(self.rgbValues())
        self.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.wavelengthPlotFigCanvas = FigureCanvasTkAgg(self.wavelengthPlotFig, master= self.rightPlotsImgFrame)
        self.wavelengthPlotFigCanvas.get_tk_widget().grid(row = 0, column = 0, sticky= 'nsew')

        #### scatter plot ######
        self.scatterPlotFig, self.scatterPlotFigax = plt.subplots()
        self.scatterPlotFig.set_facecolor(self.rgbValues())
        self.scatterPlotFigax.set_facecolor(self.rgbValues())
        self.scatterPlotFigax.set_title("Scatter Plot")
        self.scatterPlotFigax.set_xlabel("Band 1")
        self.scatterPlotFigax.set_ylabel("Band 2")
        self.scatterPlotFigCanvas = FigureCanvasTkAgg(self.scatterPlotFig, master= self.rightPlotsImgFrame)
        self.scatterPlotFigCanvas.get_tk_widget().grid(row= 1, column=0,  sticky='nsew')
        
        
        # wavelength slider
        self.wavelengthSliderCurrentValueLabel = ctk.CTkLabel(self.bottomSliderFrame, text = "", justify ="center")
        self.wavelengthSliderCurrentValueLabel.grid(row = 0, column = 0, columnspan = 2, padx = (100,5))
        self.wavelengthSlider = ctk.CTkSlider(self.bottomSliderFrame, from_ = 0, to = self.noOfBandsEMR-1, height = 20,command = self.wavelengthsSlider_event)
        self.wavelengthSlider.grid(row = 1, column = 0, columnspan=2, padx = (100,5))
        self.wavelengthsSlider_event(150)
        
        # band 1 slider
        self.band1ScatterSliderCurrentValueLabel = ctk.CTkLabel(self.bottomSliderFrame, text = "", justify ="center")
        self.band1ScatterSliderCurrentValueLabel.grid(row = 0, column =2, padx = (100,5))
        self.band1ScatterSlider = ctk.CTkSlider(self.bottomSliderFrame, from_ = 0, to = self.noOfBandsEMR-1, height = 20, command = self.band1ScatterSlider_event)
        self.band1ScatterSlider.grid(row =1, column =2, padx = (100,5))
        self.band1ScatterSlider_event(150)
        
        # band 2 slider
        self.band2ScatterSliderCurrentValueLabel = ctk.CTkLabel(self.bottomSliderFrame, text = "", justify ="center")
        self.band2ScatterSliderCurrentValueLabel.grid(row = 0, column =3, padx = (5,100))
        self.band2ScatterSlider = ctk.CTkSlider(self.bottomSliderFrame, from_ = 0, to = self.noOfBandsEMR-1, height = 20, command = self.band2ScatterSlider_event)
        self.band2ScatterSlider.grid(row =1, column=3, padx=(5,100))
        self.band2ScatterSlider_event(150)
        
        # set default values
        self.band1Value = 150
        self.band2Value = 150
        
    def optionmenu_callback(self,choice):
        ## method to select function to buttons in main menu.
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()
        elif choice == 'Preprocessing':
            self.preprocessingWindow()
        elif choice == 'Preferences':
            self.preferencesWindow()
        elif choice == 'Home':
            self.homeWindow()
        elif choice == 'Cropping/Segmentation':
            self.croppingWindow()

    def full_image(self,event, tk_image, canvas):
        
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
        self.resized_tk = ImageTk.PhotoImage(resized_image)
        # resized_tk = ImageTk.PhotoImage(resized_image)
        canvas.create_image(
            int(event.width/2), 
            int(event.height/2), 
            anchor = 'center',
            image=self.resized_tk)
        canvas.image = self.resized_tk
        
    def open(self):
        self.raw_img_dir = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = [("Raw Hyperspectral Image", "*.raw"),
                                                             ("Numpy Array", "*.npy")
                                                             ])
        
        # this makes sure that if the user selected an image and then
        # tried to open another image but cancelled the process the previous image is still displayed.
        if not self.raw_img_dir:  # Check if raw_img_dir is empty
            # Read the path from the img_dir_record.txt file
            with open(os.path.join('history', 'img_dir_record.txt'), 'r') as f:
                raw_img_dir = f.read().strip()
                self.raw_img_dir = raw_img_dir
                
        
        # Save the raw_img_dir to a text file in the history folder
        os.makedirs('history', exist_ok=True) #make sure the history folder exists. if not creates one.
        with open(os.path.join('history', 'img_dir_record.txt'), 'w') as f:
            f.write(self.raw_img_dir)
            
        ######################### RECENT FILES #################
        # first reads all the existing paths from the file into a list. 
        # It then checks if the current path already exists in the list. 
        # If it doesn’t, the path is added to the top of the list. 
        # Finally, all the paths are written back to the file. 
        # This ensures that the most recent path is always at the top and there are no duplicates.
        
        # Read the existing paths
        with open(os.path.join('history', 'recentFiles.txt'), 'r') as f:
            lines = f.read().splitlines()

        # If the path already exists in the file, remove it
        if self.raw_img_dir in lines:
            lines.remove(self.raw_img_dir)

        # Add the path to the top of the list
        lines.insert(0, self.raw_img_dir)

        # Only keep the 5 most recent paths
        lines = lines[:5]
        
        # Write the paths back to the file
        with open(os.path.join('history', 'recentFiles.txt'), 'w') as f:
            for line in lines:
                f.write(line + '\n')
                
        
        self.Dataloaded = False
        #using multithreading to show the loading dialog box while data is loading
        threading.Thread(target = self.loadData).start()
        
        self.dataLoadingScreen()  
        
    def loadData(self):
        self.loadDataText = 'Opening files...'
        self.currentData = readData(self.raw_img_dir)
        self.spectral_array = self.currentData.array_data
        self.spectral_array = applybinning(self.spectral_array,2)
        self.loadDataText = 'Loading data and creating plots...'
        self.kmeanslabels, self.kmeansData = scatterPlotData(self.raw_img_dir)
        self.loadDataText = 'Unfolding data...'
        self.unfoldedData = unfold(self.spectral_array)
        self.loadDataText = 'Finishing up...'
        self.wavelengthsSlider_event(value = 150)
        self.Dataloaded = True
        
    def dataLoadingScreen(self):
        loading_window = tk.Toplevel(self)
        loading_window.transient(self) 
        loading_window.title("Loading data")
        loading_window.geometry("500x200")
        loading_window.resizable(width=False, height=False)

        loading_window.grab_set()

        loading_window.attributes('-topmost', True)
        loading_window.after_idle(loading_window.attributes, '-topmost', False)
        
        self.loadDataLabel = ctk.CTkLabel(master=loading_window, text = self.loadDataText, justify = "center", font = ("Helvetica", 20))
        self.loadDataLabel.pack(side = 'top', expand = True, fill = 'x', pady =(10,0))
        
        # Create a progress bar
        progress = ctk.CTkProgressBar(loading_window, width = 150, height = 30, mode='indeterminate', orientation='horizontal')
        progress.pack(side = 'top',expand=True, fill='x', padx = 80, pady=(0,80))
        progress.start()
        
        def check_data_loaded():
            if self.Dataloaded:
                loading_window.destroy()
                
            else:
                self.loadDataLabel.configure(text=self.loadDataText)
                loading_window.after(50, check_data_loaded) #keep checking after 50ms
                
        check_data_loaded()
        
    def wavelengthsSlider_event(self, value):
        
        if self.raw_img_dir == None:
            pass
        else:
      
            value = int(float(value))

            
            single_band_img = single_band(self.spectral_array, int(value))
            self.tk_image = Image.fromarray(np.uint8(single_band_img))

            # updates the current slider value
            self.wavelengthSliderCurrentValueLabel.configure(text= "Current Wavelength: " + str(int(value)))
            
    
            # destroy the left frame for new image
            for widget in self.leftOriginalImgFrame.winfo_children():
                widget.destroy()
            
            openCanvas = ctk.CTkCanvas(self.leftOriginalImgFrame, 
                            bg = self.rgbValues(),
                            bd = 0,
                            highlightthickness = 0,
                            relief = 'ridge')
        
            
            openCanvas.pack(expand =True, fill='both')        
            openCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: self.getresizedImageCoordinates(event, canvas = openCanvas, image = self.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.

    def band1ScatterSlider_event(self, value):
        if self.raw_img_dir == None:
            pass
        else:
            self.band1ScatterSliderCurrentValueLabel.configure(text = "First Band: " + str(int(value)))
            self.band1Value = int(value)
            self.scatterPlotFigax.clear()
            self.scatterPlotFigax.scatter(self.kmeansData[:, self.band1Value], 
                                          self.kmeansData[:, self.band2Value], 
                                          c=self.kmeanslabels, s=10)
            self.scatterPlotFigax.set_title("Scatter Plot")
            self.scatterPlotFigax.set_xlabel("Band 1")
            self.scatterPlotFigax.set_ylabel("Band 2")
            self.scatterPlotFigax.figure.canvas.draw()
    
    def band2ScatterSlider_event(self, value):
        if self.raw_img_dir == None:
            pass
        else:
            self.band2ScatterSliderCurrentValueLabel.configure(text= "Second Band: " + str(int(value)))
            self.band2Value = int(value)
            self.scatterPlotFigax.clear()
            self.scatterPlotFigax.scatter(self.kmeansData[:, self.band1Value], 
                                          self.kmeansData[:, self.band2Value], 
                                          c=self.kmeanslabels, s=10)
            self.scatterPlotFigax.set_title("Scatter Plot")
            self.scatterPlotFigax.set_xlabel("Band 1")
            self.scatterPlotFigax.set_ylabel("Band 2")
            self.scatterPlotFigax.figure.canvas.draw()
  
    def getresizedImageCoordinates(self,event, canvas, image):
    
    
        # The event object contains the x and y coordinates of the mouse click
        x, y = int(event.x), int(event.y)
        
        # Calculate the size of the borders
        border_x = (canvas.winfo_width() - self.resized_tk.width()) / 2
        border_y = (canvas.winfo_height() - self.resized_tk.height()) / 2
        
        if border_x == 0:
            if y <= int(border_y):
                pass
            elif y>= (int(border_y) + self.resized_tk.height()):
                pass
            elif int(border_y) <= y <= (int(border_y) + self.resized_tk.height()):
                imgX = x-int(border_x)
                imgY = y-int(border_y)
                
                x_scale_ratio = image.width / self.resized_tk.width()
                y_scale_ratio = image.height / self.resized_tk.height()
                
                scaled_imgX = round(imgX * x_scale_ratio)
                scaled_imgY = round(imgY * y_scale_ratio)
                self.wavelengthPlot(scaled_imgX, scaled_imgY)
                
        
        elif border_y == 0:
            if x <= int(border_x):
                pass
            elif x >= (int(border_x) + self.resized_tk.width()):
                pass
            elif int(border_x) <= x <= (int(border_x) + self.resized_tk.width()):
                imgX = x-int(border_x)
                imgY = y-int(border_y)
        
                
                x_scale_ratio = image.width / self.resized_tk.width()
                y_scale_ratio = image.height / self.resized_tk.height()
                
                scaled_imgX = round(imgX * x_scale_ratio)
                scaled_imgY = round(imgY * y_scale_ratio)
                self.wavelengthPlot(scaled_imgX, scaled_imgY)
                
    def wavelengthPlot(self,scaled_imgX, scaled_imgY):
        reflectance = self.spectral_array[int(scaled_imgY), int(scaled_imgX), :]
        self.wavelengthPlotFigax.clear()
        self.wavelengthPlotFigax.plot(np.arange(0, self.noOfBandsEMR), reflectance)
        self.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.wavelengthPlotFigCanvas.draw()

    def about(self):
        aboutImgpath= 'data/about.png'
        # creates a new top level tkinter window.
        about_window = ctk.CTkToplevel(self)
        about_window.transient(self) 
        about_window.title("About")
        about_window.geometry("500x500")
        about_window.resizable(width=False, height=False)

        # routes all event for the app to about window.
        # user cannot intereact with app until about window is closed.
        about_window.grab_set()
        
        # makes the popup window appear on top of the application window
        # instead of a seperate desktop window.
        about_window.attributes('-topmost', True)
        about_window.after_idle(about_window.attributes, '-topmost', False)
        
        # Load the image
        aboutImg = Image.open(aboutImgpath)
        # Resize the image to fit the window
        aboutImg = aboutImg.resize((500,500))
        aboutImg_tk = ImageTk.PhotoImage(aboutImg)
        
        # Keep a reference to the image
        about_window.aboutImg_tk = aboutImg_tk
        
        aboutCanvas = tk.Canvas(master = about_window,
                                bd = 0,
                                highlightthickness = 0,
                                relief = 'ridge'
                                )
        aboutCanvas.create_image(0, 0, image=aboutImg_tk, anchor='nw')
        aboutCanvas.pack(expand=True, fill='both')

    def preferenceOptions_callback(self, choice):
        if choice == "K-means clustering":
            print("k means pressed")
        elif choice == "Segment Anything":
            print("segment anything pressed")
        elif choice == "Standard Normal Variate":
            print("standard normal variate pressed")
        elif choice == "Savitzky-Golay":
            print("savitzky golay pressed")
        elif choice == "Normalization":
            print("normalization pressed")
        elif choice == "ViT-H SAM Model":
            print("vit h sam model pressed")
        elif choice == "ViT-L SAM Model":
            print("vit l sam model pressed")
        elif choice == "ViT-B SAM Model":
            print("vit b sam model pressed")

    def croppingWindow(self):
        
        
        
        def cropped_getresizedImageCoordinates(event, canvas, tk_image, resized_tk):
    
    
            # The event object contains the x and y coordinates of the mouse click
            x, y = int(event.x), int(event.y)
            
            
            # Calculate the size of the borders
            border_x = (canvas.winfo_width() - resized_tk.width()) / 2
            border_y = (canvas.winfo_height() - resized_tk.height()) / 2
            
            if border_x == 0:
                if y <= int(border_y):
                    pass
                elif y>= (int(border_y) + resized_tk.height()):
                    pass
                elif int(border_y) <= y <= (int(border_y) + resized_tk.height()):
                    imgX = x-int(border_x)
                    imgY = y-int(border_y)
                    
                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()
                    
                    scaled_imgX = round(imgX * x_scale_ratio)
                    scaled_imgY = round(imgY * y_scale_ratio)
                    generateFinalSegmentedImage(segmented_img = tk_image, x = scaled_imgX, y = scaled_imgY)
                    
                    
                    
            
            elif border_y == 0:
                if x <= int(border_x):
                    pass
                elif x >= (int(border_x) + resized_tk.width()):
                    pass
                elif int(border_x) <= x <= (int(border_x) + resized_tk.width()):
                    imgX = x-int(border_x)
                    imgY = y-int(border_y)
            
                    
                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()
                    
                    scaled_imgX = round(imgX * x_scale_ratio)
                    scaled_imgY = round(imgY * y_scale_ratio)
                    generateFinalSegmentedImage(segmented_img = tk_image, x = scaled_imgX, y = scaled_imgY)
        
        
        def generateFinalSegmentedImage(segmented_img, x,y):
            segmented_img = np.array(segmented_img)
            point_color = segmented_img[y,x]
            self.mask = np.all(segmented_img == point_color, axis=-1)
            extracted_point = np.where(self.mask[..., None], segmented_img, 255)
            
            # Convert the NumPy array back to a PIL Image
            extracted_point_img = Image.fromarray(extracted_point.astype('uint8'))
            
            for widget in rightCroppedImageFrame.winfo_children():
                widget.destroy()
                
            croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                bg = self.rgbValues(),
                bd =0,
                highlightthickness=0,
                relief='ridge')
            
            croppedImgcroppingCanvas.pack(expand = True, fill='both')
            croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, extracted_point_img, canvas=croppedImgcroppingCanvas))
            
            
            
            
        
        def cropped_full_image(event, tk_image, canvas):
        
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
            resized_tk = ImageTk.PhotoImage(resized_image)
            
            canvas.create_image(
                int(event.width/2), 
                int(event.height/2), 
                anchor = 'center',
                image=resized_tk)
            canvas.image = resized_tk
            
        def getResizedCanvasImage(tk_image, canvas):
        
            # this function takes in a image and calculates it's dimension and the window dimension
            # and then makes sure that the image is fit to the window frame.
        
            canvas_ratio = canvas.winfo_width() / canvas.winfo_height()
            img_ratio = tk_image.size[0]/tk_image.size[1]
            
            if canvas_ratio > img_ratio: 
                height = int(canvas.winfo_height())
                width = int(height * img_ratio)
            else: 
                width = int(canvas.winfo_width())
                height = int(width/img_ratio)
                
                
            resized_image = tk_image.resize((width, height))
            resized_tk = ImageTk.PhotoImage(resized_image)

            return resized_tk
            
        
        def callback(event):
            # print ("clicked at", event.x, event.y)
            
            xypos.append([event.x, event.y])
            if len(xypos) > 1:
                oriImgcroppingCanvas.delete("box")  # delete the old rectangle
                x, y = xypos[0]
                x1, y1 = xypos[-1]
                oriImgcroppingCanvas.create_rectangle(x, y, event.x, event.y, outline="red", tags="box", width=2)
            
        def getCroppedimage(canvas, image, xypos):

            x, y = xypos[0]
            x1, y1 = xypos[-1]
            
            border_x = (canvas.winfo_width() - self.resized_tk.width()) / 2
            border_y = (canvas.winfo_height() - self.resized_tk.height()) / 2

            imgX = x-int(border_x)
            imgY = y-int(border_y)
            imgX1 = x1-int(border_x)
            imgY1 = y1-int(border_y)
            
            x_scale_ratio = image.width / self.resized_tk.width()
            y_scale_ratio = image.height / self.resized_tk.height()
            
            self.scaled_imgX = round(imgX * x_scale_ratio)
            self.scaled_imgY = round(imgY * y_scale_ratio)
            self.scaled_imgX1 = round(imgX1 * x_scale_ratio)
            self.scaled_imgY1 = round(imgY1 * y_scale_ratio)
            
            croppedImage = image.crop((self.scaled_imgX, self.scaled_imgY, self.scaled_imgX1, self.scaled_imgY1))
            
            return croppedImage

        def display_cropped_image(event):
            # Crop the image
            croppedImg = getCroppedimage(oriImgcroppingCanvas, self.tk_image, xypos)
            
            xypos.clear()
            
            # Convert the cropped image to a PhotoImage
           
            for widget in rightCroppedImageFrame.winfo_children():
                widget.destroy()
                
            croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                bg = self.rgbValues(),
                bd =0,
                highlightthickness=0,
                relief='ridge')
            
            croppedImgcroppingCanvas.pack(expand = True, fill='both')
            croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, croppedImg, canvas=croppedImgcroppingCanvas))
            
            
    
        def savecroppedImage():
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving cropped data ...'
                threading.Thread(target = savecroppedimageDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def savecroppedimageDataloader():
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.Dataloaded = True
        
        
        def saveUnfoldedcroppedImage():
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Comma Separated Values", "*.csv"),
                                                                ("Text File", ".txt"),
                                                                ("Numpy Array", "*.npy"),
                                                                ])
            if self.saveFile is not None:
                self.loadDataText = f'Saving cropped data (unfolded) ...'
                threading.Thread(target = setUnfoldedDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def setUnfoldedDataloader():
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            dataToSave = unfold(dataToSave)
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.Dataloaded = True
            
            
        def saveSegmentedImage():
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving Segmented data (x,y,z) ...'
                threading.Thread(target = saveSegmentedDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def saveSegmentedDataloader():
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            dataToSave = np.where(self.mask[..., None], dataToSave, 0)
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.Dataloaded = True
            
            
        def saveUnfoldedSegmentedImage():
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving unfolded Segmented data (x,y) ...'
                threading.Thread(target = saveUnfoldedSegmentedDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def saveUnfoldedSegmentedDataloader():
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            dataToSave = np.where(self.mask[..., None], dataToSave, 0)
            dataToSave = unfold(dataToSave)
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.Dataloaded = True
            
            
        def applySegmentation():
            # self.KclusterNoSegPrePro = 2
            # self.KClusterThresPrePro = 2
            # self.selectedSAMModel = 'ViT-B SAM Model'
            # self.defaultSegmentationMethod = 'K means clustering'
            croppedImg = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            
            for widget in rightCroppedImageFrame.winfo_children():
                    widget.destroy()
                    
            if self.defaultSegmentationMethod == "K means clustering":
                
                segmentedImg = kmeansSegmentation(array= croppedImg, 
                                                  clusters = self.KclusterNoSegPrePro, 
                                                  bands = 3)
                
                segmentedtk_image = Image.fromarray(np.uint8(segmentedImg))
                
                croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                    bg = self.rgbValues(),
                    bd = 0,
                    highlightthickness=0,
                    relief='ridge')
                croppedImgcroppingCanvas.pack( expand =True, fill='both')
                croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, segmentedtk_image, canvas=croppedImgcroppingCanvas))
                croppedImgcroppingCanvas.bind('<1>', lambda event: cropped_getresizedImageCoordinates(event, canvas = croppedImgcroppingCanvas, tk_image = segmentedtk_image,resized_tk= getResizedCanvasImage(tk_image=segmentedtk_image,canvas =croppedImgcroppingCanvas)))

                
            elif self.defaultSegmentationMethod == "SAM Model":
                pass
            
        
        
        
        

        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()

        
        ## children to workMenuFrame 
        leftOriginalImageFrame = ctk.CTkFrame(master = self.workAreaFrame)
        rightCroppedImageFrame = ctk.CTkFrame(master = self.workAreaFrame)
        leftBottomButtonCroppingFrame = ctk.CTkFrame(master = self.workAreaFrame)
        righBottomButtonCroppingFrame = ctk.CTkFrame(master = self.workAreaFrame)
        
        leftOriginalImageFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        rightCroppedImageFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        leftBottomButtonCroppingFrame.place(rely = 0.9, x=0, relwidth = 0.5, relheight = 0.1)
        righBottomButtonCroppingFrame.place(rely = 0.9, relx=0.5, relwidth = 0.5, relheight = 0.1)
    
    
        leftBottomButtonCroppingFrame.columnconfigure((0,1,2,3), weight = 1)
        leftBottomButtonCroppingFrame.rowconfigure((0,1), weight = 1)
        righBottomButtonCroppingFrame.columnconfigure((0,1,2,3), weight = 1)
        righBottomButtonCroppingFrame.rowconfigure((0,1), weight = 1)
        
        
        
        
        saveCroppedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Cropped Image (x,y,z)',
                                                    command= savecroppedImage)
        saveunfoldedCroppedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Unfolded Cropped Image (x,y)',
                                                    command= saveUnfoldedcroppedImage)
        saveSegmentedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Segmented Image',
                                                    command= saveSegmentedImage)
        saveunfoldedSegmentedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Unfolded Segmented Image',
                                                    command= saveUnfoldedSegmentedImage)
        
        saveCroppedImageButton.grid(row =1, column =0, sticky = 'nsew', pady= 10, padx=10)
        saveunfoldedCroppedImageButton.grid(row =1, column =1, sticky = 'nsew', pady= 10, padx=10)
        saveSegmentedImageButton.grid(row =1, column =2, sticky = 'nsew', pady= 10, padx=10)
        saveunfoldedSegmentedImageButton.grid(row =1, column =3, sticky = 'nsew', pady= 10, padx=10)
        
        
        # applyCroppingImageButton = ctk.CTkButton(master = leftBottomButtonCroppingFrame, 
        #                                             text = 'Apply \n Cropping',
        #                                             command= savecroppedImage)
        applySegmentationImageButton = ctk.CTkButton(master = leftBottomButtonCroppingFrame, 
                                                    text = 'Apply \n Segmentation',
                                                    command= applySegmentation)
        
        # applyCroppingImageButton.grid(row =1, column =0, columnspan =2, sticky = 'nsew', pady= 10, padx=10)
        applySegmentationImageButton.grid(row =1, column =2, columnspan =2 ,sticky = 'nsew', pady= 10, padx=10)

        
        
      
   
        if self.raw_img_dir == None:
            pass
        else:
            for widget in leftOriginalImageFrame.winfo_children():
                widget.destroy()
            xypos = []
            
            oriImgcroppingCanvas = ctk.CTkCanvas(leftOriginalImageFrame,
                            bg = self.rgbValues(),
                            bd =0,
                            highlightthickness=0,
                            relief='ridge')
        
            
            oriImgcroppingCanvas.pack(expand =True, fill='both')
            oriImgcroppingCanvas.bind('<Configure>',lambda event: self.full_image(event, tk_image= self.tk_image, canvas=oriImgcroppingCanvas))
            oriImgcroppingCanvas.bind("<B1-Motion>", callback)
            oriImgcroppingCanvas.bind("<ButtonRelease-1>", display_cropped_image)

    def preprocessingWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()

        
        
        ## children to workMenuFrame 
        self.leftButtonsPreProFrame = ctk.CTkFrame(master = self.workAreaFrame)
        self.leftButtonsPreProFrame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        self.middlePreProFrame = ctk.CTkFrame(master = self.workAreaFrame)
        self.middlePreProFrame.place(relx = 0.2, y = 0, relwidth = 0.4, relheight = 1)
        self.rightPreProFrame = ctk.CTkFrame(master = self.workAreaFrame)
        self.rightPreProFrame.place(relx = 0.6, y = 0, relwidth = 0.4, relheight = 1)
    

        self.leftButtonsPreProFrame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.rightPreProFrame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.rightPreProFrame.columnconfigure((0,1), weight = 1)
        
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods
        
        self.PreProOptionsInput = ctk.CTkLabel(master = self.leftButtonsPreProFrame,
                                               text = "Input: Raw Data. \nSelect filters as forward feed. \nSelect None (pass) to skip filter.")
        self.PreProOptionsInput.grid(row = 0, column = 0, sticky='ew', padx = 30, pady =(50,0))
        


        self.PreProOptions1 = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option1", selection))
        
        self.PreProOptions1.set("Filter 1")
        self.PreProOptions1.grid(row = 1, column = 0, sticky='ew', padx = 30, pady =(0,5))
   
        
        self.PreProOptions2 = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option2", selection))
        self.PreProOptions2.set("Filter 2")
        self.PreProOptions2.grid(row = 2, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.PreProOptions3 = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                         
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option3", selection))
        self.PreProOptions3.set("Filter 3")
        self.PreProOptions3.grid(row = 3, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.PreProOptions4 = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option4", selection))
        self.PreProOptions4.set("Filter 4")
        self.PreProOptions4.grid(row = 4, column = 0, sticky='ew', padx = 30, pady =(0,5))
        

        

    
        self.PreProOptionsOutput = ctk.CTkLabel(master = self.leftButtonsPreProFrame,
                                               text = "Output: Preprocessed Data")
        self.PreProOptionsOutput.grid(row = 5, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.PreProApplyButton = ctk.CTkButton(master=self.leftButtonsPreProFrame, 
                                                    text="Apply Preprocessing", 
                                                    command = self.applyPreprocessing)
        self.PreProApplyButton.grid(row = 6, column = 0, sticky='ew', padx = 30, pady = (0,5))
        
        self.PreProSaveButton = ctk.CTkButton(master=self.leftButtonsPreProFrame, 
                                                    text="Save Preprocessed Data", 
                                                    command = self.savePreprocessedData)
        self.PreProSaveButton.grid(row = 7, column = 0, sticky='ew', padx = 30, pady = (0,50))
        

        # raw spectral plot in preprocessing window
        self.rawPlotFig, self.rawPlotFigax = plt.subplots(figsize =(10,10), dpi =40)
        self.rawPlotFig.set_facecolor(self.rgbValues())
        self.rawPlotFigax.set_facecolor(self.rgbValues())
        self.rawPlotFigax.set_title("Raw Spectral Signature")
        self.rawPlotFigax.set_xlabel("Wavelength")
        self.rawPlotFigax.set_ylabel("Reflectance")
        self.rawPlotFigCanvas = FigureCanvasTkAgg(self.rawPlotFig, master= self.middlePreProFrame)
        self.rawPlotFigCanvas.get_tk_widget().pack(expand = True, fill ='x')
        
        # preprocessed spectral plot in preprocessing window
        self.preProcessedPlotFig, self.preProcessedPlotFigax = plt.subplots(figsize =(10,10), dpi = 40)
        self.preProcessedPlotFig.set_facecolor(self.rgbValues())
        self.preProcessedPlotFigax.set_facecolor(self.rgbValues())
        self.preProcessedPlotFigax.set_title("Preprocessed Signature")
        self.preProcessedPlotFigax.set_xlabel("Wavelength")
        self.preProcessedPlotFigax.set_ylabel("Reflectance")
        self.preProcessedPlotFigCanvas = FigureCanvasTkAgg(self.preProcessedPlotFig, master= self.rightPreProFrame)
        self.preProcessedPlotFigCanvas.get_tk_widget().pack(expand = True, fill ='x')
        
        if self.raw_img_dir == None:
            pass
        else:
            self.rawSpectralPlot(self.unfoldedData)
        
    def preProcessingPipeLineSelection(self, source, selection):
        print(f"Selection from {source}: {selection}")
        if source == "option1":
            self.filter1 = selection
        elif source == "option2":
            self.filter2 = selection
        elif source == "option3":
            self.filter3 = selection
        elif source == "option4":
            self.filter4 = selection
        else:
            pass
            
    def applyPreprocessing(self):
        
        def preprocessing_in_thread():
            self.loadDataText = 'Loading...'
            
            self.loadDataText = f'Applying {self.filter1} ...'
            filter1data = preprocessing(self.filter1, self.unfoldedData,w = self.SGWinSizePrePro,p = self.SGPolyOrderPrePro)
            self.loadDataText = f'Applying {self.filter2} ...'
            filter2data = preprocessing(self.filter2, filter1data,w = self.SGWinSizePrePro,p = self.SGPolyOrderPrePro)
            self.loadDataText = f'Applying {self.filter3} ...'
            filter3data = preprocessing(self.filter3, filter2data,w = self.SGWinSizePrePro,p = self.SGPolyOrderPrePro)
            self.loadDataText = f'Applying {self.filter4} ...'
            self.preprocessedData = preprocessing(self.filter4, filter3data,w = self.SGWinSizePrePro,p = self.SGPolyOrderPrePro)
            self.loadDataText = f'Plotting preprocessed spectra ...'
            self.preprocessedSpectralPlot(self.preprocessedData)
            self.Dataloaded = True
            
        self.Dataloaded = False
        threading.Thread(target = preprocessing_in_thread).start()
        self.dataLoadingScreen()
        
    def savePreprocessedData(self):
        self.Dataloaded = False
        
        self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.csv',
                                               filetypes = [("Comma Separated Values", "*.csv"),
                                                            ("Text File", ".txt"),
                                                            ("Numpy Array", "*.npy"),
                                                            ])
        if self.saveFile is not None:
            self.loadDataText = f'Saving preprocessed data ...'
            threading.Thread(target = self.setDataloader).start()
            self.dataLoadingScreen()
            self.saveFile.close()
            
    def setDataloader(self):
        dataToSave = self.preprocessedData
        saveDatatoComputer(dataToSave, self.saveFile.name)
        self.Dataloaded = True

    def rawSpectralPlot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.rawPlotFigax.clear()
        for i, row in enumerate(selected_rows):
            self.rawPlotFigax.plot(np.arange(0, self.noOfBandsEMR), row, label=f'Row {indices[i]}')
        self.rawPlotFigax.set_title("Raw Spectral Signature")
        self.rawPlotFigax.set_xlabel("Wavelength")
        self.rawPlotFigax.set_ylabel("Reflectance")
        self.rawPlotFigCanvas.draw()
        
    def preprocessedSpectralPlot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.preProcessedPlotFigax.clear()
        for i, row in enumerate(selected_rows):
            self.preProcessedPlotFigax.plot(np.arange(0, self.noOfBandsEMR), row, label=f'Row {indices[i]}')
        self.preProcessedPlotFigax.set_title("Preprocessed Signature")
        self.preProcessedPlotFigax.set_xlabel("Wavelength")
        self.preProcessedPlotFigax.set_ylabel("Reflectance")
        self.preProcessedPlotFigCanvas.draw()

    def preferencesWindow(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
        
        def PreprocessingButton_callback():
            
            def savePreProSetting():
                self.SGWinSizePrePro = int(ppSGWinSizeEntry.get())
                self.SGPolyOrderPrePro = int(ppSGPolyOrderEntry.get() )   
                
                print(f"SG Window Size: {self.SGWinSizePrePro}")
                print(f"SG Poly Order: {self.SGPolyOrderPrePro}")
                
                
            # Clear rightFormFrame
            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            PreprocessingForm = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                             border_width= 1,
                                            )
            PreprocessingForm.pack(side = 'left', fill = 'both', expand = True)
        

            ppSGWinSizeLabel = ctk.CTkLabel(master = PreprocessingForm, text = "Enter Window Size for Savitzky Golay (odd number):  ", anchor = 'w')
            ppSGWinSizeEntry = ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter window size" )
            ppSGPolyOrderLabel = ctk.CTkLabel(master = PreprocessingForm, text = "Enter Polynomial Order for Savitzky Golay (< Window size):  ", anchor = 'w')
            ppSGPolyOrderEntry = ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter polynomial order" )
            savePreProSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=savePreProSetting)
           
            
            
            ppSGWinSizeLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            ppSGWinSizeEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            ppSGPolyOrderLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            ppSGPolyOrderEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            savePreProSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            

        
            
        def SegmentationButton_callback():
            
            def saveSegmentationSetting():
                  
                self.KclusterNoSegPrePro = int(segKclusterEntry.get())
                self.KClusterThresPrePro = int(segThresEntry.get())
                self.selectedSAMModel = str(segSAMModelOptions.get())
                self.defaultSegmentationMethod = str(segDefaultMethodOptions.get())
                
                print("K-cluster No Seg PrePro: ", self.KclusterNoSegPrePro)
                print("K-Cluster Thres PrePro: ", self.KClusterThresPrePro)
                print("Selected SAM Model: ", self.selectedSAMModel)
                print("Default Segmentation Model PrePro: ", self.defaultSegmentationMethod)
                
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            SegmentationForm = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1,
                                            )
            SegmentationForm.pack(side = 'left', fill = 'both', expand = True)
            
            segDefaultMethodLabel = ctk.CTkLabel(master = SegmentationForm, text = "Default Segmentation Method:  ", anchor='w')
            segKclusterLabel = ctk.CTkLabel(master = SegmentationForm, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
            segKclusterEntry = ctk.CTkEntry(master = SegmentationForm, placeholder_text="Enter cluster numbers" )
            segThresLabel = ctk.CTkLabel(master = SegmentationForm, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
            segThresEntry = ctk.CTkEntry(master = SegmentationForm, placeholder_text="Threshold number" )
            segSAMModelLabel = ctk.CTkLabel(master = SegmentationForm, text = "Select your SAM model:  ", anchor='w')
            saveSegmentationSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveSegmentationSetting)
            
            segSAMModelOptions = ctk.CTkOptionMenu(master = SegmentationForm,
                                                    values = ["ViT-H SAM Model", 
                                                            "ViT-L SAM Model", 
                                                            "ViT-B SAM Model"],
                                                    )
            segSAMModelOptions.set("SAM Models")
            
            segDefaultMethodOptions = ctk.CTkOptionMenu(master = SegmentationForm,
                                                    values = ["K means clustering", 
                                                            "SAM Model"],
                                                    )
            segDefaultMethodOptions.set("Default Segmentation Method")
            
            
            segDefaultMethodLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            segDefaultMethodOptions.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            segKclusterLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            segKclusterEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            segThresLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            segThresEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')                      
            segSAMModelLabel.grid(row = 3, column = 0,padx=100, pady=5, sticky = 'ew')
            segSAMModelOptions.grid(row = 3, column = 1 ,padx=100, pady=5, sticky = 'ew')
            saveSegmentationSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            
            
            
            
            


            

        def RGBButton_callback():
            
            
            def savePseudoRGBSetting():
                self.RedbandNoPseudoRGB = int(RedbandEntry.get())
                self.greenBandNoPseudoRGB = int(GreenbandEntry.get())
                self.blueBandNoPseudoRGB = int(BluebandEntry.get())  
                
                print(f"Red band number for Pseudo RGB Image: {self.RedbandNoPseudoRGB}")
                print(f"Green band number for Pseudo RGB Image: {self.greenBandNoPseudoRGB}")
                print(f"Blue band number for Pseudo RGB Image: {self.blueBandNoPseudoRGB}")
                
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            PseudoRGBFrame = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            PseudoRGBFrame.pack(side = 'left', fill = 'both', expand ='true')
            

            RedbandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
            RedbandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Red band number" )
            GreenbandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
            GreenbandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Green band number" )
            BluebandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
            BluebandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Blue band number" )
            savepseudoRGBSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command= savePseudoRGBSetting)
            
            
            RedbandLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            RedbandEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            GreenbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            GreenbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            BluebandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            BluebandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            savepseudoRGBSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            

                            
            
        def EMRButton_callback():
            
            
            def saveEMRSetting():
                self.noOfBandsEMR = int(BandNoEntry.get())
                self.firstBandEMR = int(FirstbandEntry.get())
                self.lastBandEMR =  int(LastbandEntry.get())
                self.spectralResolution = int(SpectralResolutionEntry.get())
                
                print(f"No of Band: {self.noOfBandsEMR}\n"
                    f"First Band: {self.firstBandEMR}\n"
                    f"Last Band: {self.lastBandEMR}\n"
                    f"Spectral Resolution: {self.spectralResolution}")
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            EMRInfoFrame = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            EMRInfoFrame.pack(side = 'left', fill = 'both', expand ='true')
            
            BandNoLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
            BandNoEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Total number of bands" )
            
            FirstbandLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
            FirstbandEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="First nanometer" )
            
            LastbandLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
            LastbandEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Last nanometer" )
            
            SpectralResolutionLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
            SpectralResolutionEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Spectral Resolution" )
            
            saveEMRSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveEMRSetting)
            
            BandNoLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            BandNoEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            FirstbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            FirstbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            LastbandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            LastbandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            SpectralResolutionLabel.grid(row = 3, column = 0, padx=100, pady=5, sticky = 'ew')
            SpectralResolutionEntry.grid(row = 3, column = 1,padx=100, pady=5,sticky = 'ew')
            saveEMRSettings.grid(row=0, column = 1, padx=5, pady=5, sticky = 'ew')
            
            


        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        leftPreferenceButtonsFrame = ctk.CTkFrame(master = self.workAreaFrame)
        rightPreferenceFormFrame = ctk.CTkFrame(master = self.workAreaFrame)
        rightBottomApplyButtomFrame = ctk.CTkFrame(master = self.workAreaFrame)
        
        leftPreferenceButtonsFrame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        rightPreferenceFormFrame.place(relx = 0.2, y = 0, relwidth = 0.8, relheight = 0.9)
        rightBottomApplyButtomFrame.place(rely = 0.9, relx = 0.2, relwidth =0.8, relheight =0.1)

        for widget in rightPreferenceFormFrame.winfo_children():
            widget.destroy()
        
        PreprocessingButton_callback()
        
        PreprocessingButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Preprocessing", command=PreprocessingButton_callback)
        SegmentationButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Segmentation", command=SegmentationButton_callback)
        RGBButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="RGB Bands", command=RGBButton_callback)
        EMRButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Wavelengths", command=EMRButton_callback)
        
        
        rightBottomApplyButtomFrame.columnconfigure((0,1,2), weight = 1)
        rightBottomApplyButtomFrame.rowconfigure((0), weight = 1)
        
        PreprocessingButton.pack(side= 'top',padx=50, pady=(50,10))
        SegmentationButton.pack(side= 'top',padx=50, pady=10)
        RGBButton.pack(side= 'top',padx=50, pady=10)
        EMRButton.pack(side= 'top',padx=50, pady=10)
        
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
        
        

        
app = App()
app.mainloop()