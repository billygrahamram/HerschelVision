from tkinter import *

root = Tk()
root.geometry("500x500")
xypos = []
    
    
def callback(event):
    print ("clicked at", event.x, event.y)

    xypos.append([event.x, event.y])
    if len(xypos) > 1:
        frame.delete("box")  # delete the old rectangle
        x1, y1 = xypos[0]
        frame.create_rectangle(x1, y1, event.x, event.y, outline="red", tags="box", width=2)

def on_release(event):
    # save first and last values in xypos when mouse button is released
    if len(xypos) > 1:
        x1, y1 = xypos[0]
        x2, y2 = xypos[-1]
        print("First:", (x1, y1), "Last:", (x2, y2))
    
    elif len(xypos) == 1:
        x1, y1 = x2, y2 = xypos[0]
        print("First and Last:", (x1, y1))

    else:
        print("List is empty")


frame = Canvas(root)
frame.bind("<B1-Motion>", callback)
frame.bind("<ButtonRelease-1>", on_release)



frame.pack(expand =True, fill= 'both')

root.mainloop()



