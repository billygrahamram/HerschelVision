import os
import threading
import tkinter as tk

import customtkinter as ctk

from gui.cropping_segmentation_window import *
from gui.home_window import *
from gui.preferences_window import *
from gui.preprocess import *
from utils.data_preprocessing_utils import *
from utils.io_utils import *
from utils.variables_utils import *


class Main_menu(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent
         self.app = parent
         self.unfolded_data = None
         self.creat_drop_down_menu()
         
    def optionmenu_callback(self,choice):
        ## method to select function to buttons in main menu.
        if choice == 'Exit':
            self.app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()
        elif choice == 'Preprocessing':
            preprocess_object = Preprocess(self)
            preprocess_object.preprocessing_window()
        elif choice == 'Preferences':
            preference_object = Preference_windows(self)
            preference_object.preferences_window()
        elif choice == 'Home':
            hw_object = Home_window(self.parent)
            hw_object.home_menu()
        elif choice == 'Cropping/Segmentation':
            hw_object = Crop_segment_windows(self.parent)
            hw_object.cropping_window()

    def creat_drop_down_menu(self):
        file_option_menu = self.parent.ctk.CTkOptionMenu(master=self.parent.menu_bar_frame, values=["Home","New","Open","Save","Export","Exit"], command = self.optionmenu_callback)
        file_option_menu.set("File")
        file_option_menu.pack(side= 'left',padx=5, pady=5)

        edit_option_menu = self.parent.ctk.CTkOptionMenu(master=self.parent.menu_bar_frame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        edit_option_menu.set("Edit")
        edit_option_menu.pack(side= 'left',padx=5, pady=5)
        
        tools_option_menu = self.parent.ctk.CTkOptionMenu(master=self.parent.menu_bar_frame, values=["Cropping/Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        tools_option_menu.set("Tools")
        tools_option_menu.pack(side= 'left',padx=5, pady=5)

        about_option_menu = self.parent.ctk.CTkOptionMenu(master=self.parent.menu_bar_frame, values=["Updates","Version","About","References", "Contact us"], command=self.optionmenu_callback)
        about_option_menu.set("About")
        about_option_menu.pack(side= 'left',padx=5, pady=5)

        show_image_button = self.parent.ctk.CTkButton(self.parent.menu_bar_frame, text="Show RGB Image", command=self.parent.show_psuedo_rgb)
        show_image_button.pack(side='left', padx=5, pady=5)
        
    def open(self):
        # Save the raw_img_dir to a text file in the history folder
        os.makedirs(data_dir_path, exist_ok=True) #make sure the history folder exists. if not creates one.
        self.parent.raw_img_dir = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = [("Raw Hyperspectral Image", "*.raw"),
                                                             ("Numpy Array", "*.npy")
                                                             ])
        
        # this makes sure that if the user selected an image and then
        # tried to open another image but cancelled the process the previous image is still displayed.
        if not self.parent.raw_img_dir:  # Check if raw_img_dir is empty
            # Read the path from the img_dir_record.txt file
            with open(img_dir_record_path, 'r') as f:
                raw_img_dir = f.read().strip()
                self.parent.raw_img_dir = raw_img_dir
                
        
        
        with open(img_dir_record_path, 'w') as f:
            f.write(self.parent.raw_img_dir)
            
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
        if self.parent.raw_img_dir in lines:
            lines.remove(self.parent.raw_img_dir)

        # Add the path to the top of the list
        lines.insert(0, self.parent.raw_img_dir)

        # Only keep the 5 most recent paths
        lines = lines[:5]
        
        # Write the paths back to the file
        with open(recent_file_path, 'w') as f:
            for line in lines:
                f.write(line + '\n')
                
        self.parent.Dataloaded = False
        #using multithreading to show the loading dialog box while data is loading
        threading.Thread(target = self.loadData).start()
        
        self.data_loading_screen()

    def loadData(self):
        self.load_data_text = 'Opening files...'
        self.current_data = read_data(self.parent.raw_img_dir)
        self.spectral_array = self.current_data
        self.spectral_array = apply_binning(self.spectral_array,2)
        self.parent.spectral_array = self.spectral_array
        self.parent.rgb_data = create_pseudo_rgb(self.spectral_array)
        self.load_data_text = 'Loading data and creating plots...'
        self.parent.kmeanslabels, self.parent.kmeansData = scatter_plot_data(self.parent.raw_img_dir)
        self.load_data_text = 'Unfolding data...'
        self.unfolded_data = unfold(self.spectral_array)
        self.load_data_text = 'Finishing up...'
        #self.parent.wavelengths_slider_event()
        self.parent.show_psuedo_rgb()
        self.parent.Dataloaded = True
        print("end")

    def data_loading_screen(self):
        loading_window = tk.Toplevel(self.parent)
        loading_window.transient(self.parent) 
        loading_window.title("Loading data")
        loading_window.geometry("500x200")
        loading_window.resizable(width=False, height=False)
        loading_window.update_idletasks()

        loading_window.grab_set()

        loading_window.attributes('-topmost', True)
        loading_window.after_idle(loading_window.attributes, '-topmost', False)
        
        self.load_data_label = self.parent.ctk.CTkLabel(master=loading_window, text = self.load_data_text, justify = "center", font = ("Helvetica", 20))
        self.load_data_label.pack(side = 'top', expand = True, fill = 'x', pady =(10,0))
        
        # Create a progress bar
        progress = self.parent.ctk.CTkProgressBar(loading_window, width = 150, height = 30, mode='indeterminate', orientation='horizontal')
        progress.pack(side = 'top',expand=True, fill='x', padx = 80, pady=(0,80))
        progress.start()
        
        def check_data_loaded():
            if self.parent.Dataloaded:
                loading_window.destroy()
                
            else:
                self.load_data_label.configure(text=self.load_data_text)
                loading_window.after(50, check_data_loaded) #keep checking after 50ms
                
        check_data_loaded()

    def about(self):
        # creates a new top level tkinter window.
        about_window = self.parent.ctk.CTkToplevel(self)
        about_window.transient(self) 
        about_window.title("About")
        about_window.geometry("500x500")
        about_window.resizable(width=False, height=False)

        # routes all event for the app to about window.
        # user cannot intereact with app until about window is closed.
        about_window.grab_set()
        
        # makes the popup window appear on top of the application window
        # instead of a seperate desktop window.
        about_window.attributes('-topmost', True)
        about_window.after_idle(about_window.attributes, '-topmost', False)
        
        # Load the image
        about_img = Image.open(about_imgpath)
        # Resize the image to fit the window
        about_img = about_img.resize((500,500))
        about_img_tk = ImageTk.PhotoImage(about_img)
        
        # Keep a reference to the image
        about_window.about_img_tk = about_img_tk
        
        about_canvas = tk.Canvas(master = about_window,
                                bd = 0,
                                highlightthickness = 0,
                                relief = 'ridge'
                                )
        about_canvas.create_image(0, 0, image=about_img_tk, anchor='nw')
        about_canvas.pack(expand=True, fill='both')