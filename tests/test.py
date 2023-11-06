import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk




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
        self.workAreaFrame = frame(master = self, side = 'top', border_width=0,fill = 'both', expand= True, fg_color='white')
        
        # opens the home window by default
        self.homeWindow()
        self.mainMenu()
    


    def mainMenu(self):
        ## children to menuBarFrame. Menu bar buttons
        self.FileOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["New","Open","Save","Export","Exit"], command=self.optionmenu_callback)
        self.FileOptionMenu.set("File")
        self.FileOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.EditOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        self.EditOptionMenu.set("Edit")
        self.EditOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.ToolsOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preliminary Analysis","Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        self.ToolsOptionMenu.set("Tools")
        self.ToolsOptionMenu.pack(side= 'left',padx=5, pady=5)

        self.AboutOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Updates","Version","About", "Contact us"], command=self.optionmenu_callback)
        self.AboutOptionMenu.set("About")
        self.AboutOptionMenu.pack(side= 'left',padx=5, pady=5)
       
    def optionmenu_callback(self,choice):
    
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()
        elif choice == 'About':
            self.about()
        elif choice == 'Segmentation':
            self.greenboard()
        elif choice == 'Preliminary Analysis':
            self.homeWindow()
        elif choice == 'Preprocessing':
            self.greenboard()
        elif choice == 'Preferences':
            self.preferences()

    
    def homeWindow(self):
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        ## children to workMenuFrame 
        self.leftFrame = frame(master=self.workAreaFrame, side='left', border_width= 20)
        self.rightFrame = frame(master=self.workAreaFrame, side='right', border_width= 20)
        
        
        ## children to righFrame
        self.rightFrameTop = frame(master=self.rightFrame, side='top', border_width= 20, border_color='green')
        self.rightFrameBottom = frame(master=self.rightFrame, side='top', border_width= 20, border_color='green')
    
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
        self.about_window = ctk.CTkToplevel(self)
        self.about_window.title("About")
        self.about_window.geometry("400x400")
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
        
        self.canvas = tk.Canvas(master = self.about_window,
                                background = "black",
                                bd = 0,
                                highlightthickness = 0,
                                relief = 'ridge'
                                )
        
        self.canvas.pack(expand=True, fill='both')
        self.canvas.bind('<Configure>',self.full_image)
        

        
    def greenboard(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.leftFrame = frame(master=self.workAreaFrame, 
                               side='left', 
                               border_width= 20,
                               fg_color='white', expand = False,
                               width = self.dimensionPercentage(4, dimension='w'),
                               height = self.dimensionPercentage(100, dimension='h'))
        self.middleFrame = frame(master=self.workAreaFrame, 
                                 side='left', 
                                 border_width= 20,
                                 fg_color='red',
                                 width = self.dimensionPercentage(48, dimension='w'),
                                 height = self.dimensionPercentage(100, dimension='h'))
        self.rightFrame = frame(master=self.workAreaFrame, 
                                side='left', 
                                border_width= 20,
                                fg_color='green', 
                                width = self.dimensionPercentage(48, dimension='w'),
                                height = self.dimensionPercentage(100, dimension='h'))
        
        ## children to righFrame
        self.rightFrameTop = frame(master=self.rightFrame, 
                                   side='top', 
                                   border_width= 20, 
                                   border_color='green',
                                   height =  self.dimensionPercentage(70, dimension='h'))
        self.rightFrameBottom = frame(master=self.rightFrame, 
                                      side='top', 
                                      border_width= 20, 
                                      border_color='green', expand = False,
                                      height = self.dimensionPercentage(30, dimension='h'))
        
        self.rightFrameBottom.columnconfigure(0, weight=1)
        self.rightFrameBottom.columnconfigure(1, weight=1)

        
        self.saveImgasNPYButton(master = self.rightFrameBottom)
        self.saveUnfoldDatButton(master = self.rightFrameBottom)

    def preferences(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
            
        ## children to workAreaFrame 
        self.leftButtonsFrame = frame(master=self.workAreaFrame,  
                                      border_width= 20,
                                      fg_color='white', 
                                      width = self.dimensionPercentage(5, dimension='w'), 
                                      height = self.dimensionPercentage(100, dimension='h'),
                                      side='left', expand = False, fill ='both')
        self.rightOptionsFrame = frame(master=self.workAreaFrame,  
                                       border_width= 20,
                                       fg_color='green', 
                                       width = self.dimensionPercentage(95, dimension='w'), 
                                       height = self.dimensionPercentage(100, dimension='h'),
                                       side='left')
    
        ## children to menuBarFrame. Menu bar buttons
        self.PreprocessingOptionMenu = ctk.CTkButton(master=self.leftButtonsFrame, text="Preprocessing", command=self.preferenceMenu_callback)
        self.PreprocessingOptionMenu.pack(side= 'top',padx=10, pady=10)
        
        self.SegmentationOptionMenu = ctk.CTkButton(master=self.leftButtonsFrame, text="Segmentation", command=self.preferenceMenu_callback)
        self.SegmentationOptionMenu.pack(side= 'top',padx=10, pady=10)
        
        self.RGBOptionMenu = ctk.CTkButton(master=self.leftButtonsFrame, text="RGB Bands", command=self.preferenceMenu_callback)
        self.RGBOptionMenu.pack(side= 'top',padx=5, pady=10)

        self.EMROptionMenu = ctk.CTkButton(master=self.leftButtonsFrame, text="Wavelengths", command=self.preferenceMenu_callback)
        self.EMROptionMenu.pack(side= 'top',padx=5, pady=10)
        
        
        
    def preferenceMenu_callback(self):
        print("it works dude!")

 
    def dimensionPercentage(self, percent, dimension='w'):
        if dimension == 'h':
            size = self.winfo_height()
        elif dimension == 'w':
            size = self.winfo_width()
        else:
            raise ValueError("Invalid dimension: choose either 'w' or 'h'")
            
        pxSize = int((percent*size)/100)
        return pxSize

        
    def saveImgasNPYButton(self, master):
        self.button = ctk.CTkButton(master=master,
                                                    text='Save Image as NPY (3D array)',
                                                    fg_color='red',
                                                    bg_color='white',
                                                    hover = True,
                                                    corner_radius=100,
                                                    border_width=5,
                                                    border_color='red',
                                                    command=button_event)

        self.button.grid(row = 0, column = 0, sticky='ew')
        
        
    def saveUnfoldDatButton(self, master):
        self.button = ctk.CTkButton(master=master,
                                                    text='Save Unfold Image (.txt)',
                                                    fg_color='red',
                                                    bg_color='black',
                                                    hover = True,
                                                    corner_radius=100,
                                                    border_width=5,
                                                    border_color='red',
                                                    command=button_event)
        self.button.grid(row = 0, column = 1, sticky='ew')
        
        
        
app = App()
app.mainloop()

