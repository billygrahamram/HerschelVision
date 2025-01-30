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


class PreferenceWindows(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent

    def preferencesWindow(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
        
        def PreprocessingButton_callback():
            
            def savePreProSetting():
                self.parent.parent.default_properties["SGWinSizePrePro"] = int(ppSGWinSizeEntry.get())
                self.parent.parent.default_properties["SGPolyOrderPrePro "] = int(ppSGWinSizeEntry.get())  
                
                print(f"SG Window Size: {self.parent.parent.default_properties.get('SGWinSizePrePro')}")
                print(f"SG Poly Order: {self.parent.parent.default_properties.get('SGPolyOrderPrePro')}")
                
                
            # Clear rightFormFrame
            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            PreprocessingForm = self.parent.parent.ctk.CTkFrame(master = rightPreferenceFormFrame,
                                             border_width= 1,
                                            )
            PreprocessingForm.pack(side = 'left', fill = 'both', expand = True)
        

            ppSGWinSizeLabel = self.parent.parent.ctk.CTkLabel(master = PreprocessingForm, text = "Enter Window Size for Savitzky Golay (odd number):  ", anchor = 'w')
            ppSGWinSizeEntry = self.parent.parent.ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter window size" )
            ppSGPolyOrderLabel = self.parent.parent.ctk.CTkLabel(master = PreprocessingForm, text = "Enter Polynomial Order for Savitzky Golay (< Window size):  ", anchor = 'w')
            ppSGPolyOrderEntry = self.parent.parent.ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter polynomial order" )
            savePreProSettings = self.parent.parent.ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=savePreProSetting)
           
            
            
            ppSGWinSizeLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            ppSGWinSizeEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            ppSGPolyOrderLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            ppSGPolyOrderEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            savePreProSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            

        
            
        def SegmentationButton_callback():
            
            def saveSegmentationSetting():
                  
                self.parent.parent.default_properties["KclusterNoSegPrePro"]  = int(segKclusterEntry.get())
                self.parent.parent.default_properties["KClusterThresPrePro"] = int(segThresEntry.get())
                self.parent.parent.default_properties["selectedSAMModel "]  = str(segSAMModelOptions.get())
                self.parent.parent.default_properties["defaultSegmentationMethod "] = str(segDefaultMethodOptions.get())

                print("K-cluster No Seg PrePro: ", self.parent.parent.default_properties.get('KclusterNoSegPrePro'))
                print("K-Cluster Thres PrePro: ", self.parent.parent.default_properties.get('KClusterThresPrePro'))
                print("Selected SAM Model: ", self.parent.parent.default_properties.get('selectedSAMModel'))
                print("Default Segmentation Model PrePro: ", self.parent.parent.default_properties.get('defaultSegmentationMethod'))
                
            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            SegmentationForm = self.parent.parent.ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1,
                                            )
            SegmentationForm.pack(side = 'left', fill = 'both', expand = True)
            
            segDefaultMethodLabel = self.parent.parent.ctk.CTkLabel(master = SegmentationForm, text = "Default Segmentation Method:  ", anchor='w')
            segKclusterLabel = self.parent.parent.ctk.CTkLabel(master = SegmentationForm, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
            segKclusterEntry = self.parent.parent.ctk.CTkEntry(master = SegmentationForm, placeholder_text="Enter cluster numbers" )
            segThresLabel = self.parent.parent.ctk.CTkLabel(master = SegmentationForm, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
            segThresEntry = self.parent.parent.ctk.CTkEntry(master = SegmentationForm, placeholder_text="Threshold number" )
            segSAMModelLabel = self.parent.parent.ctk.CTkLabel(master = SegmentationForm, text = "Select your SAM model:  ", anchor='w')
            saveSegmentationSettings = self.parent.parent.ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveSegmentationSetting)
            
            segSAMModelOptions = self.parent.parent.ctk.CTkOptionMenu(master = SegmentationForm,
                                                    values = ["ViT-H SAM Model", 
                                                            "ViT-L SAM Model", 
                                                            "ViT-B SAM Model"],
                                                    )
            segSAMModelOptions.set("SAM Models")
            
            segDefaultMethodOptions = self.parent.parent.ctk.CTkOptionMenu(master = SegmentationForm,
                                                    values = ["K means clustering", 
                                                            "SAM Model"],
                                                    )
            segDefaultMethodOptions.set("Default Segmentation Method")
            
            
            segDefaultMethodLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            segDefaultMethodOptions.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            segKclusterLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            segKclusterEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            segThresLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            segThresEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')                      
            segSAMModelLabel.grid(row = 3, column = 0,padx=100, pady=5, sticky = 'ew')
            segSAMModelOptions.grid(row = 3, column = 1 ,padx=100, pady=5, sticky = 'ew')
            saveSegmentationSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')

        def RGBButton_callback():
            
            
            def savePseudoRGBSetting():
                self.parent.parent.default_properties["RedbandNoPseudoRGB"] = int(RedbandEntry.get())
                self.parent.parent.default_properties["greenBandNoPseudoRGB"]= int(GreenbandEntry.get())
                self.parent.parent.default_properties["blueBandNoPseudoRGB"] = int(BluebandEntry.get())  
                
                print(f"Red band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('RedbandNoPseudoRGB')}")
                print(f"Green band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('greenBandNoPseudoRGB')}")
                print(f"Blue band number for Pseudo RGB Image: {self.parent.parent.default_properties.get('blueBandNoPseudoRGB')}")
                
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            PseudoRGBFrame = self.parent.parent.ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            PseudoRGBFrame.pack(side = 'left', fill = 'both', expand ='true')
            

            RedbandLabel = self.parent.parent.ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
            RedbandEntry = self.parent.parent.ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Red band number" )
            GreenbandLabel = self.parent.parent.ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
            GreenbandEntry = self.parent.parent.ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Green band number" )
            BluebandLabel = self.parent.parent.ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
            BluebandEntry = self.parent.parent.ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Blue band number" )
            savepseudoRGBSettings = self.parent.parent.ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command= savePseudoRGBSetting)
            
            
            RedbandLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            RedbandEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            GreenbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            GreenbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            BluebandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            BluebandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            savepseudoRGBSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
                
        def EMRButton_callback():
            
            
            def saveEMRSetting():
                self.parent.parent.default_properties["noOfBandsEMR"] = int(BandNoEntry.get())
                self.parent.parent.default_properties["firstBandEMR"] = int(FirstbandEntry.get())
                self.parent.parent.default_properties["lastBandEMR"] =  int(LastbandEntry.get())
                self.parent.parent.default_properties["spectralResolution"]= int(SpectralResolutionEntry.get())
                
                print(f"No of Band: {self.parent.parent.default_properties.get('noOfBandsEMR')}\n"
                    f"First Band: {self.parent.parent.default_properties.get('firstBandEMR')}\n"
                    f"Last Band: {self.parent.parent.default_properties.get('lastBandEMR')}\n"
                    f"Spectral Resolution: {self.parent.parent.default_properties.get('spectralResolution')}")
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            EMRInfoFrame = self.parent.parent.ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            EMRInfoFrame.pack(side = 'left', fill = 'both', expand ='true')
            
            BandNoLabel = self.parent.parent.ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
            BandNoEntry = self.parent.parent.ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Total number of bands" )
            
            FirstbandLabel = self.parent.parent.ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
            FirstbandEntry = self.parent.parent.ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="First nanometer" )
            
            LastbandLabel = self.parent.parent.ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
            LastbandEntry = self.parent.parent.ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Last nanometer" )
            
            SpectralResolutionLabel = self.parent.parent.ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
            SpectralResolutionEntry = self.parent.parent.ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Spectral Resolution" )
            
            saveEMRSettings = self.parent.parent.ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveEMRSetting)
            
            BandNoLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            BandNoEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            FirstbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            FirstbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            LastbandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            LastbandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            SpectralResolutionLabel.grid(row = 3, column = 0, padx=100, pady=5, sticky = 'ew')
            SpectralResolutionEntry.grid(row = 3, column = 1,padx=100, pady=5,sticky = 'ew')
            saveEMRSettings.grid(row=0, column = 1, padx=5, pady=5, sticky = 'ew')

        for widget in self.parent.parent.workAreaFrame.winfo_children():
            widget.destroy()
            
        leftPreferenceButtonsFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        rightPreferenceFormFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        rightBottomApplyButtomFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        
        leftPreferenceButtonsFrame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        rightPreferenceFormFrame.place(relx = 0.2, y = 0, relwidth = 0.8, relheight = 0.9)
        rightBottomApplyButtomFrame.place(rely = 0.9, relx = 0.2, relwidth =0.8, relheight =0.1)

        for widget in rightPreferenceFormFrame.winfo_children():
            widget.destroy()
        
        PreprocessingButton_callback()
        
        PreprocessingButton = self.parent.parent.ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Preprocessing", command=PreprocessingButton_callback)
        SegmentationButton = self.parent.parent.ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Segmentation", command=SegmentationButton_callback)
        RGBButton = self.parent.parent.ctk.CTkButton(master=leftPreferenceButtonsFrame, text="RGB Bands", command=RGBButton_callback)
        EMRButton = self.parent.parent.ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Wavelengths", command=EMRButton_callback)
        
        
        rightBottomApplyButtomFrame.columnconfigure((0,1,2), weight = 1)
        rightBottomApplyButtomFrame.rowconfigure((0), weight = 1)
        
        PreprocessingButton.pack(side= 'top',padx=50, pady=(50,10))
        SegmentationButton.pack(side= 'top',padx=50, pady=10)
        RGBButton.pack(side= 'top',padx=50, pady=10)
        EMRButton.pack(side= 'top',padx=50, pady=10)
        