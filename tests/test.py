#####################################################################################
## Author: Billy G. Ram
## Linkedin: https://www.linkedin.com/in/billygrahamram/
## Twitter: https://twitter.com/billygrahamram
## Github: https://github.com/billygrahamram
## This code solely belongs to Billy G. Ram and is currently NOT open sourced. 
#####################################################################################

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt


### herschelVision modules ####
from readfile import *
### herschelVision modules ####

from plantcv import plantcv as pcv
import numpy as np

ctk.set_appearance_mode("light") # light, dark, system

def frame(master,
          corner_radius=0,
          
          border_width=1,
          border_color="gray",
          width = 100,
          height = 100,
          side='left',
          fill = 'both',
          expand = True,):
    
    frame = ctk.CTkFrame(master=master, 
                         corner_radius=corner_radius, 
                         
                         border_width=border_width, 
                         border_color=border_color,
                         width = width,
                         height = height)
    frame.pack(side=side, 
               fill=fill, 
               expand=expand)
    return frame 

def button(master,
           text='Button',
          
           bg_color='white',
           hover = True,
           width = 300,
           height = 10,
           corner_radius=100,
           border_width=1,
           border_color='gray',
           side='top',
           fill='both',
           expand=True,
           command=None):
    
    button = ctk.CTkButton(master=master,
                           text=text,
                           
                           bg_color=bg_color,
                           hover = hover,
                           width = width,
                           height = height,
                           corner_radius=corner_radius,
                           border_width=border_width,
                           border_color=border_color,
                           command=command)

    button.pack(side=side, fill=fill, expand=expand)
    
    return button

def button_event():
    print("button pressed")
    
    
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #inheriting the data analysis class
    
        
        self.geometry("1600x900")
        self.title("Herchel Vision: Hyperspectral Image Analysis")
        self.resizable(width=True, height=True)

    
        ## self.raw_img_dir is the directory path for the image currently worked on.
        self.raw_img_dir = None
   
        
        # Empty the img_dir_record.txt file at startup. Opens and closes it, making the file empty.
        data_path_file = os.path.join('history', 'img_dir_record.txt')
        with open(data_path_file, 'w') as f:
            pass
        
        ## children to main window
        self.menuBarFrame = frame(master = self, side = 'top', border_width=1 ,fill = 'x', expand=False)
        self.workAreaFrame = frame(master = self, side = 'top', border_width=1,fill = 'both', expand= True)

        
        # opens the home window by default
        self.homeWindow()
        self.mainMenu()
    


    def mainMenu(self):
        ## children to menuBarFrame. Menu bar buttons
        self.FileOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Home","New","Open","Save","Export","Exit"], command=self.optionmenu_callback)
        self.FileOptionMenu.set("File")
        self.FileOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.EditOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        self.EditOptionMenu.set("Edit")
        self.EditOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.ToolsOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        self.ToolsOptionMenu.set("Tools")
        self.ToolsOptionMenu.pack(side= 'left',padx=5, pady=5)

        self.AboutOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Updates","Version","About","References", "Contact us"], command=self.optionmenu_callback)
        self.AboutOptionMenu.set("About")
        self.AboutOptionMenu.pack(side= 'left',padx=5, pady=5)
       
       
    def optionmenu_callback(self,choice):
        ## method to select function to buttons in main menu.
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()
        elif choice == 'Segmentation':
            self.imageSegmentationWindow()
        elif choice == 'Preprocessing':
            self.preprocessingWindow()
        elif choice == 'Preferences':
            self.preferencesWindow()
        elif choice == 'Home':
            self.homeWindow()

    
    def homeWindow(self):
        # method to show the home window.
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        ## children to workMenuFrame 
        self.leftFrame = frame(master=self.workAreaFrame, side='left', border_width= 1)
        self.rightFrame = frame(master=self.workAreaFrame, side='right', border_width= 1)
        

        ## children to leftFrame
        self.leftFrameTop = frame(master=self.leftFrame, 
                                  side='top', 
                                  border_width= 1)
        self.leftFrameBottom = frame(master=self.leftFrame, 
                                     side='top', 
                                     border_width= 1,
                                     expand = False)
        
        data_path_file = os.path.join('history', 'img_dir_record.txt') 
        
        # if the img_dir_record is empty. show the welcome image
        if os.path.exists(data_path_file) and os.path.getsize(data_path_file) == 0:
            lightThemeImgPath = 'data/welcomeLight.png'
            darkThemeImgPath = 'data/welcomeDark.png'
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
                
            
            else:
                welcomeImg = Image.open(darkThemeImgPath)
                

            homeCanvas = ctk.CTkCanvas(self.leftFrameTop, 
                            bg = self.rgbValues(),
                            bd =0,
                            highlightthickness=0,
                            relief='ridge')
            
            homeCanvas.pack(expand=True, fill='both')
            homeCanvas.bind('<Configure>',lambda event: self.full_image(event, welcomeImg, canvas=homeCanvas))
        
        elif os.path.exists(data_path_file) and os.path.getsize(data_path_file) > 0:
            with open(data_path_file, 'r') as f:
                self.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.leftFrameTop, 
                        bg = self.rgbValues(),
                        bd =0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand=True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: self.getresizedImageCoordinates(event, canvas = homeCanvas, image = self.tk_image))
        else:
            pass
            

        # left side slider and slider label
        self.wavelengthSlider = ctk.CTkSlider(self.leftFrameBottom, from_ = 0, to = 223,
                                height = 30, command = self.wavelengthsSlider_event)
        self.wavelengthSlider.pack(side='bottom', expand = False, fill ='x')
        self.wavelengthSliderCurrentValueLabel = ctk.CTkLabel(master = self.leftFrameBottom, 
                                                    text = "", 
                                                    justify = "center")
        self.wavelengthSliderCurrentValueLabel.pack(side='bottom', expand =False, fill='x')
        self.wavelengthsSlider_event(220)
            
            
        
        
        
        ## children to righFrame
        self.rightFrameTop = frame(master=self.rightFrame, 
                                   side='top', 
                                   border_width= 1)
        self.rightFrameMiddle = frame(master=self.rightFrame, 
                                      side='top', 
                                      border_width= 1)
        self.rightFrameBottom = frame(master=self.rightFrame, 
                                   side='top', 
                                   border_width= 1,
                                   expand = False)
   
        
        # right side plot and labels
        #### scatter plot ######
        self.wavelengthPlotFigLabel = ctk.CTkLabel(master = self.rightFrameTop, 
                                                    text = "Wavelength Plots", 
                                                    justify = "center")
        self.wavelengthPlotFigLabel.pack(side='top', expand = False, fill='x')
        self.wavelengthPlotFig, self.wavelengthPlotFigax = plt.subplots()
        self.wavelengthPlotFig.set_facecolor(self.rgbValues())
        self.wavelengthPlotFigax.set_facecolor(self.rgbValues())
        self.wavelengthPlotFigCanvas = FigureCanvasTkAgg(self.wavelengthPlotFig, master= self.rightFrameTop)
        self.wavelengthPlotFigCanvas.get_tk_widget().pack(side = 'top', fill='x', expand=False)


        # self.rightFrameBottomScatter = frame(master=self.rightFrameBottom, side='top', border_width= 0)
        # self.rightFrameBottomSlider = frame(master=self.rightFrameBottom, side='top', border_width= 0, expand = False, fill ='x')
        
    
        #### scatter plot ######
        self.scatterPlotFigLabel = ctk.CTkLabel(master = self.rightFrameMiddle, 
                                                    text = "Scatter Plot", 
                                                    justify = "center")
        self.scatterPlotFigLabel.pack(side='top', expand = False, fill='x')
        self.scatterPlotFig, self.scatterPlotFigax = plt.subplots()
        self.scatterPlotFig.set_facecolor(self.rgbValues())
        self.scatterPlotFigax.set_facecolor(self.rgbValues())
        self.scatterPlotFigCanvas = FigureCanvasTkAgg(self.scatterPlotFig, master= self.rightFrameMiddle)
        self.scatterPlotFigCanvas.get_tk_widget().pack(side = 'top', fill='x', expand=True)



    # Configure the rows and columns of the grid
        self.rightFrameBottom.grid_rowconfigure(0, weight=1)    # Makes the row expandable
        self.rightFrameBottom.grid_columnconfigure(0, weight=1) # Makes the first column expandable
        self.rightFrameBottom.grid_columnconfigure(1, weight=1) # Makes the second column expandable

        # right scatter slider and slider label for first band
        self.band1ScatterSlider = ctk.CTkSlider(self.rightFrameBottom, from_ = 0, to = 223,
                                height = 30, command = self.band1ScatterSlider_event)
        self.band1ScatterSlider.grid(row =0, column =0, sticky ='ew',padx = (150,50))
        self.band1ScatterSlider_event(220)
        
        
        # right scatter slider and slider label for second band
        self.band2ScatterSlider = ctk.CTkSlider(self.rightFrameBottom, from_ = 0, to = 223,
                                height = 30, command = self.band2ScatterSlider_event)
        self.band2ScatterSlider.grid(row =0, column=1, sticky='ew',padx = (50,150))
        self.band2ScatterSlider_event(220)

        
        self.band1Value = 150
        self.band2Value = 150
        
        

    
        
            
            

            
    
    def full_image(self,event, tk_image, canvas):
        
        # this function takes in a image and calculates it's dimension and the window dimension
        # and then makes sure that the image is fit to the window frame.
        
        canvas_ratio = event.width / event.height
        img_ratio = tk_image.size[0]/tk_image.size[1]
        
        if canvas_ratio > img_ratio: # canvas is wider than the image
            height = int(event.height)
            width = int(height * img_ratio)
        else: # canvas is narrow than the image
            width = int(event.width)
            height = int(width/img_ratio)
            
            
        resized_image = tk_image.resize((width, height))
        self.resized_tk = ImageTk.PhotoImage(resized_image)
        canvas.create_image(
            int(event.width/2), 
            int(event.height/2), 
            anchor = 'center',
            image=self.resized_tk,
            tag ='img')
        canvas.image = self.resized_tk
        
    
    def open(self):
        self.raw_img_dir = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = [("Raw Hyperspectral Image", "*.raw")
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
                
        self.wavelengthsSlider_event(value=220)
        
        self.kmeanslabels, self.unfoldedData = scatterPlotData(self.raw_img_dir)
   
        

    
    def wavelengthsSlider_event(self, value):
        
        if self.raw_img_dir == None:
            pass

  
        else:
            
            self.spectral_array = readData(self.raw_img_dir)

            single_band_img = single_band(self.spectral_array, int(value))
            
            self.tk_image = Image.fromarray(np.uint8(single_band_img))

            # updates the current slider value
            self.wavelengthSliderCurrentValueLabel.configure(text= "Current Wavelength: " + str(int(value)))
            
    
            # destroy the left frame for new image
            for widget in self.leftFrameTop.winfo_children():
                widget.destroy()
            
            openCanvas = ctk.CTkCanvas(self.leftFrameTop, 
                            bg = self.rgbValues(),
                            bd =0,
                            highlightthickness=0,
                            relief='ridge')
        
            # makes sure that the new image is displayed as "fit" within the frame.
            openCanvas.pack(side = 'top', expand=True, fill='both')
        
            openCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: self.getresizedImageCoordinates(event, canvas = openCanvas, image = self.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.
            
            
    def band1ScatterSlider_event(self, value):
        if self.raw_img_dir == None:
            pass
        else:
            self.band1Value= int(value)
            self.scatterPlotFigax.clear()
            self.scatterPlotFigax.scatter(self.unfoldedData[:, self.band1Value], self.unfoldedData[:,self.band2Value], c=self.kmeanslabels, s=2)
            self.scatterPlotFigax.figure.canvas.draw()

        


    
    def band2ScatterSlider_event(self, value):
        if self.raw_img_dir == None:
            pass
        else:
            self.band2Value = int(value)
            self.scatterPlotFigax.clear()
            self.scatterPlotFigax.scatter(self.unfoldedData[:, self.band1Value], self.unfoldedData[:,self.band2Value], c=self.kmeanslabels, s=2)
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
        self.wavelengthPlotFigax.plot(np.arange(1, 225), reflectance)
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

    def imageSegmentationWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.leftButtonsImgSegFrame = frame(master=self.workAreaFrame, 
                               side='left', 
                               border_width= 1,
                               expand = False,
                               width = self.dimensionPercentage(4, dimension='w'),
                               height = self.dimensionPercentage(100, dimension='h'))
        self.middleImgSegFrame = frame(master=self.workAreaFrame, 
                                 side='left', 
                                 border_width= 1,
                                 
                                 width = self.dimensionPercentage(48, dimension='w'),
                                 height = self.dimensionPercentage(100, dimension='h'))
        self.rightImgSegFrame = frame(master=self.workAreaFrame, 
                                side='left', 
                                border_width= 1,
                                
                                width = self.dimensionPercentage(48, dimension='w'),
                                height = self.dimensionPercentage(100, dimension='h'))
        
        ## children to righFrame
        self.rightImgSegTopFrame = frame(master=self.rightImgSegFrame, 
                                   side='top', 
                                   border_width= 1, 
                                   border_color='gray',
                                   height =  self.dimensionPercentage(70, dimension='h'))
        self.rightImgSegBottomButtonFrame = frame(master=self.rightImgSegFrame, 
                                      side='top', 
                                      border_width= 1, 
                                      border_color='gray', expand = False,
                                      height = self.dimensionPercentage(30, dimension='h'))
        
        self.rightImgSegBottomButtonFrame.columnconfigure(0, weight=1)
        self.rightImgSegBottomButtonFrame.columnconfigure(1, weight=1)

        ## RIGHT BOTTOM Buttons
        self.saveImgasNPYButton(master = self.rightImgSegBottomButtonFrame)
        self.saveUnfoldDatButton(master = self.rightImgSegBottomButtonFrame)
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods

        self.ImgSegOptions = ctk.CTkOptionMenu(master = self.leftButtonsImgSegFrame,
                                                values = ["K-means clustering", 
                                                          "Segment Anything"],command = self.optionmenu_callback)
        self.ImgSegOptions.set("Segmentation Models")
        self.ImgSegOptions.pack(side= 'top',padx=50, pady=(50,10))
        self.ImgSegParametersButton = ctk.CTkButton(master=self.leftButtonsImgSegFrame, text="Parameters", command=self.preferencesWindow)
        self.ImgSegParametersButton.pack(side= 'top',padx=50, pady=10)

    def preprocessingWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.leftButtonsPreProFrame = frame(master=self.workAreaFrame, 
                               side='left', 
                               border_width= 1,
                            expand = False,
                               width = self.dimensionPercentage(4, dimension='w'),
                               height = self.dimensionPercentage(100, dimension='h'))
        self.middlePreProFrame = frame(master=self.workAreaFrame, 
                                 side='left', 
                                 border_width= 1,
                                 
                                 width = self.dimensionPercentage(48, dimension='w'),
                                 height = self.dimensionPercentage(100, dimension='h'))
        self.rightPreProFrame = frame(master=self.workAreaFrame, 
                                side='left', 
                                border_width= 1,
                                
                                width = self.dimensionPercentage(48, dimension='w'),
                                height = self.dimensionPercentage(100, dimension='h'))
        
        ## children to righFrame
        self.rightPreProTopFrame = frame(master=self.rightPreProFrame, 
                                   side='top', 
                                   border_width= 1, 
                                   border_color='gray',
                                   height =  self.dimensionPercentage(70, dimension='h'))
        self.rightPreProBottomButtonFrame = frame(master=self.rightPreProFrame, 
                                      side='top', 
                                      border_width= 1, 
                                      border_color='gray', expand = False,
                                      height = self.dimensionPercentage(30, dimension='h'))
        
        self.rightPreProBottomButtonFrame.columnconfigure(0, weight=1)
        self.rightPreProBottomButtonFrame.columnconfigure(1, weight=1)

        ## RIGHT BOTTOM Buttons
        self.saveImgasNPYButton(master = self.rightPreProBottomButtonFrame)
        self.saveUnfoldDatButton(master = self.rightPreProBottomButtonFrame)
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods

        self.PreProOptions = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["SNV", 
                                                          "MSC",
                                                          "SG",
                                                          "Normalize"],command = self.optionmenu_callback)
        self.PreProOptions.set("PreProcessing Methods")
        self.PreProOptions.pack(side= 'top',padx=50, pady=(50,10))
        self.PreProParametersButton = ctk.CTkButton(master=self.leftButtonsPreProFrame, text="Parameters", command=self.preferencesWindow)
        self.PreProParametersButton.pack(side= 'top',padx=50, pady=10)
        
    def preferencesWindow(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        ## children to workAreaFrame 
        self.leftPreferenceButtonsFrame = frame(master=self.workAreaFrame,  
                                      border_width= 1,
                                      
                                      width = self.dimensionPercentage(5, dimension='w'), 
                                      height = self.dimensionPercentage(100, dimension='h'),
                                      side='left', expand = False, fill ='both')
        self.rightPreferenceFormFrame = frame(master=self.workAreaFrame,  
                                       border_width= 1,
                                       
                                       width = self.dimensionPercentage(95, dimension='w'), 
                                       height = self.dimensionPercentage(100, dimension='h'),
                                       side='left')
            # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
        self.PreprocessingButton_callback()
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        self.PreprocessingButton = ctk.CTkButton(master=self.leftPreferenceButtonsFrame, text="Preprocessing", command=self.PreprocessingButton_callback)
        self.PreprocessingButton.pack(side= 'top',padx=50, pady=(50,10))
        self.SegmentationButton = ctk.CTkButton(master=self.leftPreferenceButtonsFrame, text="Segmentation", command=self.SegmentationButton_callback)
        self.SegmentationButton.pack(side= 'top',padx=50, pady=10)
        self.RGBButton = ctk.CTkButton(master=self.leftPreferenceButtonsFrame, text="RGB Bands", command=self.RGBButton_callback)
        self.RGBButton.pack(side= 'top',padx=50, pady=10)
        self.EMRButton = ctk.CTkButton(master=self.leftPreferenceButtonsFrame, text="Wavelengths", command=self.EMRButton_callback)
        self.EMRButton.pack(side= 'top',padx=50, pady=10)
        
    def PreprocessingButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.PreprocessingForm = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 1,
                                        
                                        side='left',  fill ='both')
        

        ## label and dropdown for the preprocessing methods
        self.ppModelLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Select your preprocessing method:  ", anchor='w')
        self.ppModelLabel.grid(row = 0, column = 0,padx=100, pady=(100,5), sticky = 'ew')
        self.ppModelOptions = ctk.CTkOptionMenu(master = self.PreprocessingForm,
                                                values = ["Standard Normal Variate", 
                                                          "Multiplicative Scatter Correction", 
                                                          "Savitzky-Golay", 
                                                          "Normalization"],command = self.optionmenu_callback)
        self.ppModelOptions.set("Preprocessing Models")
        self.ppModelOptions.grid(row = 0, column = 1 ,padx=100, pady=(100,5), sticky = 'ew')
        
        
        ## label and input field for savitzky golay window size
        self.ppSGWinSizeLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Enter Window Size for Savitzky Golay:  ", anchor = 'w')
        self.ppSGWinSizeLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
        self.ppSGWinSizeEntry = ctk.CTkEntry(master = self.PreprocessingForm, placeholder_text="Enter window size" )
        self.ppSGWinSizeEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
                                   
        
        ## label and input field for savitzky golay derivative
        self.ppSGDerivLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Enter Savitzky Golay Derivative:  ", anchor = 'w')
        self.ppSGDerivLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
        self.ppSGDerivEntry = ctk.CTkEntry(master = self.PreprocessingForm, placeholder_text="Enter Derivative Number" )
        self.ppSGDerivEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
        
    def SegmentationButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.SegmentationForm = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 1,
                                         
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.segKclusterLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
        self.segKclusterLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
        self.segKclusterEntry = ctk.CTkEntry(master = self.SegmentationForm, placeholder_text="Enter cluster numbers" )
        self.segKclusterEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
                                   
        
        ## label and input field for savitzky golay derivative
        self.segThresLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
        self.segThresLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
        self.segThresEntry = ctk.CTkEntry(master = self.SegmentationForm, placeholder_text="Threshold number" )
        self.segThresEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
        
        ## label and dropdown for the preprocessing methods
        self.segSAMModelLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Select your SAM model:  ", anchor='w')
        self.segSAMModelLabel.grid(row = 2, column = 0,padx=100, pady=5, sticky = 'ew')
        self.segSAMModelOptions = ctk.CTkOptionMenu(master = self.SegmentationForm,
                                                values = ["ViT-H SAM Model", 
                                                          "ViT-L SAM Model", 
                                                          "ViT-B SAM Model"],command = self.optionmenu_callback)
        self.segSAMModelOptions.set("SAM Models")
        self.segSAMModelOptions.grid(row = 2, column = 1 ,padx=100, pady=5, sticky = 'ew')
         
    def RGBButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.PseudoRGBFrame = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 1,
                                        
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.RedbandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
        self.RedbandLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
        self.RedbandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Red band number" )
        self.RedbandEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
                                   
        ## label and input field for savitzky golay derivative
        self.GreenbandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
        self.GreenbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
        self.GreenbandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Green band number" )
        self.GreenbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.BluebandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
        self.BluebandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
        self.BluebandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Blue band number" )
        self.BluebandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')

    def EMRButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.EMRInfoFrame = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 1,
                                        
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.BandNoLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
        self.BandNoLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
        self.BandNoEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Total number of bands" )
        self.BandNoEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
                                   
        ## label and input field for savitzky golay derivative
        self.FirstbandLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
        self.FirstbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
        self.FirstbandEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="First nanometer" )
        self.FirstbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.LastbandLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
        self.LastbandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
        self.LastbandEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Last nanometer" )
        self.LastbandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.SpectralResolutionLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
        self.SpectralResolutionLabel.grid(row = 3, column = 0, padx=100, pady=5, sticky = 'ew')
        self.SpectralResolutionEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Spectral Resolution" )
        self.SpectralResolutionEntry.grid(row = 3, column = 1,padx=100, pady=5,sticky = 'ew')

    def dimensionPercentage(self, percent, dimension='w'):
        if dimension == 'h':
            size = self.winfo_height()
        elif dimension == 'w':
            size = self.winfo_width()
        else:
            raise ValueError("Invalid dimension: choose either 'w' or 'h'")
            
        pxSize = int((percent*size)/100)
        return pxSize

    def saveImgasNPYButton(self, master):
        self.button = ctk.CTkButton(master=master,
                                                    text='Save Image as NPY (3D array)',
                                                    
                                                    
                                                    hover = True,
                                                    
                                                    border_width=1,
                                                    border_color='gray',
                                                    command=button_event)

        self.button.grid(row = 0, column = 0, sticky='ew')
        
    def saveUnfoldDatButton(self, master):
        self.button = ctk.CTkButton(master=master,
                                                    text='Save Unfold Image (.txt)',
                                                    
                                                    
                                                    hover = True,
                                                    
                                                    border_width=1,
                                                    border_color='gray',
                                                    command=button_event)
        self.button.grid(row = 0, column = 1, sticky='ew')
        
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