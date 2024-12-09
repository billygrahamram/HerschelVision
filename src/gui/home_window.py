from utils.variables_utils import *
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk


class HomeWindow(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.home_menu()

    def home_menu(self):
        # method to show the home window.
        
        # Clear self.workAreaFrame
        for widget in self.parent.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.parent.leftOriginalImgFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        self.parent.rightPlotsImgFrame   = ctk.CTkFrame(master = self.parent.workAreaFrame)
        self.parent.bottomSliderFrame    = ctk.CTkFrame(master = self.parent.workAreaFrame)

        
        self.parent.leftOriginalImgFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.rightPlotsImgFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.bottomSliderFrame.place(rely = 0.9, y = 0, relwidth = 1, relheight = 0.1)


        self.parent.rightPlotsImgFrame.rowconfigure((0,1), weight = 1)
        self.parent.rightPlotsImgFrame.columnconfigure((0), weight = 1)
        self.parent.bottomSliderFrame.rowconfigure((0,1), weight = 1)
        self.parent.bottomSliderFrame.columnconfigure((0,1,2,3), weight = 1)
        

        
        if self.parent.start_app or self.parent.Dataloaded==False:
            print("first time start")
            
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
            else:
                welcomeImg = Image.open(darkThemeImgPath)
                

            homeCanvas = ctk.CTkCanvas(self.parent.leftOriginalImgFrame, 
                            bg = self.parent.rgbValues(),
                            bd = 0,
                            highlightthickness=0,
                            relief='ridge')
            
            homeCanvas.pack( expand =True, fill='both')
            homeCanvas.bind('<Configure>',lambda event: self.parent.full_image(event, welcomeImg, canvas=homeCanvas))

            self.parent.start_app = False
            self.parent.raw_img_dir == None
        
        else:
            with open(img_dir_record_path, 'r') as f:
                print("not first time start")
                self.parent.raw_img_dir = f.read().strip()
                homeCanvas = ctk.CTkCanvas(self.parent.leftOriginalImgFrame, 
                        bg = self.parent.rgbValues(),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                homeCanvas.pack(expand =True, fill='both')
                homeCanvas.bind('<Configure>',lambda event: self.parent.full_image(event, self.parent.tk_image, canvas=homeCanvas))
                homeCanvas.bind('<1>', lambda event: self.parent.getresizedImageCoordinates(event,canvas = homeCanvas, image = self.parent.tk_image))

        print(self.parent.default_properties)
        noOfBandsEMR = self.parent.default_properties.get('noOfBandsEMR')
        
        #### wavelength plot ######
        self.parent.wavelengthPlotFig, self.parent.wavelengthPlotFigax = plt.subplots()
        self.parent.wavelengthPlotFig.set_facecolor(self.parent.rgbValues())
        self.parent.wavelengthPlotFigax.set_facecolor(self.parent.rgbValues())
        self.parent.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.parent.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.parent.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.parent.wavelengthPlotFigCanvas = FigureCanvasTkAgg(self.parent.wavelengthPlotFig, master= self.parent.rightPlotsImgFrame)
        self.parent.wavelengthPlotFigCanvas.get_tk_widget().grid(row = 0, column = 0, sticky= 'nsew')

        #### scatter plot ######
        self.parent.scatterPlotFig, self.parent.scatterPlotFigax = plt.subplots()
        self.parent.scatterPlotFig.set_facecolor(self.parent.rgbValues())
        self.parent.scatterPlotFigax.set_facecolor(self.parent.rgbValues())
        self.parent.scatterPlotFigax.set_title("Scatter Plot")
        self.parent.scatterPlotFigax.set_xlabel("Band 1")
        self.parent.scatterPlotFigax.set_ylabel("Band 2")
        self.parent.scatterPlotFigCanvas = FigureCanvasTkAgg(self.parent.scatterPlotFig, master= self.parent.rightPlotsImgFrame)
        self.parent.scatterPlotFigCanvas.get_tk_widget().grid(row= 1, column=0,  sticky='nsew')
        
        
        # wavelength slider
        self.parent.wavelengthSliderCurrentValueLabel = self.parent.ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.wavelengthSliderCurrentValueLabel.grid(row = 0, column = 0, columnspan = 2, padx = (100,5))
        self.parent.wavelengthSlider = self.parent.ctk.CTkSlider(self.parent.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20,command = self.parent.wavelengthsSlider_event)
        self.parent.wavelengthSlider.grid(row = 1, column = 0, columnspan=2, padx = (100,5))
        print(self.parent.raw_img_dir)
        self.parent.wavelengthsSlider_event()

        # band 1 slider
        self.parent.band1ScatterSliderCurrentValueLabel = self.parent.ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.band1ScatterSliderCurrentValueLabel.grid(row = 0, column =2, padx = (100,5))
        self.parent.band1ScatterSlider = self.parent.ctk.CTkSlider(self.parent.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20, command = self.parent.band1ScatterSlider_event)
        self.parent.band1ScatterSlider.grid(row =1, column =2, padx = (100,5))
        self.parent.band1ScatterSlider_event()

        # band 2 slider
        self.parent.band2ScatterSliderCurrentValueLabel = self.parent.ctk.CTkLabel(self.parent.bottomSliderFrame, text = "", justify ="center")
        self.parent.band2ScatterSliderCurrentValueLabel.grid(row = 0, column =3, padx = (5,100))
        self.parent.band2ScatterSlider = self.parent.ctk.CTkSlider(self.parent.bottomSliderFrame, from_ = 0, to = noOfBandsEMR-1, height = 20, command = self.parent.band2ScatterSlider_event)
        self.parent.band2ScatterSlider.grid(row =1, column=3, padx=(5,100))
        self.parent.band2ScatterSlider_event()

        #add show rgb image button
        self.parent.show_image_button = self.parent.ctk.CTkButton(self, text="Show RGB Image", command=self.parent.show_psuedo_rgb)
        #self.parent.show_image_button.grid(row=1, column=4, padx=(10, 5), pady=(10, 5), sticky="e")  # Place the button above the label
        self.parent.show_image_button.grid(row=0, column=5, columnspan=2, pady=(10, 5), sticky="n")  # Center button at the top