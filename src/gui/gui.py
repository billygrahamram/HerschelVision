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
from tkinter import  messagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_properties =  parse_properties('resources/config/default_config.property')
        self.raw_img_dir = None
        self.Dataloaded = False
        self.start_app = True
        self.ctk = ctk
        self.spectral_array = None

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
                            bg = self.rgbValues(),
                            bd = 0,
                            highlightthickness = 0,
                            relief = 'ridge')
        
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            openCanvas.pack(expand =True, fill='both')        
            openCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: self.getresizedImageCoordinates(event, canvas = openCanvas, image = self.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    
    def band1ScatterSlider_event(self,value=150):
        if self.raw_img_dir== None:
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

    def band2ScatterSlider_event(self,value=150):
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

    def wavelengthPlot(self,scaled_imgX,scaled_imgY):
        reflectance = self.spectral_array[int(scaled_imgY), int(scaled_imgX), :]
        self.wavelengthPlotFigax.clear()
        self.wavelengthPlotFigax.plot(np.arange(0, self.default_properties.get("noOfBandsEMR")), reflectance)
        self.wavelengthPlotFigax.set_title("Wavelength Plot")
        self.wavelengthPlotFigax.set_xlabel("Wavelength")
        self.wavelengthPlotFigax.set_ylabel("Reflectance")
        self.wavelengthPlotFigCanvas.draw()

    def show_psuedo_rgb(self):
            if self.spectral_array is None:
                messagebox.showinfo("Info", "Please load an image first.")
                return
            rgb = create_pseudo_rgb(self.spectral_array)
            self.tk_image = Image.fromarray(np.uint8(rgb))

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
