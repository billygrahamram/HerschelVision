import os
import tkinter as tk
import threading
from utils.variables_utils import *
from utils.io_utils import *
from utils.data_preprocessing_utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter import  messagebox


class CropSegmentWindows(ctk.CTkFrame):
    def __init__(self,parent):
         super().__init__(parent)
         self.parent = parent

    def croppingWindow(self):
        
        def cropped_getresizedImageCoordinates(event, canvas, tk_image, resized_tk):
    
            print("cropped get resized image coordinates........")
            # The event object contains the x and y coordinates of the mouse click
            x, y = int(event.x), int(event.y)
            
            
            # Calculate the size of the borders
            border_x = (canvas.winfo_width() - resized_tk.width()) / 2
            border_y = (canvas.winfo_height() - resized_tk.height()) / 2
            
            if border_x == 0:
                if y <= int(border_y):
                    pass
                elif y>= (int(border_y) + resized_tk.height()):
                    pass
                elif int(border_y) <= y <= (int(border_y) + resized_tk.height()):
                    imgX = x-int(border_x)
                    imgY = y-int(border_y)
                    
                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()
                    
                    scaled_imgX = round(imgX * x_scale_ratio)
                    scaled_imgY = round(imgY * y_scale_ratio)
                    print("this is test of generateFinalSegmentedImage")
                    generateFinalSegmentedImage(segmented_img = tk_image, x = scaled_imgX, y = scaled_imgY)
                
            elif border_y == 0:
                if x <= int(border_x):
                    pass
                elif x >= (int(border_x) + resized_tk.width()):
                    pass
                elif int(border_x) <= x <= (int(border_x) + resized_tk.width()):
                    imgX = x-int(border_x)
                    imgY = y-int(border_y)
            
                    
                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()
                    
                    scaled_imgX = round(imgX * x_scale_ratio)
                    scaled_imgY = round(imgY * y_scale_ratio)
                    print("this is test of generateFinalSegmentedImage 2225")
                    generateFinalSegmentedImage(segmented_img = tk_image, x = scaled_imgX, y = scaled_imgY)
        
        
        def generateFinalSegmentedImage(segmented_img, x,y):
            
            print("generate final segmented image method........")
            segmented_img = np.array(segmented_img)
            point_color = segmented_img[y,x]
            self.mask = np.all(segmented_img == point_color, axis=-1)
            extracted_point = np.where(self.mask[..., None], segmented_img, 255)
            
            # Convert the NumPy array back to a PIL Image
            extracted_point_img = Image.fromarray(extracted_point.astype('uint8'))
            
            for widget in rightCroppedImageFrame.winfo_children():
                widget.destroy()
                
            croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                bg = self.rgbValues(),
                bd =0,
                highlightthickness=0,
                relief='ridge')
            
            croppedImgcroppingCanvas.pack(expand = True, fill='both')
            croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, extracted_point_img, canvas=croppedImgcroppingCanvas))

        def cropped_full_image(event, tk_image, canvas):
            print("cropped full image ........")
            # this function takes in a image and calculates it's dimension and the window dimension
            # and then makes sure that the image is fit to the window frame.
        
            canvas_ratio = event.width / event.height
            img_ratio = tk_image.size[0]/tk_image.size[1]
            
            if canvas_ratio > img_ratio: 
                height = int(event.height)
                width = int(height * img_ratio)
            else: 
                width = int(event.width)
                height = int(width/img_ratio)
                
                
            resized_image = tk_image.resize((width, height))
            resized_tk = ImageTk.PhotoImage(resized_image)
            
            canvas.create_image(
                int(event.width/2), 
                int(event.height/2), 
                anchor = 'center',
                image=resized_tk)
            canvas.image = resized_tk
            
        def getResizedCanvasImage(tk_image, canvas):
            print("get resized canvas image........")
            # this function takes in a image and calculates it's dimension and the window dimension
            # and then makes sure that the image is fit to the window frame.
        
            canvas_ratio = canvas.winfo_width() / canvas.winfo_height()
            img_ratio = tk_image.size[0]/tk_image.size[1]
            
            if canvas_ratio > img_ratio: 
                height = int(canvas.winfo_height())
                width = int(height * img_ratio)
            else: 
                width = int(canvas.winfo_width())
                height = int(width/img_ratio)
                
                
            resized_image = tk_image.resize((width, height))
            resized_tk = ImageTk.PhotoImage(resized_image)

            return resized_tk
            
        
        def callback(event):
            print("callback........")
            # print ("clicked at", event.x, event.y)
            
            xypos.append([event.x, event.y])
            if len(xypos) > 1:
                oriImgcroppingCanvas.delete("box")  # delete the old rectangle
                x, y = xypos[0]
                x1, y1 = xypos[-1]
                oriImgcroppingCanvas.create_rectangle(x, y, event.x, event.y, outline="red", tags="box", width=2)
            
        def getCroppedimage(canvas, image, xypos):
            print("get cropped image........")

            x, y = xypos[0]
            x1, y1 = xypos[-1]
            
            border_x = (canvas.winfo_width() - self.resized_tk.width()) / 2
            border_y = (canvas.winfo_height() - self.resized_tk.height()) / 2

            imgX = x-int(border_x)
            imgY = y-int(border_y)
            imgX1 = x1-int(border_x)
            imgY1 = y1-int(border_y)
            
            x_scale_ratio = image.width / self.resized_tk.width()
            y_scale_ratio = image.height / self.resized_tk.height()
            
            self.scaled_imgX = round(imgX * x_scale_ratio)
            self.scaled_imgY = round(imgY * y_scale_ratio)
            self.scaled_imgX1 = round(imgX1 * x_scale_ratio)
            self.scaled_imgY1 = round(imgY1 * y_scale_ratio)
            
            croppedImage = image.crop((self.scaled_imgX, self.scaled_imgY, self.scaled_imgX1, self.scaled_imgY1))
            
            return croppedImage

        def display_cropped_image(event):
            print("display cropped image........")
            # Crop the image
            croppedImg = getCroppedimage(oriImgcroppingCanvas, self.tk_image, xypos)
            
            xypos.clear()
            
            # Convert the cropped image to a PhotoImage
           
            for widget in rightCroppedImageFrame.winfo_children():
                widget.destroy()
                
            croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                bg = self.rgbValues(),
                bd =0,
                highlightthickness=0,
                relief='ridge')
            
            croppedImgcroppingCanvas.pack(expand = True, fill='both')
            croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, croppedImg, canvas=croppedImgcroppingCanvas))
            
            
    
        def savecroppedImage():
            print("save cropped image........")
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving cropped data ...'
                threading.Thread(target = savecroppedimageDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def savecroppedimageDataloader():
            print("save cropped image data loader........")
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.Dataloaded = True
        
        
        def saveUnfoldedcroppedImage():
            print("save unfolded cropped image........")
            self.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Comma Separated Values", "*.csv"),
                                                                ("Text File", ".txt"),
                                                                ("Numpy Array", "*.npy"),
                                                                ])
            if self.saveFile is not None:
                self.loadDataText = f'Saving cropped data (unfolded) ...'
                threading.Thread(target = setUnfoldedDataloader).start()
                self.parent.dataLoadingScreen()
                self.saveFile.close()
            
        def setUnfoldedDataloader():
            print("set unfolded data loader........")
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            dataToSave = unfold(dataToSave)
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.parent.parent.Dataloaded = True
            
            
        def saveSegmentedImage():
            print("save segmented image........")
            self.parent.parent.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving Segmented data (x,y,z) ...'
                threading.Thread(target = saveSegmentedDataloader).start()
                self.parent.dataLoadingScreen()
                self.saveFile.close()
                
                
            
        def saveSegmentedDataloader():
            print("save segmented data loader...")
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            print("Shape of cropped data:", dataToSave.shape)
            
            dataToSave = np.where(self.mask[..., None], dataToSave, 0)
            print("Shape of data after applying mask:", dataToSave.shape)  
            saveDatatoComputer(dataToSave, self.saveFile.name)
            print("Data saved to:", self.saveFile.name)
            self.parent.parent.Dataloaded = True
            print("Dataloaded set to True")
            
            
        def saveUnfoldedSegmentedImage():
            
            print("save unfolded segmented image........")
            self.parent.parent.Dataloaded = False
            
            self.saveFile = tk.filedialog.asksaveasfile(defaultextension = '.npy',
                                                filetypes = [("Numpy Array", "*.npy"),
                                                             ("Comma Separated Values", "*.csv"),
                                                             ("Text File", ".txt")])
            if self.saveFile is not None:
                self.loadDataText = f'Saving unfolded Segmented data (x,y) ...'
                threading.Thread(target = saveUnfoldedSegmentedDataloader).start()
                self.dataLoadingScreen()
                self.saveFile.close()
            
        def saveUnfoldedSegmentedDataloader():
            print("save unfolded segmented dataq loader........")
            dataToSave = crop_3d_image(self.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            dataToSave = np.where(self.mask[..., None], dataToSave, 0)
            dataToSave = unfold(dataToSave)
            saveDatatoComputer(dataToSave, self.saveFile.name)
            self.parent.parent.Dataloaded = True
            
            
        def applySegmentation():
            print("apply segmentation........")
            # self.KclusterNoSegPrePro = 2
            # self.KClusterThresPrePro = 2
            # self.selectedSAMModel = 'ViT-B SAM Model'
            # self.defaultSegmentationMethod = 'K means clustering'
            croppedImg = crop_3d_image(self.parent.spectral_array,(self.scaled_imgX, self.scaled_imgY), (self.scaled_imgX1, self.scaled_imgY1))
            
            for widget in rightCroppedImageFrame.winfo_children():
                    widget.destroy()
                    
            if self.defaultSegmentationMethod == "K means clustering":
                
                segmentedImg = kmeansSegmentation(array= croppedImg, 
                                                  clusters = self.KclusterNoSegPrePro, 
                                                  bands = 3)
                
                # Rescale to 0-255
                segmentedImg_rescaled = (segmentedImg - np.min(segmentedImg)) / (np.max(segmentedImg) - np.min(segmentedImg)) * 255
                
                segmentedtk_image = Image.fromarray(np.uint8(segmentedImg_rescaled))
                
                numpy_image = np.array(segmentedtk_image)
                print(np.unique(numpy_image))
  

                croppedImgcroppingCanvas = ctk.CTkCanvas(rightCroppedImageFrame,
                    bg = self.rgbValues(),
                    bd = 0,
                    highlightthickness=0,
                    relief='ridge')
                croppedImgcroppingCanvas.pack( expand =True, fill='both')
                croppedImgcroppingCanvas.bind('<Configure>',lambda event: cropped_full_image(event, segmentedtk_image, canvas=croppedImgcroppingCanvas))
                croppedImgcroppingCanvas.bind('<1>', lambda event: cropped_getresizedImageCoordinates(event, canvas = croppedImgcroppingCanvas, tk_image = segmentedtk_image,resized_tk= getResizedCanvasImage(tk_image=segmentedtk_image,canvas =croppedImgcroppingCanvas)))

                
            elif self.defaultSegmentationMethod == "SAM Model":
                pass

        # Clear self.workAreaFrame
        for widget in self.parent.workAreaFrame.winfo_children():
            widget.destroy()

        
        ## children to workMenuFrame 
        leftOriginalImageFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        rightCroppedImageFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        leftBottomButtonCroppingFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        righBottomButtonCroppingFrame = ctk.CTkFrame(master = self.parent.workAreaFrame)
        
        leftOriginalImageFrame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
        rightCroppedImageFrame.place(relx = 0.5, y = 0, relwidth = 0.5, relheight = 0.9)
        leftBottomButtonCroppingFrame.place(rely = 0.9, x=0, relwidth = 0.5, relheight = 0.1)
        righBottomButtonCroppingFrame.place(rely = 0.9, relx=0.5, relwidth = 0.5, relheight = 0.1)


        leftBottomButtonCroppingFrame.columnconfigure((0,1,2,3), weight = 1)
        leftBottomButtonCroppingFrame.rowconfigure((0,1), weight = 1)
        righBottomButtonCroppingFrame.columnconfigure((0,1,2,3), weight = 1)
        righBottomButtonCroppingFrame.rowconfigure((0,1), weight = 1)
        
        
        
        
        saveCroppedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Cropped Image (x,y,z)',
                                                    command= savecroppedImage)
        saveunfoldedCroppedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Unfolded Cropped Image (x,y)',
                                                    command= saveUnfoldedcroppedImage)
        saveSegmentedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Segmented Image',
                                                    command= saveSegmentedImage)
        saveunfoldedSegmentedImageButton = ctk.CTkButton(master = righBottomButtonCroppingFrame, 
                                                    text = 'Save \n Unfolded Segmented Image',
                                                    command= saveUnfoldedSegmentedImage)
        
        saveCroppedImageButton.grid(row =1, column =0, sticky = 'nsew', pady= 10, padx=10)
        saveunfoldedCroppedImageButton.grid(row =1, column =1, sticky = 'nsew', pady= 10, padx=10)
        saveSegmentedImageButton.grid(row =1, column =2, sticky = 'nsew', pady= 10, padx=10)
        saveunfoldedSegmentedImageButton.grid(row =1, column =3, sticky = 'nsew', pady= 10, padx=10)
        
        
        # applyCroppingImageButton = ctk.CTkButton(master = leftBottomButtonCroppingFrame, 
        #                                             text = 'Apply \n Cropping',
        #                                             command= savecroppedImage)
        applySegmentationImageButton = ctk.CTkButton(master = leftBottomButtonCroppingFrame, 
                                                    text = 'Apply \n Segmentation',
                                                    command= applySegmentation)
        
        # applyCroppingImageButton.grid(row =1, column =0, columnspan =2, sticky = 'nsew', pady= 10, padx=10)
        applySegmentationImageButton.grid(row =1, column =2, columnspan =2 ,sticky = 'nsew', pady= 10, padx=10)

        
        
        

        if self.parent.raw_img_dir == None:
            pass
        else:
            for widget in leftOriginalImageFrame.winfo_children():
                widget.destroy()
            xypos = []
            
            oriImgcroppingCanvas = ctk.CTkCanvas(leftOriginalImageFrame,
                            bg = self.parent.rgbValues(),
                            bd =0,
                            highlightthickness=0,
                            relief='ridge')
        
            
            oriImgcroppingCanvas.pack(expand =True, fill='both')
            oriImgcroppingCanvas.bind('<Configure>',lambda event: self.parent.full_image(event, tk_image= self.parent.tk_image, canvas=oriImgcroppingCanvas))
            oriImgcroppingCanvas.bind("<B1-Motion>", callback)
            oriImgcroppingCanvas.bind("<ButtonRelease-1>", display_cropped_image)

