import customtkinter as ctk

ctk.set_appearance_mode("white")

def frame(master,
          corner_radius=0,
          fg_color='gray',
          border_width=5,
          border_color="white",
          side='left',
          fill = 'both',
          expand = True,
          width = 100,
          height = 100):
    
    frame = ctk.CTkFrame(master=master, 
                         corner_radius=corner_radius, 
                         fg_color=fg_color, 
                         border_width=border_width, 
                         border_color=border_color,
                         width = width,
                         height = height)
    frame.pack(side=side, fill=fill, expand=expand)
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
    
        self.Leftframe = frame(master=self, side='left', border_width= 0)
        self.Leftframe1 = frame(master=self.Leftframe, side = 'top', height = 900)
        self.leftbutton = button(master=self.Leftframe,command = button_event, text = "Open Image")
        
        
        self.Rightframe = frame(master=self, side='right', border_width= 0)
        self.Rightframe1 = frame(master=self.Rightframe, side='top')
        self.Rightframe2 = frame(master=self.Rightframe, side='top')
        



        
app = App()
app.mainloop()

