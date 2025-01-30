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

    def preprocessingWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.parent.parent.workAreaFrame.winfo_children():
            widget.destroy()

        ## children to workMenuFrame 
        self.parent.parent.leftButtonsPreProFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        self.parent.parent.leftButtonsPreProFrame.place(x = 0, y = 0, relwidth = 0.2, relheight = 1)
        self.parent.parent.middlePreProFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        self.parent.parent.middlePreProFrame.place(relx = 0.2, y = 0, relwidth = 0.4, relheight = 1)
        self.parent.parent.rightPreProFrame = self.parent.parent.ctk.CTkFrame(master = self.parent.parent.workAreaFrame)
        self.parent.parent.rightPreProFrame.place(relx = 0.6, y = 0, relwidth = 0.4, relheight = 1)
    

        self.parent.parent.leftButtonsPreProFrame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.rightPreProFrame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        # self.rightPreProFrame.columnconfigure((0,1), weight = 1)
        
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods
        
        self.parent.parent.PreProOptionsInput = self.parent.parent.ctk.CTkLabel(master = self.parent.parent.leftButtonsPreProFrame,
                                               text = "Input: Raw Data. \nSelect filters as forward feed. \nSelect None (pass) to skip filter.")
        self.parent.parent.PreProOptionsInput.grid(row = 0, column = 0, sticky='ew', padx = 30, pady =(50,0))
        


        self.parent.parent.PreProOptions1 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option1", selection))
        
        self.parent.parent.PreProOptions1.set("Filter 1")
        self.parent.parent.PreProOptions1.grid(row = 1, column = 0, sticky='ew', padx = 30, pady =(0,5))
   
        
        self.parent.parent.PreProOptions2 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option2", selection))
        self.parent.parent.PreProOptions2.set("Filter 2")
        self.parent.parent.PreProOptions2.grid(row = 2, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.PreProOptions3 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                         
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option3", selection))
        self.parent.parent.PreProOptions3.set("Filter 3")
        self.parent.parent.PreProOptions3.grid(row = 3, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.PreProOptions4 = self.parent.parent.ctk.CTkOptionMenu(master = self.parent.parent.leftButtonsPreProFrame,
                                                values = ["Standard Normal Variate", 
                                                          "Savitzky-Golay (first)",
                                                          "Savitzky-Golay (second)",
                                                          "Normalization",
                                                          "None (pass)"],
                                                command = lambda selection: self.preProcessingPipeLineSelection("option4", selection))
        self.parent.parent.PreProOptions4.set("Filter 4")
        self.parent.parent.PreProOptions4.grid(row = 4, column = 0, sticky='ew', padx = 30, pady =(0,5))
        

        

    
        self.parent.parent.PreProOptionsOutput = self.parent.parent.ctk.CTkLabel(master = self.parent.parent.leftButtonsPreProFrame,
                                               text = "Output: Preprocessed Data")
        self.parent.parent.PreProOptionsOutput.grid(row = 5, column = 0, sticky='ew', padx = 30, pady =(0,5))
        
        self.parent.parent.PreProApplyButton = self.parent.parent.ctk.CTkButton(master=self.parent.parent.leftButtonsPreProFrame, 
                                                    text="Apply Preprocessing", 
                                                    command = self.applyPreprocessing)
        self.parent.parent.PreProApplyButton.grid(row = 6, column = 0, sticky='ew', padx = 30, pady = (0,5))
        
        self.parent.parent.PreProSaveButton = self.parent.parent.ctk.CTkButton(master=self.parent.parent.leftButtonsPreProFrame, 
                                                    text="Save Preprocessed Data", 
                                                    command = self.savePreprocessedData)
        self.parent.parent.PreProSaveButton.grid(row = 7, column = 0, sticky='ew', padx = 30, pady = (0,50))
        

        # raw spectral plot in preprocessing window
        self.rawPlotFig, self.rawPlotFigax = plt.subplots(figsize =(10,10), dpi =40)
        self.rawPlotFig.set_facecolor(self.parent.parent.rgbValues())
        self.rawPlotFigax.set_facecolor(self.parent.parent.rgbValues())
        self.rawPlotFigax.set_title("Raw Spectral Signature",fontsize =40)
        self.rawPlotFigax.set_xlabel("Wavelength",fontsize =40)
        self.rawPlotFigax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.rawPlotFigax.tick_params(axis='both', which='major', labelsize=20)
        self.rawPlotFigCanvas = FigureCanvasTkAgg(self.rawPlotFig, master= self.parent.parent.middlePreProFrame)
        self.rawPlotFigCanvas.get_tk_widget().pack(expand = True, fill ='x')
        
        # preprocessed spectral plot in preprocessing window
        self.preProcessedPlotFig, self.preProcessedPlotFigax = plt.subplots(figsize =(10,10), dpi = 40)
        self.preProcessedPlotFig.set_facecolor(self.parent.parent.rgbValues())
        self.preProcessedPlotFigax.set_facecolor(self.parent.parent.rgbValues())
        self.preProcessedPlotFigax.set_title("Preprocessed Signature",fontsize =40)
        self.preProcessedPlotFigax.set_xlabel("Wavelength",fontsize =40)
        self.preProcessedPlotFigax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.preProcessedPlotFigax.tick_params(axis='both', which='major', labelsize=20)
        self.preProcessedPlotFigCanvas = FigureCanvasTkAgg(self.preProcessedPlotFig, master= self.parent.parent.rightPreProFrame)
        self.preProcessedPlotFigCanvas.get_tk_widget().pack(expand = True, fill ='x')
        
        if self.parent.parent.raw_img_dir == None:
            pass
        else:
            self.rawSpectralPlot(self.parent.unfoldedData)

    def preProcessingPipeLineSelection(self, source, selection):
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

    def applyPreprocessing(self):

        
        def preprocessing_in_thread():
            SGWinSizePrePro = self.parent.parent.default_properties.get("SGWinSizePrePro")
            SGPolyOrderPrePro = self.parent.parent.default_properties.get("SGPolyOrderPrePro")

            self.parent.loadDataText = 'Loading...'
            
            self.parent.loadDataText = f'Applying {self.filter1} ...'
            filter1data = preprocessing(self.filter1, self.parent.unfoldedData,w = SGWinSizePrePro,p = SGPolyOrderPrePro)
            self.parent.loadDataText = f'Applying {self.filter2} ...'
            filter2data = preprocessing(self.filter2, filter1data,w = SGWinSizePrePro,p = SGPolyOrderPrePro)
            self.parent.loadDataText = f'Applying {self.filter3} ...'
            filter3data = preprocessing(self.filter3, filter2data,w = SGWinSizePrePro,p = SGPolyOrderPrePro)
            self.parent.loadDataText = f'Applying {self.filter4} ...'
            self.preprocessedData = preprocessing(self.filter4, filter3data,w = SGWinSizePrePro,p = SGPolyOrderPrePro)
            self.parent.loadDataText = f'Plotting preprocessed spectra ...'
            self.preprocessedSpectralPlot(self.preprocessedData)
            self.Dataloaded = True

        
        if self.parent.unfoldedData is None:
                messagebox.showinfo("Info", "Please load a data first.")
                return
        self.Dataloaded = False
        threading.Thread(target = preprocessing_in_thread).start()
        self.parent.dataLoadingScreen()

    
    def savePreprocessedData(self):
        self.Dataloaded = False
        
        self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.csv',
                                               filetypes = [("Comma Separated Values", "*.csv"),
                                                            ("Text File", ".txt"),
                                                            ("Numpy Array", "*.npy"),
                                                            ])
        if self.saveFile is not None:
            self.loadDataText = f'Saving preprocessed data ...'
            threading.Thread(target = self.setDataloader).start()
            self.dataLoadingScreen()
            self.saveFile.close()

    def rawSpectralPlot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.rawPlotFigax.clear()
        for i, row in enumerate(selected_rows):
            self.rawPlotFigax.plot(np.arange(0, self.parent.parent.default_properties.get("noOfBandsEMR")), row, label=f'Row {indices[i]}')
        self.rawPlotFigax.set_title("Raw Spectral Signature",fontsize =40)
        self.rawPlotFigax.set_xlabel("Wavelength",fontsize =40)
        self.rawPlotFigax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.rawPlotFigax.tick_params(axis='both', which='major', labelsize=20)
        self.rawPlotFigCanvas.draw()

    def preprocessedSpectralPlot(self, spectral_array):
        
        indices = np.random.choice(spectral_array.shape[0], size=1000, replace=False)
        selected_rows = spectral_array[indices]
        self.preProcessedPlotFigax.clear()
        for i, row in enumerate(selected_rows):
            self.preProcessedPlotFigax.plot(np.arange(0, self.parent.parent.default_properties.get('noOfBandsEMR')), row, label=f'Row {indices[i]}')
        self.preProcessedPlotFigax.set_title("Preprocessed Signature",fontsize =40)
        self.preProcessedPlotFigax.set_xlabel("Wavelength",fontsize =40)
        self.preProcessedPlotFigax.set_ylabel("Reflectance",fontsize =40)
        # Set the fontsize of x and y tick marks
        self.preProcessedPlotFigax.tick_params(axis='both', which='major', labelsize=20)
        self.preProcessedPlotFigCanvas.draw()