import os
from utils.variables_utils import *
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from common.common_utils import *
import matplotlib.pyplot as plt

class HomeWindow():
    def __init__(self,obj_lvl1):
        self.obj_lvl2 = obj_lvl1

    def home_menu(self):
        # method to show the home window.
        
        # Clear self.workAreaFrame
        for widget in self.obj_lvl2.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.obj_lvl2.leftOriginalImgFrame = ctk.CTkFrame(master = self.obj_lvl2.workAreaFrame)
        self.obj_lvl2.rightPlotsImgFrame   = ctk.CTkFrame(master = self.obj_lvl2.workAreaFrame)
        self.obj_lvl2.bottomSliderFrame    = ctk.CTkFrame(master = self.obj_lvl2.workAreaFrame)

        
        self.obj_lvl2.leftOriginalImgFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        self.obj_lvl2.rightPlotsImgFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        self.obj_lvl2.bottomSliderFrame.place(rely = 0.9, y = 0, relwidth = 1, relheight = 0.1)


        self.obj_lvl2.rightPlotsImgFrame.rowconfigure((0,1), weight = 1)
        self.obj_lvl2.rightPlotsImgFrame.columnconfigure((0), weight = 1)
        self.obj_lvl2.bottomSliderFrame.rowconfigure((0,1), weight = 1)
        self.obj_lvl2.bottomSliderFrame.columnconfigure((0,1,2,3), weight = 1)
        

        # if the img_dir_record is empty. show the welcome image
        if os.path.exists(img_dir_record_path) and os.path.getsize(img_dir_record_path) == 0:
            
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
        
        elif os.path.exists(img_dir_record_path) and os.path.getsize(img_dir_record_path) > 0:
            with open(img_dir_record_path, 'r') as f:
                self.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.leftOriginalImgFrame, 
                        bg = self.rgbValues(),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand =True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: full_image(event,self.obj_lvl2 , self.obj_lvl2 .tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: getresizedImageCoordinates(event,self.obj_lvl2 ,canvas = homeCanvas, image = self.obj_lvl2.tk_image))

        
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


    
