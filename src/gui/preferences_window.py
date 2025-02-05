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


class Preference_windows(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent

    def preferences_window(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
        
        def Preprocessing_button_callback():
            
            def save_pre_pro_setting():
                self.parent.parent.default_properties["sg_win_size_pre_pro"] = int(pp_sg_win_size_entry.get())
                self.parent.parent.default_properties["sg_poly_order_pre_pro "] = int(pp_sg_win_size_entry.get())  
                
                print(f"SG Window Size: {self.parent.parent.default_properties.get('sg_win_size_pre_pro')}")
                print(f"SG Poly Order: {self.parent.parent.default_properties.get('sg_poly_order_pre_pro')}")
                
                
            # Clear rightFormFrame
            for widget in right_preference_form_frame.winfo_children():
                widget.destroy()
            right_preference_form_frame.update()
            
            Preprocessing_form = self.parent.parent.ctk.CTkFrame(master = right_preference_form_frame,
                                             border_width= 1,
                                            )
            Preprocessing_form.pack(side = 'left', fill = 'both', expand = True)
        

            pp_sg_win_size_label = self.parent.parent.ctk.CTkLabel(master = Preprocessing_form, text = "Enter Window Size for Savitzky Golay (odd number):  ", anchor = 'w')
            pp_sg_win_size_entry = self.parent.parent.ctk.CTkEntry(master = Preprocessing_form, placeholder_text="Enter window size" )
            pp_sg_poly_order_label = self.parent.parent.ctk.CTkLabel(master = Preprocessing_form, text = "Enter Polynomial Order for Savitzky Golay (< Window size):  ", anchor = 'w')
            pp_sg_poly_order_entry = self.parent.parent.ctk.CTkEntry(master = Preprocessing_form, placeholder_text="Enter polynomial order" )
            save_pre_pro_settings = self.parent.parent.ctk.CTkButton(master=right_bottom_apply_buttom_frame, text="Apply", command=save_pre_pro_setting)
           
            
            
            pp_sg_win_size_label.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            pp_sg_win_size_entry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            pp_sg_poly_order_label.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            pp_sg_poly_order_entry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            save_pre_pro_settings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            

        
            
        def segmentation_button_callback():
            
            def save_segmentation_setting():
                  
                self.parent.parent.default_properties["kcluster_no_seg_pre_pro"]  = int(seg_kcluster_entry.get())
                self.parent.parent.default_properties["kcluster_thres_pre_pro"] = int(seg_thres_entry.get())
                self.parent.parent.default_properties["selected_SAM_model "]  = str(seg_SAM_model_options.get())
                self.parent.parent.default_properties["default_segmentation_method "] = str(seg_default_method_options.get())

                print("K-cluster No Seg PrePro: ", self.parent.parent.default_properties.get('kcluster_no_seg_pre_pro'))
                print("K-Cluster Thres PrePro: ", self.parent.parent.default_properties.get('kcluster_thres_pre_pro'))
                print("Selected SAM Model: ", self.parent.parent.default_properties.get('selected_SAM_model'))
                print("Default Segmentation Model PrePro: ", self.parent.parent.default_properties.get('default_segmentation_method'))
                
            for widget in right_preference_form_frame.winfo_children():
                widget.destroy()
            right_preference_form_frame.update()
            
            segmentation_form = self.parent.parent.ctk.CTkFrame(master = right_preference_form_frame,
                                            border_width= 1,
                                            )
            segmentation_form.pack(side = 'left', fill = 'both', expand = True)
            
            seg_default_method_label = self.parent.parent.ctk.CTkLabel(master = segmentation_form, text = "Default Segmentation Method:  ", anchor='w')
            seg_kcluster_label = self.parent.parent.ctk.CTkLabel(master = segmentation_form, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
            seg_kcluster_entry = self.parent.parent.ctk.CTkEntry(master = segmentation_form, placeholder_text="Enter cluster numbers" )
            seg_thres_label = self.parent.parent.ctk.CTkLabel(master = segmentation_form, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
            seg_thres_entry = self.parent.parent.ctk.CTkEntry(master = segmentation_form, placeholder_text="Threshold number" )
            seg_SAM_model_label = self.parent.parent.ctk.CTkLabel(master = segmentation_form, text = "Select your SAM model:  ", anchor='w')
            save_segmentation_settings = self.parent.parent.ctk.CTkButton(master=right_bottom_apply_buttom_frame, text="Apply", command=save_segmentation_setting)
            
            seg_SAM_model_options = self.parent.parent.ctk.CTkOptionMenu(master = segmentation_form,
                                                    values = ["ViT-H SAM Model", 
                                                            "ViT-L SAM Model", 
                                                            "ViT-B SAM Model"],
                                                    )
            seg_SAM_model_options.set("SAM Models")
            
            seg_default_method_options = self.parent.parent.ctk.CTkOptionMenu(master = segmentation_form,
                                                    values = ["K means clustering", 
                                                            "SAM Model"],
                                                    )
            seg_default_method_options.set("Default Segmentation Method")
            
            
            seg_default_method_label.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            seg_default_method_options.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            seg_kcluster_label.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            seg_kcluster_entry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            seg_thres_label.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            seg_thres_entry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')                      
            seg_SAM_model_label.grid(row = 3, column = 0,padx=100, pady=5, sticky = 'ew')
            seg_SAM_model_options.grid(row = 3, column = 1 ,padx=100, pady=5, sticky = 'ew')
            save_segmentation_settings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')

        def RGB_button_callback():
            
            
            def save_pseudo_RGB_setting():
                self.parent.parent.default_properties["red_band_no_pseudo_RGB"] = int(red_band_entry.get())
                self.parent.parent.default_properties["green_band_no_pseudo_RGB"]= int(green_band_entry.get())
                self.parent.parent.default_properties["blue_band_no_pseudo_RGB"] = int(blue_band_entry.get())  
                
                print(f"Red band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('red_band_no_pseudo_RGB')}")
                print(f"Green band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('green_band_no_pseudo_RGB')}")
                print(f"Blue band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('blue_band_no_pseudo_RGB')}")
                
                

            for widget in right_preference_form_frame.winfo_children():
                widget.destroy()

            right_preference_form_frame.update()
    
            pseudo_RGB_frame = self.parent.parent.ctk.CTkFrame(master = right_preference_form_frame,
                                            border_width= 1)   
            pseudo_RGB_frame.pack(side = 'left', fill = 'both', expand ='true')
            

            red_band_label = self.parent.parent.ctk.CTkLabel(master = pseudo_RGB_frame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
            red_band_entry = self.parent.parent.ctk.CTkEntry(master = pseudo_RGB_frame, placeholder_text="Red band number" )
            green_band_label = self.parent.parent.ctk.CTkLabel(master = pseudo_RGB_frame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
            green_band_entry = self.parent.parent.ctk.CTkEntry(master = pseudo_RGB_frame, placeholder_text="Green band number" )
            blue_band_label = self.parent.parent.ctk.CTkLabel(master = pseudo_RGB_frame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
            blue_band_entry = self.parent.parent.ctk.CTkEntry(master = pseudo_RGB_frame, placeholder_text="Blue band number" )
            save_pseudo_RGB_settings = self.parent.parent.ctk.CTkButton(master=right_bottom_apply_buttom_frame, text="Apply", command= save_pseudo_RGB_setting)
            
            
            red_band_label.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            red_band_entry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            green_band_label.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            green_band_entry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            blue_band_label.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            blue_band_entry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            save_pseudo_RGB_settings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
                
        def EMR_button_callback():
            
            
            def save_EMR_Setting():
                self.parent.parent.default_properties["no_of_bands_EMR"] = int(band_no_entry.get())
                self.parent.parent.default_properties["first_band_EMR"] = int(first_band_entry.get())
                self.parent.parent.default_properties["last_band_EMR"] =  int(last_band_entry.get())
                self.parent.parent.default_properties["spectral_resolution"]= int(spectral_resolution_entry.get())
                
                print(f"No of Band: {self.parent.parent.default_properties.get('no_of_bands_EMR')}\n"
                    f"First Band: {self.parent.parent.default_properties.get('first_band_EMR')}\n"
                    f"Last Band: {self.parent.parent.default_properties.get('last_band_EMR')}\n"
                    f"Spectral Resolution: {self.parent.parent.default_properties.get('spectral_resolution')}")
                

            for widget in right_preference_form_frame.winfo_children():
                widget.destroy()

            right_preference_form_frame.update()
    
            EMR_info_frame = self.parent.parent.ctk.CTkFrame(master = right_preference_form_frame,
                                            border_width= 1)   
            EMR_info_frame.pack(side = 'left', fill = 'both', expand ='true')
            
            band_no_label = self.parent.parent.ctk.CTkLabel(master = EMR_info_frame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
            band_no_entry = self.parent.parent.ctk.CTkEntry(master = EMR_info_frame, placeholder_text="Total number of bands" )
            
            first_band_label = self.parent.parent.ctk.CTkLabel(master = EMR_info_frame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
            first_band_entry = self.parent.parent.ctk.CTkEntry(master = EMR_info_frame, placeholder_text="First nanometer" )
            
            last_band_label = self.parent.parent.ctk.CTkLabel(master = EMR_info_frame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
            last_band_entry = self.parent.parent.ctk.CTkEntry(master = EMR_info_frame, placeholder_text="Last nanometer" )
            
            spectral_resolution_label = self.parent.parent.ctk.CTkLabel(master = EMR_info_frame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
            spectral_resolution_entry = self.parent.parent.ctk.CTkEntry(master = EMR_info_frame, placeholder_text="Spectral Resolution" )
            
            save_EMR_settings = self.parent.parent.ctk.CTkButton(master=right_bottom_apply_buttom_frame, text="Apply", command=save_EMR_Setting)
            
            band_no_label.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            band_no_entry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            first_band_label.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            first_band_entry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            last_band_label.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            last_band_entry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            spectral_resolution_label.grid(row = 3, column = 0, padx=100, pady=5, sticky = 'ew')
            spectral_resolution_entry.grid(row = 3, column = 1,padx=100, pady=5,sticky = 'ew')
            save_EMR_settings.grid(row=0, column = 1, padx=5, pady=5, sticky = 'ew')

        for widget in self.parent.parent.work_area_frame.winfo_children():
            widget.destroy()
            
        left_preference_buttons_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        right_preference_form_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        right_bottom_apply_buttom_frame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.work_area_frame)
        
        left_preference_buttons_frame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        right_preference_form_frame.place(relx = 0.2, y = 0, relwidth = 0.8, relheight = 0.9)
        right_bottom_apply_buttom_frame.place(rely = 0.9, relx = 0.2, relwidth =0.8, relheight =0.1)

        for widget in right_preference_form_frame.winfo_children():
            widget.destroy()
        
        Preprocessing_button_callback()
        
        preprocessing_button = self.parent.parent.ctk.CTkButton(master=left_preference_buttons_frame, text="Preprocessing", command=Preprocessing_button_callback)
        segmentation_button = self.parent.parent.ctk.CTkButton(master=left_preference_buttons_frame, text="Segmentation", command=segmentation_button_callback)
        RGB_button = self.parent.parent.ctk.CTkButton(master=left_preference_buttons_frame, text="RGB Bands", command=RGB_button_callback)
        EMR_button = self.parent.parent.ctk.CTkButton(master=left_preference_buttons_frame, text="Wavelengths", command=EMR_button_callback)
        
        
        right_bottom_apply_buttom_frame.columnconfigure((0,1,2), weight = 1)
        right_bottom_apply_buttom_frame.rowconfigure((0), weight = 1)
        
        preprocessing_button.pack(side= 'top',padx=50, pady=(50,10))
        segmentation_button.pack(side= 'top',padx=50, pady=10)
        RGB_button.pack(side= 'top',padx=50, pady=10)
        EMR_button.pack(side= 'top',padx=50, pady=10)
        