import os
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.data_preprocessing_utils import *
from utils.io_utils import *
from utils.variables_utils import *


class Preprocess(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent

    def preprocessing_window(self):
        
        # Clear self.work_area_frame
        for widget in self.parent.parent.work_area_frame.winfo_children():
            widget.destroy()

        ## children to workMenuFrame 
        self.parent.parent.left_buttons_pre_pro_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        self.parent.parent.left_buttons_pre_pro_frame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        self.parent.parent.middle_pre_pro_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        self.parent.parent.middle_pre_pro_frame.place(relx = 0.2, y = 0, relwidth = 0.4, relheight = 1)
        self.parent.parent.right_pre_pro_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        self.parent.parent.right_pre_pro_frame.place(relx = 0.6, y = 0, relwidth = 0.4, relheight = 1)
    

        self.parent.parent.left_buttons_pre_pro_frame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.right_pre_pro_frame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.right_pre_pro_frame.columnconfigure((0,1), weight = 1)
        
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods
        
        self.parent.parent.pre_pro_options_input = self.parent.parent.ctk.CTkLabel(master = self.parent.parent.left_buttons_pre_pro_frame,
                                               text = "Input: Raw Data. \nSelect filters as forward feed. \nSelect None (pass) to skip filter.")
        self.parent.parent.pre_pro_options_input.grid(row = 0, column = 0, sticky='ew', padx = 30, pady =(50,0))
        


        self.parent.parent.pre_pro_options_1 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.left_buttons_pre_pro_frame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization"],
                                                command = lambda selection: self.pre_processing_pipe_line_selection("option1", selection))
        
        self.parent.parent.pre_pro_options_1.set("Filter 1")
        self.parent.parent.pre_pro_options_1.grid(row = 1, column = 0, sticky='ew', padx = 30, pady =(0,5))
   
        
        self.parent.parent.pre_pro_options_2 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.left_buttons_pre_pro_frame,
                                                values = ["Standard Normal Variate", 
                                                          
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.pre_processing_pipe_line_selection("option2", selection))
        self.parent.parent.pre_pro_options_2.set("Filter 2")
        self.parent.parent.pre_pro_options_2.grid(row = 2, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.pre_pro_options_3 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.left_buttons_pre_pro_frame,
                                                values = ["Standard Normal Variate", 
                                                         
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.pre_processing_pipe_line_selection("option3", selection))
        self.parent.parent.pre_pro_options_3.set("Filter 3")
        self.parent.parent.pre_pro_options_3.grid(row = 3, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.pre_pro_options_4 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.left_buttons_pre_pro_frame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.pre_processing_pipe_line_selection("option4", selection))
        self.parent.parent.pre_pro_options_4.set("Filter 4")
        self.parent.parent.pre_pro_options_4.grid(row = 4, column = 0, sticky='ew', padx = 30, pady =(0,5))
        

        

    
        self.parent.parent.pre_pro_options_output = self.parent.parent.ctk.CTkLabel(master = self.parent.parent.left_buttons_pre_pro_frame,
                                               text = "Output: Preprocessed Data")
        self.parent.parent.pre_pro_options_output.grid(row = 5, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.pre_pro_apply_button = self.parent.parent.ctk.CTkButton(master=self.parent.parent.left_buttons_pre_pro_frame, 
                                                    text="Apply Preprocessing", 
                                                    command = self.apply_preprocessing)
        self.parent.parent.pre_pro_apply_button.grid(row = 6, column = 0, sticky='ew', padx = 30, pady = (0,5))
        
        self.parent.parent.pre_pro_save_button = self.parent.parent.ctk.CTkButton(master=self.parent.parent.left_buttons_pre_pro_frame, 
                                                    text="Save Preprocessed Data", 
                                                    command = self.save_preprocessed_data)
        self.parent.parent.pre_pro_save_button.grid(row = 7, column = 0, sticky='ew', padx = 30, pady = (0,50))
        

        # raw spectral plot in preprocessing window
        self.raw_plot_fig, self.raw_plot_fig_ax = plt.subplots(figsize =(10,10), dpi =40)
        self.raw_plot_fig.set_facecolor(self.parent.parent.rgbValues())
        self.raw_plot_fig_ax.set_facecolor(self.parent.parent.rgbValues())
        self.raw_plot_fig_ax.set_title("Raw Spectral Signature",fontsize =40)
        self.raw_plot_fig_ax.set_xlabel("Wavelength",fontsize =40)
        self.raw_plot_fig_ax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.raw_plot_fig_ax.tick_params(axis='both', which='major', labelsize=20)
        self.raw_plot_fig_canvas = FigureCanvasTkAgg(self.raw_plot_fig, master= self.parent.parent.middle_pre_pro_frame)
        self.raw_plot_fig_canvas.get_tk_widget().pack(expand = True, fill ='x')
        
        # preprocessed spectral plot in preprocessing window
        self.pre_processed_plot_fig, self.pre_processed_plot_fig_ax = plt.subplots(figsize =(10,10), dpi = 40)
        self.pre_processed_plot_fig.set_facecolor(self.parent.parent.rgbValues())
        self.pre_processed_plot_fig_ax.set_facecolor(self.parent.parent.rgbValues())
        self.pre_processed_plot_fig_ax.set_title("Preprocessed Signature",fontsize =40)
        self.pre_processed_plot_fig_ax.set_xlabel("Wavelength",fontsize =40)
        self.pre_processed_plot_fig_ax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.pre_processed_plot_fig_ax.tick_params(axis='both', which='major', labelsize=20)
        self.pre_processed_plot_fig_canvas = FigureCanvasTkAgg(self.pre_processed_plot_fig, master= self.parent.parent.right_pre_pro_frame)
        self.pre_processed_plot_fig_canvas.get_tk_widget().pack(expand = True, fill ='x')
        
        if self.parent.parent.raw_img_dir == None:
            pass
        else:
            self.raw_spectral_plot(self.parent.unfolded_data)

    def pre_processing_pipe_line_selection(self, source, selection):
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

    def apply_preprocessing(self):

        
        def preprocessing_in_thread():
            sg_win_size_pre_pro = self.parent.parent.default_properties.get("sg_win_size_pre_pro")
            sg_poly_order_pre_pro = self.parent.parent.default_properties.get("sg_poly_order_pre_pro")

            self.parent.load_data_text = 'Loading...'
            
            self.parent.load_data_text = f'Applying {self.filter1} ...'
            filter1data = preprocessing(self.filter1, self.parent.unfolded_data,w = sg_win_size_pre_pro,p = sg_poly_order_pre_pro)
            self.parent.load_data_text = f'Applying {self.filter2} ...'
            filter2data = preprocessing(self.filter2, filter1data,w = sg_win_size_pre_pro,p = sg_poly_order_pre_pro)
            self.parent.load_data_text = f'Applying {self.filter3} ...'
            filter3data = preprocessing(self.filter3, filter2data,w = sg_win_size_pre_pro,p = sg_poly_order_pre_pro)
            self.parent.load_data_text = f'Applying {self.filter4} ...'
            self.preprocessedData = preprocessing(self.filter4, filter3data,w = sg_win_size_pre_pro,p = sg_poly_order_pre_pro)
            self.parent.load_data_text = f'Plotting preprocessed spectra ...'
            self.preprocessed_spectral_plot(self.preprocessedData)
            self.Dataloaded = True

        
        if self.parent.unfolded_data is None:
                messagebox.showinfo("Info", "Please load a data first.")
                return
        self.Dataloaded = False
        threading.Thread(target = preprocessing_in_thread).start()
        self.parent.data_loading_screen()

    
    def save_preprocessed_data(self):
        self.Dataloaded = False
        
        self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.csv',
                                               filetypes = [("Comma Separated Values", "*.csv"),
                                                            ("Text File", ".txt"),
                                                            ("Numpy Array", "*.npy"),
                                                            ])
        if self.saveFile is not None:
            self.load_data_text = f'Saving preprocessed data ...'
            threading.Thread(target = self.setDataloader).start()
            self.data_loading_screen()
            self.saveFile.close()

    def raw_spectral_plot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.raw_plot_fig_ax.clear()
        for i, row in enumerate(selected_rows):
            self.raw_plot_fig_ax.plot(np.arange(0, self.parent.parent.default_properties.get("no_of_bands_EMR")), row, label=f'Row {indices[i]}')
        self.raw_plot_fig_ax.set_title("Raw Spectral Signature",fontsize =40)
        self.raw_plot_fig_ax.set_xlabel("Wavelength",fontsize =40)
        self.raw_plot_fig_ax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.raw_plot_fig_ax.tick_params(axis='both', which='major', labelsize=20)
        self.raw_plot_fig_canvas.draw()

    def preprocessed_spectral_plot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.pre_processed_plot_fig_ax.clear()
        for i, row in enumerate(selected_rows):
            self.pre_processed_plot_fig_ax.plot(np.arange(0, self.parent.parent.default_properties.get('no_of_bands_EMR')), row, label=f'Row {indices[i]}')
        self.pre_processed_plot_fig_ax.set_title("Preprocessed Signature",fontsize =40)
        self.pre_processed_plot_fig_ax.set_xlabel("Wavelength",fontsize =40)
        self.pre_processed_plot_fig_ax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.pre_processed_plot_fig_ax.tick_params(axis='both', which='major', labelsize=20)
        self.pre_processed_plot_fig_canvas.draw()