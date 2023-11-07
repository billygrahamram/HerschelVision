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
        self.FileOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Home","New","Open","Save","Export","Exit"], command=self.optionmenu_callback)
        self.FileOptionMenu.set("File")
        self.FileOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.EditOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preferences","Undo"], command=self.optionmenu_callback)
        self.EditOptionMenu.set("Edit")
        self.EditOptionMenu.pack(side= 'left',padx=5, pady=5)
        
        self.ToolsOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Preliminary Analysis","Segmentation","Preprocessing", "Preferences"], command=self.optionmenu_callback)
        self.ToolsOptionMenu.set("Tools")
        self.ToolsOptionMenu.pack(side= 'left',padx=5, pady=5)

        self.AboutOptionMenu = ctk.CTkOptionMenu(master=self.menuBarFrame, values=["Updates","Version","About","References", "Contact us"], command=self.optionmenu_callback)
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
            self.imageSegmentationWindow()
        elif choice == 'Preliminary Analysis':
            self.homeWindow()
        elif choice == 'Preprocessing':
            self.preprocessingWindow()
        elif choice == 'Preferences':
            self.preferencesWindow()
        elif choice == 'Home':
            self.homeWindow()

    
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
          
    def imageSegmentationWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.leftButtonsImgSegFrame = frame(master=self.workAreaFrame, 
                               side='left', 
                               border_width= 20,
                               fg_color='white', expand = False,
                               width = self.dimensionPercentage(4, dimension='w'),
                               height = self.dimensionPercentage(100, dimension='h'))
        self.middleImgSegFrame = frame(master=self.workAreaFrame, 
                                 side='left', 
                                 border_width= 20,
                                 fg_color='red',
                                 width = self.dimensionPercentage(48, dimension='w'),
                                 height = self.dimensionPercentage(100, dimension='h'))
        self.rightImgSegFrame = frame(master=self.workAreaFrame, 
                                side='left', 
                                border_width= 20,
                                fg_color='green', 
                                width = self.dimensionPercentage(48, dimension='w'),
                                height = self.dimensionPercentage(100, dimension='h'))
        
        ## children to righFrame
        self.rightImgSegTopFrame = frame(master=self.rightImgSegFrame, 
                                   side='top', 
                                   border_width= 20, 
                                   border_color='green',
                                   height =  self.dimensionPercentage(70, dimension='h'))
        self.rightImgSegBottomButtonFrame = frame(master=self.rightImgSegFrame, 
                                      side='top', 
                                      border_width= 20, 
                                      border_color='green', expand = False,
                                      height = self.dimensionPercentage(30, dimension='h'))
        
        self.rightImgSegBottomButtonFrame.columnconfigure(0, weight=1)
        self.rightImgSegBottomButtonFrame.columnconfigure(1, weight=1)

        ## RIGHT BOTTOM Buttons
        self.saveImgasNPYButton(master = self.rightImgSegBottomButtonFrame)
        self.saveUnfoldDatButton(master = self.rightImgSegBottomButtonFrame)
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods

        self.ImgSegOptions = ctk.CTkOptionMenu(master = self.leftButtonsImgSegFrame,
                                                values = ["K-means clustering", 
                                                          "Segment Anything"],command = self.optionmenu_callback)
        self.ImgSegOptions.set("Segmentation Models")
        self.ImgSegOptions.pack(side= 'top',padx=10, pady=10)
        self.ImgSegParametersButton = ctk.CTkButton(master=self.leftButtonsImgSegFrame, text="Parameters", command=self.preferencesWindow)
        self.ImgSegParametersButton.pack(side= 'top',padx=10, pady=10)



    def preprocessingWindow(self):
        
        # Clear self.workAreaFrame
        for widget in self.workAreaFrame.winfo_children():
            widget.destroy()
        
        ## children to workMenuFrame 
        self.leftButtonsPreProFrame = frame(master=self.workAreaFrame, 
                               side='left', 
                               border_width= 20,
                               fg_color='white', expand = False,
                               width = self.dimensionPercentage(4, dimension='w'),
                               height = self.dimensionPercentage(100, dimension='h'))
        self.middlePreProFrame = frame(master=self.workAreaFrame, 
                                 side='left', 
                                 border_width= 20,
                                 fg_color='red',
                                 width = self.dimensionPercentage(48, dimension='w'),
                                 height = self.dimensionPercentage(100, dimension='h'))
        self.rightPreProFrame = frame(master=self.workAreaFrame, 
                                side='left', 
                                border_width= 20,
                                fg_color='green', 
                                width = self.dimensionPercentage(48, dimension='w'),
                                height = self.dimensionPercentage(100, dimension='h'))
        
        ## children to righFrame
        self.rightPreProTopFrame = frame(master=self.rightPreProFrame, 
                                   side='top', 
                                   border_width= 20, 
                                   border_color='green',
                                   height =  self.dimensionPercentage(70, dimension='h'))
        self.rightPreProBottomButtonFrame = frame(master=self.rightPreProFrame, 
                                      side='top', 
                                      border_width= 20, 
                                      border_color='green', expand = False,
                                      height = self.dimensionPercentage(30, dimension='h'))
        
        self.rightPreProBottomButtonFrame.columnconfigure(0, weight=1)
        self.rightPreProBottomButtonFrame.columnconfigure(1, weight=1)

        ## RIGHT BOTTOM Buttons
        self.saveImgasNPYButton(master = self.rightPreProBottomButtonFrame)
        self.saveUnfoldDatButton(master = self.rightPreProBottomButtonFrame)
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        ## label and dropdown for the preprocessing methods

        self.PreProOptions = ctk.CTkOptionMenu(master = self.leftButtonsPreProFrame,
                                                values = ["SNV", 
                                                          "MSC",
                                                          "SG",
                                                          "Normalize"],command = self.optionmenu_callback)
        self.PreProOptions.set("PreProcessing Methods")
        self.PreProOptions.pack(side= 'top',padx=10, pady=10)
        self.PreProParametersButton = ctk.CTkButton(master=self.leftButtonsPreProFrame, text="Parameters", command=self.preferencesWindow)
        self.PreProParametersButton.pack(side= 'top',padx=10, pady=10)


        
        
    def preferencesWindow(self): # the settings window that allows the user to input/select variables for analysis inputs.
        
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
        self.rightPreferenceFormFrame = frame(master=self.workAreaFrame,  
                                       border_width= 20,
                                       fg_color='white', 
                                       width = self.dimensionPercentage(95, dimension='w'), 
                                       height = self.dimensionPercentage(100, dimension='h'),
                                       side='left')
            # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
        self.PreprocessingButton_callback()
        
        ## LEFT SIDE BUTTONS
        ## children to leftButtonsFrame. Preferences buttons
        self.PreprocessingButton = ctk.CTkButton(master=self.leftButtonsFrame, text="Preprocessing", command=self.PreprocessingButton_callback)
        self.PreprocessingButton.pack(side= 'top',padx=10, pady=10)
        self.SegmentationButton = ctk.CTkButton(master=self.leftButtonsFrame, text="Segmentation", command=self.SegmentationButton_callback)
        self.SegmentationButton.pack(side= 'top',padx=10, pady=10)
        self.RGBButton = ctk.CTkButton(master=self.leftButtonsFrame, text="RGB Bands", command=self.RGBButton_callback)
        self.RGBButton.pack(side= 'top',padx=5, pady=10)
        self.EMRButton = ctk.CTkButton(master=self.leftButtonsFrame, text="Wavelengths", command=self.EMRButton_callback)
        self.EMRButton.pack(side= 'top',padx=5, pady=10)
        
    def PreprocessingButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.PreprocessingForm = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 20,
                                        fg_color='white', 
                                        side='left',  fill ='both')
        
        
        ## label and dropdown for the preprocessing methods
        self.ppModelLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Select your preprocessing method:  ", anchor='w')
        self.ppModelLabel.grid(row = 0, column = 0,padx=5, pady=5, sticky = 'ew')
        self.ppModelOptions = ctk.CTkOptionMenu(master = self.PreprocessingForm,
                                                values = ["Standard Normal Variate", 
                                                          "Multiplicative Scatter Correction", 
                                                          "Savitzky-Golay", 
                                                          "Normalization"],command = self.optionmenu_callback)
        self.ppModelOptions.set("Preprocessing Models")
        self.ppModelOptions.grid(row = 0, column = 1 ,padx=5, pady=5, sticky = 'ew')
        
        
        ## label and input field for savitzky golay window size
        self.ppSGWinSizeLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Enter Window Size for Savitzky Golay:  ", anchor = 'w')
        self.ppSGWinSizeLabel.grid(row = 1, column = 0, padx=5, pady=5, sticky = 'ew')
        self.ppSGWinSizeEntry = ctk.CTkEntry(master = self.PreprocessingForm, placeholder_text="Enter window size" )
        self.ppSGWinSizeEntry.grid(row = 1, column = 1,padx=5, pady=5,sticky = 'ew')
                                   
        
        ## label and input field for savitzky golay derivative
        self.ppSGDerivLabel = ctk.CTkLabel(master = self.PreprocessingForm, text = "Enter Savitzky Golay Derivative:  ", anchor = 'w')
        self.ppSGDerivLabel.grid(row = 2, column = 0, padx=5, pady=5, sticky = 'ew')
        self.ppSGDerivEntry = ctk.CTkEntry(master = self.PreprocessingForm, placeholder_text="Enter Derivative Number" )
        self.ppSGDerivEntry.grid(row = 2, column = 1,padx=5, pady=5,sticky = 'ew')
        
    def SegmentationButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.SegmentationForm = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 20,
                                        fg_color='white', 
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.segKclusterLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Enter the number of clusters for K-means:  ", anchor = 'w')
        self.segKclusterLabel.grid(row = 0, column = 0, padx=5, pady=5, sticky = 'ew')
        self.segKclusterEntry = ctk.CTkEntry(master = self.SegmentationForm, placeholder_text="Enter cluster numbers" )
        self.segKclusterEntry.grid(row = 0, column = 1,padx=5, pady=5,sticky = 'ew')
                                   
        
        ## label and input field for savitzky golay derivative
        self.segThresLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Enter Segmentation Thresholding value:  ", anchor = 'w')
        self.segThresLabel.grid(row = 1, column = 0, padx=5, pady=5, sticky = 'ew')
        self.segThresEntry = ctk.CTkEntry(master = self.SegmentationForm, placeholder_text="Threshold number" )
        self.segThresEntry.grid(row = 1, column = 1,padx=5, pady=5,sticky = 'ew')
        
        ## label and dropdown for the preprocessing methods
        self.segSAMModelLabel = ctk.CTkLabel(master = self.SegmentationForm, text = "Select your SAM model:  ", anchor='w')
        self.segSAMModelLabel.grid(row = 2, column = 0,padx=5, pady=5, sticky = 'ew')
        self.segSAMModelOptions = ctk.CTkOptionMenu(master = self.SegmentationForm,
                                                values = ["ViT-H SAM Model", 
                                                          "ViT-L SAM Model", 
                                                          "ViT-B SAM Model"],command = self.optionmenu_callback)
        self.segSAMModelOptions.set("SAM Models")
        self.segSAMModelOptions.grid(row = 2, column = 1 ,padx=5, pady=5, sticky = 'ew')
        
        
    def RGBButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.PseudoRGBFrame = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 20,
                                        fg_color='white', 
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.RedbandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Red band number for Pseudo RGB Image:  ", anchor = 'w')
        self.RedbandLabel.grid(row = 0, column = 0, padx=5, pady=5, sticky = 'ew')
        self.RedbandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Red band number" )
        self.RedbandEntry.grid(row = 0, column = 1,padx=5, pady=5,sticky = 'ew')
                                   
        ## label and input field for savitzky golay derivative
        self.GreenbandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Green band number for Pseudo RGB Image:  ", anchor = 'w')
        self.GreenbandLabel.grid(row = 1, column = 0, padx=5, pady=5, sticky = 'ew')
        self.GreenbandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Green band number" )
        self.GreenbandEntry.grid(row = 1, column = 1,padx=5, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.BluebandLabel = ctk.CTkLabel(master = self.PseudoRGBFrame, text = "Enter the Blue band number for Pseudo RGB Image:  ", anchor = 'w')
        self.BluebandLabel.grid(row = 2, column = 0, padx=5, pady=5, sticky = 'ew')
        self.BluebandEntry = ctk.CTkEntry(master = self.PseudoRGBFrame, placeholder_text="Blue band number" )
        self.BluebandEntry.grid(row = 2, column = 1,padx=5, pady=5,sticky = 'ew')

    def EMRButton_callback(self):
        # Clear rightFormFrame
        for widget in self.rightPreferenceFormFrame.winfo_children():
            widget.destroy()
                ## user input forms on the right side of window for various buttons.
  
        self.EMRInfoFrame = frame(master=self.rightPreferenceFormFrame,  
                                        border_width= 20,
                                        fg_color='white', 
                                        side='left',  fill ='both')
        
        ## label and input field for savitzky golay window size
        self.BandNoLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the number of bands in your dataset:  ", anchor = 'w')
        self.BandNoLabel.grid(row = 0, column = 0, padx=5, pady=5, sticky = 'ew')
        self.BandNoEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Total number of bands" )
        self.BandNoEntry.grid(row = 0, column = 1,padx=5, pady=5,sticky = 'ew')
                                   
        ## label and input field for savitzky golay derivative
        self.FirstbandLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the first wavelength of range in nm:  ", anchor = 'w')
        self.FirstbandLabel.grid(row = 1, column = 0, padx=5, pady=5, sticky = 'ew')
        self.FirstbandEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="First nanometer" )
        self.FirstbandEntry.grid(row = 1, column = 1,padx=5, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.LastbandLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the last wavelength of range in nm:  ", anchor = 'w')
        self.LastbandLabel.grid(row = 2, column = 0, padx=5, pady=5, sticky = 'ew')
        self.LastbandEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Last nanometer" )
        self.LastbandEntry.grid(row = 2, column = 1,padx=5, pady=5,sticky = 'ew')
        
        ## label and input field for savitzky golay derivative
        self.SpectralResolutionLabel = ctk.CTkLabel(master = self.EMRInfoFrame, text = "Enter the spectral resolution of your sensor:  ", anchor = 'w')
        self.SpectralResolutionLabel.grid(row = 3, column = 0, padx=5, pady=5, sticky = 'ew')
        self.SpectralResolutionEntry = ctk.CTkEntry(master = self.EMRInfoFrame, placeholder_text="Spectral Resolution" )
        self.SpectralResolutionEntry.grid(row = 3, column = 1,padx=5, pady=5,sticky = 'ew')

 
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
        


class dataAnalysis(App):
    pass
        
app = App()
app.mainloop()

