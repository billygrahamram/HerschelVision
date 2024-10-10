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
        self.home_menu()

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
        print(os.path.exists(img_dir_record_path))
        print(os.path.getsize(img_dir_record_path))
        if os.path.exists(img_dir_record_path) and os.path.getsize(img_dir_record_path) == 0:
            print("&&&&&&&&&&&&&&&&&&&&&&77")
            
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
            else:
                welcomeImg = Image.open(darkThemeImgPath)
                

            homeCanvas = ctk.CTkCanvas(self.obj_lvl2.leftOriginalImgFrame, 
                            bg = rgbValues(self.obj_lvl2),
                            bd = 0,
                            highlightthickness=0,
                            relief='ridge')
            
            homeCanvas.pack( expand =True, fill='both')
            homeCanvas.bind('<Configure>',lambda event: full_image(event,self.obj_lvl2, welcomeImg, canvas=homeCanvas))
        
        elif os.path.exists(img_dir_record_path) and os.path.getsize(img_dir_record_path) > 0:
            with open(img_dir_record_path, 'r') as f:
                print("&&&&&&&&&&&&&&&&333&&&&&&77")
                self.obj_lvl2.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.obj_lvl2.leftOriginalImgFrame, 
                        bg = rgbValues(self.obj_lvl2),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand =True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: full_image(event,self.obj_lvl2 , self.obj_lvl2 .tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: getresizedImageCoordinates(event,self.obj_lvl2 ,canvas = homeCanvas, image = self.obj_lvl2.tk_image))

        
        noOfBandsEMR = self.obj_lvl2.default_properties.get('noOfBandsEMR')
        
        #### wavelength plot ######
        self.obj_lvl2.wavelengthPlotFig, self.obj_lvl2.wavelengthPlotFigax = plt.subplots()
        self.obj_lvl2.wavelengthPlotFig.set_facecolor(rgbValues(self.obj_lvl2))
        self.obj_lvl2.wavelengthPlotFigax.set_facecolor(rgbValues(self.obj_lvl2))
        self.obj_lvl2.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.obj_lvl2.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.obj_lvl2.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.obj_lvl2.wavelengthPlotFigCanvas = FigureCanvasTkAgg(self.obj_lvl2.wavelengthPlotFig, master= self.obj_lvl2.rightPlotsImgFrame)
        self.obj_lvl2.wavelengthPlotFigCanvas.get_tk_widget().grid(row = 0, column = 0, sticky= 'nsew')

        #### scatter plot ######
        self.obj_lvl2.scatterPlotFig, self.obj_lvl2.scatterPlotFigax = plt.subplots()
        self.obj_lvl2.scatterPlotFig.set_facecolor(rgbValues(self.obj_lvl2))
        self.obj_lvl2.scatterPlotFigax.set_facecolor(rgbValues(self.obj_lvl2))
        self.obj_lvl2.scatterPlotFigax.set_title("Scatter Plot")
        self.obj_lvl2.scatterPlotFigax.set_xlabel("Band 1")
        self.obj_lvl2.scatterPlotFigax.set_ylabel("Band 2")
        self.obj_lvl2.scatterPlotFigCanvas = FigureCanvasTkAgg(self.obj_lvl2.scatterPlotFig, master= self.obj_lvl2.rightPlotsImgFrame)
        self.obj_lvl2.scatterPlotFigCanvas.get_tk_widget().grid(row= 1, column=0,  sticky='nsew')
        
        
        # wavelength slider
        self.obj_lvl2.wavelengthSliderCurrentValueLabel = ctk.CTkLabel(self.obj_lvl2.bottomSliderFrame, text = "", justify ="center")
        self.obj_lvl2.wavelengthSliderCurrentValueLabel.grid(row = 0, column = 0, columnspan = 2, padx = (100,5))
        self.obj_lvl2.wavelengthSlider = ctk.CTkSlider(self.obj_lvl2.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20,command = wavelengthsSlider_event)
        self.obj_lvl2.wavelengthSlider.grid(row = 1, column = 0, columnspan=2, padx = (100,5))
        wavelengthsSlider_event(self.obj_lvl2)

    
