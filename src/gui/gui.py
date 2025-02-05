#####################################################################################
## Author: Billy G. Ram
## Refactored BY: Sunil GC
## Linkedin: https://www.linkedin.com/in/billygrahamram/
## Twitter: https://twitter.com/billygrahamram
## Github: https://github.com/billygrahamram
## This code solely belongs to Billy G. Ram and is currently NOT open sourced. 
#####################################################################################

from tkinter import messagebox

import customtkinter as ctk

from gui.home_window import Home_window
from gui.main_menu import Main_menu  # Import the Main_menu subclass
from utils.config_parser import *
from utils.data_preprocessing_utils import *
from utils.variables_utils import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_properties =  parse_properties('resources/config/default_config.property')
        self.raw_img_dir = None
        self.Dataloaded = False
        self.start_app = True
        self.ctk = ctk
        self.spectral_array = None
        self.running = True

        self.title(self.default_properties.get("title"))
        self.geometry(self.default_properties.get("geometry"))
        self.minsize(self.default_properties.get("min_size"),self.default_properties.get("min_size"))
        self.resizable(width=True, height=True)

        # Empty the img_dir_record.txt file at startup. Opens and closes it, making the file empty.
        with open(img_dir_record_path, 'w') as f:
            pass

         ## children to main window
        self.menu_bar_frame = ctk.CTkFrame(self)
        self.work_area_frame = ctk.CTkFrame(self)

        self.menu_bar_frame.place(x=0, y=0, relwidth = 1, relheight = 0.05)
        self.work_area_frame.place(rely = 0.05, y =0, relwidth =1, relheight =0.95)

        # set default values
        self.band_1_value = 150
        self.band_2_value = 150

        # Instantiate subclasses
        self.main_menu = Main_menu(self)
        self.home_window = Home_window(self)

    def run(self):
        self.mainloop()

    def wavelengths_slider_event(self,value=150):
        if self.raw_img_dir == None or self.Dataloaded==False:
            pass
        else:
            value = int(float(value))
            single_band_img = single_band(self.spectral_array, int(value))
            self.tk_image = Image.fromarray(np.uint8(single_band_img))

            # updates the current slider value
            self.wavelength_slider_current_value_label.configure(text= "Current Wavelength: " + str(int(value)))
            
            # destroy the left frame for new image
            for widget in self.left_original_Img_frame.winfo_children():
                widget.destroy()
            
            openCanvas = ctk.CTkCanvas(self.left_original_Img_frame, 
                            bg = self.rgbValues(),
                            bd = 0,
                            highlightthickness = 0,
                            relief = 'ridge')
        
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            openCanvas.pack(expand =True, fill='both')        
            openCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas = openCanvas))
            openCanvas.bind('<1>', lambda event: self.get_resized_image_coordinates(event, canvas = openCanvas, image = self.tk_image))
            # canvas.bind is being used to call the self.full_image function whenever the <Configure> event occurs. 
            # The <Configure> event is triggered whenever the widget changes size, so this code is saying “whenever the canvas changes size, 
            # run the self.full_image function”.
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    
    def band_1_scatter_slider_event(self,value=150):
        if self.raw_img_dir== None or self.Dataloaded==False:
            pass
        else:
            self.band_1_scatter_slider_current_value_label.configure(text = "First Band: " + str(int(value)))
            self.band_1_value = int(value)
            self.scatter_plot_fig_ax.clear()
            self.scatter_plot_fig_ax.scatter(self.kmeansData[:, self.band_1_value], 
                                          self.kmeansData[:, self.band_2_value], 
                                          c=self.kmeanslabels, s=10)
            self.scatter_plot_fig_ax.set_title("Scatter Plot")
            self.scatter_plot_fig_ax.set_xlabel("Band 1")
            self.scatter_plot_fig_ax.set_ylabel("Band 2")
            self.scatter_plot_fig_ax.figure.canvas.draw()

    def band_2_scatter_slider_event(self,value=150):
            if self.raw_img_dir == None or self.Dataloaded==False:
                pass
            else:
                self.band_2_scatter_slider_current_value_label.configure(text= "Second Band: " + str(int(value)))
                self.band_2_value = int(value)
                self.scatter_plot_fig_ax.clear()
                self.scatter_plot_fig_ax.scatter(self.kmeansData[:, self.band_1_value], 
                                            self.kmeansData[:, self.band_2_value], 
                                            c=self.kmeanslabels, s=10)
                self.scatter_plot_fig_ax.set_title("Scatter Plot")
                self.scatter_plot_fig_ax.set_xlabel("Band 1")
                self.scatter_plot_fig_ax.set_ylabel("Band 2")
                self.scatter_plot_fig_ax.figure.canvas.draw()

    def rgbValues(self):
    
        if ctk.get_appearance_mode() == 'Light':
            color = self.work_area_frame.cget('fg_color')[0]
        else:
            color = self.work_area_frame.cget('fg_color')[1]
            
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


    def get_resized_image_coordinates(self,event, canvas, image):
    
    
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
                self.wavelength_plot(scaled_imgX, scaled_imgY)
                
        
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
                self.wavelength_plot(scaled_imgX, scaled_imgY)

    def wavelength_plot(self,scaled_imgX,scaled_imgY):
        reflectance = self.spectral_array[int(scaled_imgY), int(scaled_imgX), :]
        self.wavelength_plot_fig_ax.clear()
        self.wavelength_plot_fig_ax.plot(np.arange(0, self.default_properties.get("no_of_bands_EMR")), reflectance)
        self.wavelength_plot_fig_ax.set_title("Wavelength Plot")
        self.wavelength_plot_fig_ax.set_xlabel("Wavelength")
        self.wavelength_plot_fig_ax.set_ylabel("Reflectance")
        self.wavelength_plot_fig_canvas.draw()

    def show_psuedo_rgb(self):
            if self.spectral_array is None:
                messagebox.showinfo("Info", "Please load an image first.")
                return
            rgb = create_pseudo_rgb(self.spectral_array)
            self.tk_image = Image.fromarray(np.uint8(rgb))

            if hasattr(self, 'left_original_Img_frame') and self.left_original_Img_frame.winfo_exists():
                # Destroy all children of the left frame safely
                for widget in self.left_original_Img_frame.winfo_children():
                    if widget.winfo_exists():
                        widget.destroy()  # Destroy the widget if it exists
            
                        openCanvas = ctk.CTkCanvas(self.left_original_Img_frame, 
                                        bg = self.rgbValues(),
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = 'ridge')
                        openCanvas.pack(expand =True, fill='both')        
                        openCanvas.bind('<Configure>',lambda event: self.full_image(event, self.tk_image, canvas = openCanvas))
                        openCanvas.bind('<1>', lambda event: self.get_resized_image_coordinates(event, canvas = openCanvas, image = self.tk_image))
