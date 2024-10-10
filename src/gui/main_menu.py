import customtkinter as ctk
import os
import tkinter as tk
import threading
from utils.variables_utils import *
from utils.io_utils import *
from utils.data_preprocessing_utils import *
from common.common_utils import *

class MainMenu():
    def __init__(self,obj):
         self.obj = obj
         self.creat_drop_down_menu()
         print("****************888888882************")
         
    def optionmenu_callback(self,choice):
        ## method to select function to buttons in main menu.
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()
        elif choice == 'Preprocessing':
            self.preprocessingWindow()
        elif choice == 'Preferences':
            self.preferencesWindow()
        elif choice == 'Home':
            self.homeWindow()
        elif choice == 'Cropping/Segmentation':
            self.croppingWindow()

    def creat_drop_down_menu(self):
        fileOptionMenu = ctk.CTkOptionMenu(master=self.obj.menuBarFrame, values=["Home","New","Open","Save","Export","Exit"], command = self.optionmenu_callback)
        fileOptionMenu.set("File")
        fileOptionMenu.pack(side= 'left',padx=5, pady=5)

        editOptionMenu = ctk.CTkOptionMenu(master=self.obj.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        editOptionMenu.set("Edit")
        editOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        toolsOptionMenu = ctk.CTkOptionMenu(master=self.obj.menuBarFrame, values=["Cropping/Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        toolsOptionMenu.set("Tools")
        toolsOptionMenu.pack(side= 'left',padx=5, pady=5)

        aboutOptionMenu = ctk.CTkOptionMenu(master=self.obj.menuBarFrame, values=["Updates","Version","About","References", "Contact us"], command=self.optionmenu_callback)
        aboutOptionMenu.set("About")
        aboutOptionMenu.pack(side= 'left',padx=5, pady=5)
        print("***************888888888881*********************")

    def open(self):
        # Save the raw_img_dir to a text file in the history folder
        os.makedirs(data_dir_path, exist_ok=True) #make sure the history folder exists. if not creates one.
        self.obj.raw_img_dir = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = [("Raw Hyperspectral Image", "*.raw"),
                                                             ("Numpy Array", "*.npy")
                                                             ])
        
        # this makes sure that if the user selected an image and then
        # tried to open another image but cancelled the process the previous image is still displayed.
        if not self.obj.raw_img_dir:  # Check if raw_img_dir is empty
            # Read the path from the img_dir_record.txt file
            with open(img_dir_record_path, 'r') as f:
                raw_img_dir = f.read().strip()
                self.obj.raw_img_dir = raw_img_dir
                
        
        
        with open(img_dir_record_path, 'w') as f:
            f.write(self.obj.raw_img_dir)
            
        ######################### RECENT FILES #################
        # first reads all the existing paths from the file into a list. 
        # It then checks if the current path already exists in the list. 
        # If it doesn’t, the path is added to the top of the list. 
        # Finally, all the paths are written back to the file. 
        # This ensures that the most recent path is always at the top and there are no duplicates.
        
        # Read the existing paths
        with open(recent_file_path, 'r') as f:
            lines = f.read().splitlines()

        # If the path already exists in the file, remove it
        if self.obj.raw_img_dir in lines:
            lines.remove(self.obj.raw_img_dir)

        # Add the path to the top of the list
        lines.insert(0, self.obj.raw_img_dir)

        # Only keep the 5 most recent paths
        lines = lines[:5]
        
        # Write the paths back to the file
        with open(recent_file_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
                
        self.obj.Dataloaded = False
        #using multithreading to show the loading dialog box while data is loading
        threading.Thread(target = self.loadData).start()
        
        self.dataLoadingScreen()

    def loadData(self):
        self.loadDataText = 'Opening files...'
        self.currentData = readData(self.obj.raw_img_dir)
        self.spectral_array = self.currentData
        self.spectral_array = applybinning(self.spectral_array,2)
        self.loadDataText = 'Loading data and creating plots...'
        self.kmeanslabels, self.kmeansData = scatterPlotData(self.obj.raw_img_dir)
        self.loadDataText = 'Unfolding data...'
        self.unfoldedData = unfold(self.spectral_array)
        self.loadDataText = 'Finishing up...'
        wavelengthsSlider_event(self)
        self.Dataloaded = True

    def dataLoadingScreen(self):
        loading_window = tk.Toplevel(self)
        loading_window.transient(self) 
        loading_window.title("Loading data")
        loading_window.geometry("500x200")
        loading_window.resizable(width=False, height=False)

        loading_window.grab_set()

        loading_window.attributes('-topmost', True)
        loading_window.after_idle(loading_window.attributes, '-topmost', False)
        
        self.loadDataLabel = ctk.CTkLabel(master=loading_window, text = self.loadDataText, justify = "center", font = ("Helvetica", 20))
        self.loadDataLabel.pack(side = 'top', expand = True, fill = 'x', pady =(10,0))
        
        # Create a progress bar
        progress = ctk.CTkProgressBar(loading_window, width = 150, height = 30, mode='indeterminate', orientation='horizontal')
        progress.pack(side = 'top',expand=True, fill='x', padx = 80, pady=(0,80))
        progress.start()
        
        def check_data_loaded():
            if self.Dataloaded:
                loading_window.destroy()
                
            else:
                self.loadDataLabel.configure(text=self.loadDataText)
                loading_window.after(50, check_data_loaded) #keep checking after 50ms
                
        check_data_loaded()



