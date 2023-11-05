import customtkinter as ctk
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt



ctk.set_appearance_mode("white")

def frame(master,
          corner_radius=0,
          fg_color='gray',
          border_width=5,
          border_color="black",
          width = 100,
          height = 100,
          side='left',
          fill = 'both',
          expand = True,):
    
    frame = ctk.CTkFrame(master=master, 
                         corner_radius=corner_radius, 
                         fg_color=fg_color, 
                         border_width=border_width, 
                         border_color=border_color,
                         width = width,
                         height = height)
    frame.pack(side=side, 
               fill=fill, 
               expand=expand)
    return frame 

def button(master,
           text='Button',
           fg_color='red',
           bg_color='white',
           hover = True,
           width = 300,
           height = 10,
           corner_radius=100,
           border_width=5,
           border_color='red',
           side='top',
           fill='both',
           expand=True,
           command=None):
    
    button = ctk.CTkButton(master=master,
                           text=text,
                           fg_color=fg_color,
                           bg_color=bg_color,
                           hover = hover,
                           width = width,
                           height = height,
                           corner_radius=corner_radius,
                           border_width=border_width,
                           border_color=border_color,
                           command=command)

    button.pack(side=side, fill=fill, expand=expand)
    
    return button

def button_event():
    print("button pressed")
    

    
    
    
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x400")
        self.title("Herchel Vision Test Phase")
        self.resizable(width=True, height=True)
    
    
        ## children to main window
        self.menuBarFrame = frame(master = self, side = 'top', border_width=0 ,fill = 'x', expand=False, fg_color='white')
        self.workMenuFrame = frame(master = self, side = 'top', border_width=0,fill = 'both', expand= True, fg_color='white')
        
        
        ## children to workMenuFrame 
        self.leftFrame = frame(master=self.workMenuFrame, side='left', border_width= 20)
        self.rightFrame = frame(master=self.workMenuFrame, side='right', border_width= 20)
        
        
        ## children to righFrame
        self.rightFrameTop = frame(master=self.rightFrame, side='top', border_width= 20, border_color='green')
        self.rightFrameBottom = frame(master=self.rightFrame, side='top', border_width= 20, border_color='green')
        
        ## children to menuBarFrame. Menu bar buttons
        self.optionmenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["New","Open","Save","Export","Exit"], command=self.optionmenu_callback)
        self.optionmenu.set("File")
        self.optionmenu.pack(side= 'left',padx=5, pady=5)
        
        self.optionmenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        self.optionmenu.set("Edit")
        self.optionmenu.pack(side= 'left',padx=5, pady=5)
        
        self.optionmenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Segmentation","Preprocessing"], command=self.optionmenu_callback)
        self.optionmenu.set("Tools")
        self.optionmenu.pack(side= 'left',padx=5, pady=5)

        self.optionmenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Updates","Version","About", "Contact us"], command=self.optionmenu_callback)
        self.optionmenu.set("About")
        self.optionmenu.pack(side= 'left',padx=5, pady=5)


       
    def optionmenu_callback(self,choice):
    
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()

       
    def open(self):
        file_path = tk.filedialog.askopenfilename(initialdir="/", 
                                                title="Select file",
                                                filetypes = (("JPEG File", "*.jpg"),("all files","*.*")))
        
        self.img_original = Image.open(file_path)
        self.img_ratio = self.img_original.size[0]/self.img_original.size[1]
        self.img_tk = ImageTk.PhotoImage(self.img_original)

        # Clear self.leftFrame
        for widget in self.leftFrame.winfo_children():
            widget.destroy()
        
        self.canvas = tk.Canvas(self.leftFrame, 
                           background="black", 
                           bd =0,
                           highlightthickness=0,
                           relief='ridge')
        
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind('<Configure>',self.full_image)
    
    def full_image(self, event):
        
        self.canvas_ratio = event.width / event.height
        
        
        if self.canvas_ratio > self.img_ratio:
            height = int(event.height)
            width = int(height * self.img_ratio)
        else:
            width = int(event.width)
            height = int(width/self.img_ratio)
            
            
        resized_image = self.img_original.resize((width, height))
        self.resized_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(
            int(event.width/2), 
            int(event.height/2), 
            anchor = 'center',
            image=self.resized_tk)
        
    def about(self):
        # creates a new top level tkinter window.
        self.about_window = tk.Toplevel(self)
        self.about_window.title("About")
        self.about_window.geometry("500x500")
        self.about_window.resizable(width=False, height=False)
        
        # routes all event for the app to about window.
        # user cannot intereact with app until about window is closed.
        self.about_window.grab_set()
        
        # makes the popup window appear on top of the application window
        # instead of a seperate desktop window.
        self.about_window.attributes('-topmost', True)
        self.about_window.after_idle(self.about_window.attributes, '-topmost', False)
        
        self.img_original = Image.open('data/HerschelVisionAbout.png')
        self.img_ratio = self.img_original.size[0]/self.img_original.size[1]
        self.img_tk = ImageTk.PhotoImage(self.img_original)
        
        # Clear self.about_window
        for widget in self.about_window.winfo_children():
            widget.destroy()
            
        self.canvas = tk.Canvas(master = self.about_window,
                                background = "black",
                                bd = 0,
                                highlightthickness = 0,
                                relief = 'ridge'
                                )
        
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind('<Configure>',self.full_image)
        
        
        

app = App()
app.mainloop()

