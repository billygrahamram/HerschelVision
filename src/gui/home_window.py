import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

from utils.variables_utils import *


class Home_window(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.home_menu()

    def home_menu(self):
        # method to show the home window.
        
        # Clear self.work_area_frame
        for widget in self.parent.work_area_frame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.parent.left_original_Img_frame = ctk.CTkFrame(master = self.parent.work_area_frame)
        self.parent.right_plots_img_frame   = ctk.CTkFrame(master = self.parent.work_area_frame)
        self.parent.bottom_slider_frame    = ctk.CTkFrame(master = self.parent.work_area_frame)

        
        self.parent.left_original_Img_frame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.right_plots_img_frame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        self.parent.bottom_slider_frame.place(rely = 0.9, y = 0, relwidth = 1, relheight = 0.1)


        self.parent.right_plots_img_frame.rowconfigure((0,1), weight = 1)
        self.parent.right_plots_img_frame.columnconfigure((0), weight = 1)
        self.parent.bottom_slider_frame.rowconfigure((0,1), weight = 1)
        self.parent.bottom_slider_frame.columnconfigure((0,1,2,3), weight = 1)
        

        
        if self.parent.start_app or self.parent.Dataloaded==False:
            print("first time start")
            
            if ctk.get_appearance_mode() == 'Light': 
                welcomeImg = Image.open(lightThemeImgPath)
            else:
                welcomeImg = Image.open(dark_theme_img_path)
                

            home_canvas = ctk.CTkCanvas(self.parent.left_original_Img_frame, 
                            bg = self.parent.rgbValues(),
                            bd = 0,
                            highlightthickness=0,
                            relief='ridge')
            
            home_canvas.pack( expand =True, fill='both')
            home_canvas.bind('<Configure>',lambda event: self.parent.full_image(event, welcomeImg, canvas=home_canvas))

            self.parent.start_app = False
            self.parent.raw_img_dir == None
        
        else:
            with open(img_dir_record_path, 'r') as f:
                print("not first time start")
                self.parent.raw_img_dir = f.read().strip()
                home_canvas = ctk.CTkCanvas(self.parent.left_original_Img_frame, 
                        bg = self.parent.rgbValues(),
                        bd = 0,
                        highlightthickness=0,
                        relief='ridge')
        
                home_canvas.pack(expand =True, fill='both')
                home_canvas.bind('<Configure>',lambda event: self.parent.full_image(event, self.parent.tk_image, canvas=home_canvas))
                home_canvas.bind('<1>', lambda event: self.parent.get_resized_image_coordinates(event,canvas = home_canvas, image = self.parent.tk_image))

        print(self.parent.default_properties)
        no_of_bands_EMR = self.parent.default_properties.get('no_of_bands_EMR')
        
        #### wavelength plot ######
        self.parent.wavelength_plotFig, self.parent.wavelength_plot_fig_ax = plt.subplots()
        self.parent.wavelength_plotFig.set_facecolor(self.parent.rgbValues())
        self.parent.wavelength_plot_fig_ax.set_facecolor(self.parent.rgbValues())
        self.parent.wavelength_plot_fig_ax.set_title("Wavelength Plot")
        self.parent.wavelength_plot_fig_ax.set_xlabel("Wavelength")
        self.parent.wavelength_plot_fig_ax.set_ylabel("Reflectance")
        self.parent.wavelength_plot_fig_canvas = FigureCanvasTkAgg(self.parent.wavelength_plotFig, master= self.parent.right_plots_img_frame)
        self.parent.wavelength_plot_fig_canvas.get_tk_widget().grid(row = 0, column = 0, sticky= 'nsew')

        #### scatter plot ######
        self.parent.scatterPlotFig, self.parent.scatter_plot_fig_ax = plt.subplots()
        self.parent.scatterPlotFig.set_facecolor(self.parent.rgbValues())
        self.parent.scatter_plot_fig_ax.set_facecolor(self.parent.rgbValues())
        self.parent.scatter_plot_fig_ax.set_title("Scatter Plot")
        self.parent.scatter_plot_fig_ax.set_xlabel("Band 1")
        self.parent.scatter_plot_fig_ax.set_ylabel("Band 2")
        self.parent.scatterPlotFigCanvas = FigureCanvasTkAgg(self.parent.scatterPlotFig, master= self.parent.right_plots_img_frame)
        self.parent.scatterPlotFigCanvas.get_tk_widget().grid(row= 1, column=0,  sticky='nsew')
        
        
        # wavelength slider
        self.parent.wavelength_slider_current_value_label = self.parent.ctk.CTkLabel(self.parent.bottom_slider_frame, text = "", justify ="center")
        self.parent.wavelength_slider_current_value_label.grid(row = 0, column = 0, columnspan = 2, padx = (100,5))
        self.parent.wavelengthSlider = self.parent.ctk.CTkSlider(self.parent.bottom_slider_frame, from_ = 0, to = no_of_bands_EMR-1, height = 20,command = self.parent.wavelengths_slider_event)
        self.parent.wavelengthSlider.grid(row = 1, column = 0, columnspan=2, padx = (100,5))
        print(self.parent.raw_img_dir)
        self.parent.wavelengths_slider_event()

        # band 1 slider
        self.parent.band_1_scatter_slider_current_value_label = self.parent.ctk.CTkLabel(self.parent.bottom_slider_frame, text = "", justify ="center")
        self.parent.band_1_scatter_slider_current_value_label.grid(row = 0, column =2, padx = (100,5))
        self.parent.band_1_scatter_slider = self.parent.ctk.CTkSlider(self.parent.bottom_slider_frame, from_ = 0, to = no_of_bands_EMR-1, height = 20, command = self.parent.band_1_scatter_slider_event)
        self.parent.band_1_scatter_slider.grid(row =1, column =2, padx = (100,5))
        self.parent.band_1_scatter_slider_event()

        # band 2 slider
        self.parent.band_2_scatter_slider_current_value_label = self.parent.ctk.CTkLabel(self.parent.bottom_slider_frame, text = "", justify ="center")
        self.parent.band_2_scatter_slider_current_value_label.grid(row = 0, column =3, padx = (5,100))
        self.parent.band_2_scatter_slider = self.parent.ctk.CTkSlider(self.parent.bottom_slider_frame, from_ = 0, to = no_of_bands_EMR-1, height = 20, command = self.parent.band_2_scatter_slider_event)
        self.parent.band_2_scatter_slider.grid(row =1, column=3, padx=(5,100))
        self.parent.band_2_scatter_slider_event()

        #add show rgb image button
        self.parent.show_image_button = self.parent.ctk.CTkButton(self, text="Show RGB Image", command=self.parent.show_psuedo_rgb)
        #self.parent.show_image_button.grid(row=1, column=4, padx=(10, 5), pady=(10, 5), sticky="e")  # Place the button above the label
        self.parent.show_image_button.grid(row=0, column=5, columnspan=2, pady=(10, 5), sticky="n")  # Center button at the top