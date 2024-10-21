#####################################################################################
## Author: Billy G. Ram
## Refactored BY: Sunil GC
## Linkedin: https://www.linkedin.com/in/billygrahamram/
## Twitter: https://twitter.com/billygrahamram
## Github: https://github.com/billygrahamram
## This code solely belongs to Billy G. Ram and is currently NOT open sourced. 
#####################################################################################

import customtkinter as ctk
from utils.config_parser import *
from utils.variables_utils import *
from utils.data_preprocessing_utils import *
from common.common_utils import *
from gui.main_menu import MainMenu  # Import the MainMenu subclass
from gui.home_window import HomeWindow 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_properties =  parse_properties('resources/config/default_config.property')
        self.raw_img_dir = None
        self.Dataloaded = False
        self.start_app = True
        self.ctk = ctk

        self.title(self.default_properties.get("title"))
        self.geometry(self.default_properties.get("geometry"))
        self.minsize(self.default_properties.get("min_size"),self.default_properties.get("min_size"))
        self.resizable(width=True, height=True)

        # Empty the img_dir_record.txt file at startup. Opens and closes it, making the file empty.
        with open(img_dir_record_path, 'w') as f:
            pass

         ## children to main window
        self.menuBarFrame = ctk.CTkFrame(self)
        self.workAreaFrame = ctk.CTkFrame(self)

        self.menuBarFrame.place(x=0, y=0, relwidth = 1, relheight = 0.05)
        self.workAreaFrame.place(rely = 0.05, y =0, relwidth =1, relheight =0.95)

        # set default values
        self.band1Value = 150
        self.band2Value = 150

        # Instantiate subclasses
        self.main_menu = MainMenu(self)
        self.home_window = HomeWindow(self)

    def run(self):
        self.mainloop()

    def wavelengthsSlider_event(self,value=150):

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
                            bg = rgbValues(self),
                            bd = 0,
                            highlightthickness = 0,
                            relief = 'ridge')
        
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            openCanvas.pack(expand =True, fill='both')        
            openCanvas.bind('<Configure>',lambda event: full_image(event,self, self.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: getresizedImageCoordinates(event,self, canvas = openCanvas, image = mobj.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    

