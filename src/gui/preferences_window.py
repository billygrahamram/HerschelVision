import os
import tkinter as tk
import threading
from utils.variables_utils import *
from utils.io_utils import *
from utils.data_preprocessing_utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter import  messagebox


class PreferenceWindows(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent

    def preferencesWindow(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
        
        def PreprocessingButton_callback():
            
            def savePreProSetting():
                self.SGWinSizePrePro = int(ppSGWinSizeEntry.get())
                self.SGPolyOrderPrePro = int(ppSGPolyOrderEntry.get() )   
                
                print(f"SG Window Size: {self.SGWinSizePrePro}")
                print(f"SG Poly Order: {self.SGPolyOrderPrePro}")
                
                
            # Clear rightFormFrame
            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            PreprocessingForm = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                             border_width= 1,
                                            )
            PreprocessingForm.pack(side = 'left', fill = 'both', expand = True)
        

            ppSGWinSizeLabel = ctk.CTkLabel(master = PreprocessingForm, text = "Enter Window Size for Savitzky Golay (odd number):  ", anchor = 'w')
            ppSGWinSizeEntry = ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter window size" )
            ppSGPolyOrderLabel = ctk.CTkLabel(master = PreprocessingForm, text = "Enter Polynomial Order for Savitzky Golay (< Window size):  ", anchor = 'w')
            ppSGPolyOrderEntry = ctk.CTkEntry(master = PreprocessingForm, placeholder_text="Enter polynomial order" )
            savePreProSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=savePreProSetting)
           
            
            
            ppSGWinSizeLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            ppSGWinSizeEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            ppSGPolyOrderLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            ppSGPolyOrderEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            savePreProSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
            

        
            
        def SegmentationButton_callback():
            
            def saveSegmentationSetting():
                  
                self.KclusterNoSegPrePro = int(segKclusterEntry.get())
                self.KClusterThresPrePro = int(segThresEntry.get())
                self.selectedSAMModel = str(segSAMModelOptions.get())
                self.defaultSegmentationMethod = str(segDefaultMethodOptions.get())
                
                print("K-cluster No Seg PrePro: ", self.KclusterNoSegPrePro)
                print("K-Cluster Thres PrePro: ", self.KClusterThresPrePro)
                print("Selected SAM Model: ", self.selectedSAMModel)
                print("Default Segmentation Model PrePro: ", self.defaultSegmentationMethod)
                
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()
            rightPreferenceFormFrame.update()
            
            SegmentationForm = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1,
                                            )
            SegmentationForm.pack(side = 'left', fill = 'both', expand = True)
            
            segDefaultMethodLabel = ctk.CTkLabel(master = SegmentationForm, text = "Default Segmentation Method:  ", anchor='w')
            segKclusterLabel = ctk.CTkLabel(master = SegmentationForm, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
            segKclusterEntry = ctk.CTkEntry(master = SegmentationForm, placeholder_text="Enter cluster numbers" )
            segThresLabel = ctk.CTkLabel(master = SegmentationForm, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
            segThresEntry = ctk.CTkEntry(master = SegmentationForm, placeholder_text="Threshold number" )
            segSAMModelLabel = ctk.CTkLabel(master = SegmentationForm, text = "Select your SAM model:  ", anchor='w')
            saveSegmentationSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveSegmentationSetting)
            
            segSAMModelOptions = ctk.CTkOptionMenu(master = SegmentationForm,
                                                    values = ["ViT-H SAM Model", 
                                                            "ViT-L SAM Model", 
                                                            "ViT-B SAM Model"],
                                                    )
            segSAMModelOptions.set("SAM Models")
            
            segDefaultMethodOptions = ctk.CTkOptionMenu(master = SegmentationForm,
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
                self.RedbandNoPseudoRGB = int(RedbandEntry.get())
                self.greenBandNoPseudoRGB = int(GreenbandEntry.get())
                self.blueBandNoPseudoRGB = int(BluebandEntry.get())  
                
                print(f"Red band number for Pseudo RGB Image: {self.RedbandNoPseudoRGB}")
                print(f"Green band number for Pseudo RGB Image: {self.greenBandNoPseudoRGB}")
                print(f"Blue band number for Pseudo RGB Image: {self.blueBandNoPseudoRGB}")
                
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            PseudoRGBFrame = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            PseudoRGBFrame.pack(side = 'left', fill = 'both', expand ='true')
            

            RedbandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
            RedbandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Red band number" )
            GreenbandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
            GreenbandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Green band number" )
            BluebandLabel = ctk.CTkLabel(master = PseudoRGBFrame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
            BluebandEntry = ctk.CTkEntry(master = PseudoRGBFrame, placeholder_text="Blue band number" )
            savepseudoRGBSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command= savePseudoRGBSetting)
            
            
            RedbandLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            RedbandEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            GreenbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            GreenbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            BluebandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            BluebandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            savepseudoRGBSettings.grid(row = 0, column = 1, padx=5, pady=5, sticky = 'ew')
                
        def EMRButton_callback():
            
            
            def saveEMRSetting():
                self.noOfBandsEMR = int(BandNoEntry.get())
                self.firstBandEMR = int(FirstbandEntry.get())
                self.lastBandEMR =  int(LastbandEntry.get())
                self.spectralResolution = int(SpectralResolutionEntry.get())
                
                print(f"No of Band: {self.noOfBandsEMR}\n"
                    f"First Band: {self.firstBandEMR}\n"
                    f"Last Band: {self.lastBandEMR}\n"
                    f"Spectral Resolution: {self.spectralResolution}")
                

            for widget in rightPreferenceFormFrame.winfo_children():
                widget.destroy()

            rightPreferenceFormFrame.update()
    
            EMRInfoFrame = ctk.CTkFrame(master = rightPreferenceFormFrame,
                                            border_width= 1)   
            EMRInfoFrame.pack(side = 'left', fill = 'both', expand ='true')
            
            BandNoLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
            BandNoEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Total number of bands" )
            
            FirstbandLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
            FirstbandEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="First nanometer" )
            
            LastbandLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
            LastbandEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Last nanometer" )
            
            SpectralResolutionLabel = ctk.CTkLabel(master = EMRInfoFrame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
            SpectralResolutionEntry = ctk.CTkEntry(master = EMRInfoFrame, placeholder_text="Spectral Resolution" )
            
            saveEMRSettings = ctk.CTkButton(master=rightBottomApplyButtomFrame, text="Apply", command=saveEMRSetting)
            
            BandNoLabel.grid(row = 0, column = 0, padx=100, pady=(100,5), sticky = 'ew')
            BandNoEntry.grid(row = 0, column = 1,padx=100, pady=(100,5),sticky = 'ew')
            FirstbandLabel.grid(row = 1, column = 0, padx=100, pady=5, sticky = 'ew')
            FirstbandEntry.grid(row = 1, column = 1,padx=100, pady=5,sticky = 'ew')
            LastbandLabel.grid(row = 2, column = 0, padx=100, pady=5, sticky = 'ew')
            LastbandEntry.grid(row = 2, column = 1,padx=100, pady=5,sticky = 'ew')
            SpectralResolutionLabel.grid(row = 3, column = 0, padx=100, pady=5, sticky = 'ew')
            SpectralResolutionEntry.grid(row = 3, column = 1,padx=100, pady=5,sticky = 'ew')
            saveEMRSettings.grid(row=0, column = 1, padx=5, pady=5, sticky = 'ew')

        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        leftPreferenceButtonsFrame = ctk.CTkFrame(master = self.workAreaFrame)
        rightPreferenceFormFrame = ctk.CTkFrame(master = self.workAreaFrame)
        rightBottomApplyButtomFrame = ctk.CTkFrame(master = self.workAreaFrame)
        
        leftPreferenceButtonsFrame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        rightPreferenceFormFrame.place(relx = 0.2, y = 0, relwidth = 0.8, relheight = 0.9)
        rightBottomApplyButtomFrame.place(rely = 0.9, relx = 0.2, relwidth =0.8, relheight =0.1)

        for widget in rightPreferenceFormFrame.winfo_children():
            widget.destroy()
        
        PreprocessingButton_callback()
        
        PreprocessingButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Preprocessing", command=PreprocessingButton_callback)
        SegmentationButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Segmentation", command=SegmentationButton_callback)
        RGBButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="RGB Bands", command=RGBButton_callback)
        EMRButton = ctk.CTkButton(master=leftPreferenceButtonsFrame, text="Wavelengths", command=EMRButton_callback)
        
        
        rightBottomApplyButtomFrame.columnconfigure((0,1,2), weight = 1)
        rightBottomApplyButtomFrame.rowconfigure((0), weight = 1)
        
        PreprocessingButton.pack(side= 'top',padx=50, pady=(50,10))
        SegmentationButton.pack(side= 'top',padx=50, pady=10)
        RGBButton.pack(side= 'top',padx=50, pady=10)
        EMRButton.pack(side= 'top',padx=50, pady=10)
        