import customtkinter as ctk

class MainMenu():
    def __init__(self,obj):
         self.obj = obj
         FileOptionMenu = ctk.CTkOptionMenu(master=self.obj.menuBarFrame, values=["Home","New","Open","Save","Export","Exit"], command = self.optionmenu_callback)
         
    def optionmenu_callback(self,choice):
        ## method to select function to buttons in main menu.
        if choice == 'Exit':
            app.destroy()
        elif choice == 'Open':
            self.open()


