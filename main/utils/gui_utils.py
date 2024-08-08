import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from utils.image_process_utils import *

def create_canvas_with_image(obj,value=None):
    if value ==None:
        rgb_img = create_pseudo_rgb(obj.spectral_array)
        pil_image = Image.fromarray(cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB))
        obj.tk_image = ImageTk.PhotoImage(pil_image)
    else:
        value = int(float(value))
        single_band_img = single_band(obj.spectral_array, int(value))
        obj.tk_image = Image.fromarray(np.uint8(single_band_img))
                  
    # Destroy existing widgets in the frame
    for widget in obj.leftOriginalImgFrame.winfo_children():
        widget.destroy()
        
    # Create the canvas
    openCanvas = ctk.CTkCanvas(obj.leftOriginalImgFrame, 
                                bg=obj.rgbValues(),
                                bd=0,
                                highlightthickness=0,
                                relief='ridge')
        
    # Pack the canvas to fill the frame
    openCanvas.pack(expand=True, fill='both')

    # Draw the image on the canvas
    openCanvas.create_image(0, 0, image=obj.tk_image, anchor='nw')

    # Bind the events to the canvas
    openCanvas.bind('<Configure>', lambda event: obj.full_image(event, obj.tk_image, canvas=openCanvas))
    openCanvas.bind('<1>', lambda event: obj.getresizedImageCoordinates(event, canvas=openCanvas, image=obj.tk_image))
    
    openCanvas.update()
