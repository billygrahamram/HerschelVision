import customtkinter as ctk

def optionmenu_callback(choice):
    
    if choice == 'Exit':
        root.destroy()
    else:
        pass


root = ctk.CTk()
root.title("navigation menu")
root.geometry("900x800")

optionmenu = ctk.CTkOptionMenu(root, values=["New","Open","Save","Export","Exit"], command=optionmenu_callback)
optionmenu.set("File")
optionmenu.pack(side= 'left',padx=5, pady=10)

optionmenu = ctk.CTkOptionMenu(root, values=["Preferences","Undo"], command=optionmenu_callback)
optionmenu.set("Edit")
optionmenu.pack(side= 'left',padx=5, pady=10)

optionmenu = ctk.CTkOptionMenu(root, values=["Updates","Version","About", "Contact us"], command=optionmenu_callback)
optionmenu.set("About")
optionmenu.pack(side= 'left',padx=5, pady=10)

root.mainloop()
