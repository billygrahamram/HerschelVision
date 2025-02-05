import os
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.data_preprocessing_utils import *
from utils.io_utils import *
from utils.variables_utils import *


class Crop_segment_windows(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def cropping_window(self):

        def cropped_get_resized_image_coordinates(event, canvas, tk_image, resized_tk):

            print("cropped get resized image coordinates........")
            # The event object contains the x and y coordinates of the mouse click
            x, y = int(event.x), int(event.y)

            # Calculate the size of the borders
            border_x = (canvas.winfo_width() - resized_tk.width()) / 2
            border_y = (canvas.winfo_height() - resized_tk.height()) / 2

            if border_x == 0:
                if y <= int(border_y):
                    pass
                elif y >= (int(border_y) + resized_tk.height()):
                    pass
                elif int(border_y) <= y <= (int(border_y) + resized_tk.height()):
                    imgX = x - int(border_x)
                    imgY = y - int(border_y)

                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()

                    scaled_img_X = round(imgX * x_scale_ratio)
                    scaled_img_Y = round(imgY * y_scale_ratio)
                    print("this is test of generateFinalSegmentedImage")
                    generate_final_segmented_image(
                        segmented_img=tk_image, x=scaled_img_X, y=scaled_img_Y
                    )

            elif border_y == 0:
                if x <= int(border_x):
                    pass
                elif x >= (int(border_x) + resized_tk.width()):
                    pass
                elif int(border_x) <= x <= (int(border_x) + resized_tk.width()):
                    imgX = x - int(border_x)
                    imgY = y - int(border_y)

                    x_scale_ratio = tk_image.width / resized_tk.width()
                    y_scale_ratio = tk_image.height / resized_tk.height()

                    scaled_img_X = round(imgX * x_scale_ratio)
                    scaled_img_Y = round(imgY * y_scale_ratio)
                    print("this is test of generateFinalSegmentedImage 2225")
                    generate_final_segmented_image(
                        segmented_img=tk_image, x=scaled_img_X, y=scaled_img_Y
                    )

        def generate_final_segmented_image(segmented_img, x, y):

            print("generate final segmented image method........")
            segmented_img = np.array(segmented_img)
            point_color = segmented_img[y, x]
            self.mask = np.all(segmented_img == point_color, axis=-1)
            extracted_point = np.where(
                self.mask[..., None], segmented_img, 255)

            # Convert the NumPy array back to a PIL Image
            extracted_point_img = Image.fromarray(
                extracted_point.astype("uint8"))

            for widget in right_cropped_image_frame.winfo_children():
                widget.destroy()

            cropped_img_cropping_canvas = ctk.CTkCanvas(
                right_cropped_image_frame,
                bg=self.parent.rgbValues(),
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )

            cropped_img_cropping_canvas.pack(expand=True, fill="both")
            cropped_img_cropping_canvas.bind(
                "<Configure>",
                lambda event: cropped_full_image(
                    event, extracted_point_img, canvas=cropped_img_cropping_canvas
                ),
            )

        def cropped_full_image(event, tk_image, canvas):
            print("cropped full image ........")
            # this function takes in a image and calculates it's dimension and the window dimension
            # and then makes sure that the image is fit to the window frame.

            canvas_ratio = event.width / event.height
            img_ratio = tk_image.size[0] / tk_image.size[1]

            if canvas_ratio > img_ratio:
                height = int(event.height)
                width = int(height * img_ratio)
            else:
                width = int(event.width)
                height = int(width / img_ratio)

            resized_image = tk_image.resize((width, height))
            resized_tk = ImageTk.PhotoImage(resized_image)

            canvas.create_image(
                int(event.width / 2),
                int(event.height / 2),
                anchor="center",
                image=resized_tk,
            )
            canvas.image = resized_tk

        def get_resized_canvas_image(tk_image, canvas):
            print("get resized canvas image........")
            # this function takes in a image and calculates it's dimension and the window dimension
            # and then makes sure that the image is fit to the window frame.

            canvas_ratio = canvas.winfo_width() / canvas.winfo_height()
            img_ratio = tk_image.size[0] / tk_image.size[1]

            if canvas_ratio > img_ratio:
                height = int(canvas.winfo_height())
                width = int(height * img_ratio)
            else:
                width = int(canvas.winfo_width())
                height = int(width / img_ratio)

            resized_image = tk_image.resize((width, height))
            resized_tk = ImageTk.PhotoImage(resized_image)

            return resized_tk

        def callback(event):
            print("callback........")
            # print ("clicked at", event.x, event.y)

            xypos.append([event.x, event.y])
            if len(xypos) > 1:
                ori_img_cropping_canvas.delete("box")  # delete the old rectangle
                x, y = xypos[0]
                x1, y1 = xypos[-1]
                ori_img_cropping_canvas.create_rectangle(
                    x, y, event.x, event.y, outline="red", tags="box", width=2
                )

        def get_cropped_image(canvas, image, xypos):
            print("get cropped image........")

            x, y = xypos[0]
            x1, y1 = xypos[-1]

            border_x = (canvas.winfo_width() -
                        self.parent.resized_tk.width()) / 2
            border_y = (canvas.winfo_height() -
                        self.parent.resized_tk.height()) / 2

            imgX = x - int(border_x)
            imgY = y - int(border_y)
            imgX1 = x1 - int(border_x)
            imgY1 = y1 - int(border_y)

            x_scale_ratio = image.width / self.parent.resized_tk.width()
            y_scale_ratio = image.height / self.parent.resized_tk.height()

            self.scaled_imgX = round(imgX * x_scale_ratio)
            self.scaled_imgY = round(imgY * y_scale_ratio)
            self.scaled_imgX1 = round(imgX1 * x_scale_ratio)
            self.scaled_imgY1 = round(imgY1 * y_scale_ratio)

            cropped_image = image.crop(
                (
                    self.scaled_imgX,
                    self.scaled_imgY,
                    self.scaled_imgX1,
                    self.scaled_imgY1,
                )
            )

            return cropped_image

        def display_cropped_image(event):
            print("display cropped image........")
            # Crop the image
            croppedImg = get_cropped_image(
                ori_img_cropping_canvas, self.parent.tk_image, xypos
            )

            xypos.clear()

            # Convert the cropped image to a PhotoImage

            for widget in right_cropped_image_frame.winfo_children():
                widget.destroy()

            cropped_img_cropping_canvas = ctk.CTkCanvas(
                right_cropped_image_frame,
                bg=self.parent.rgbValues(),
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )

            cropped_img_cropping_canvas.pack(expand=True, fill="both")
            cropped_img_cropping_canvas.bind(
                "<Configure>",
                lambda event: cropped_full_image(
                    event, croppedImg, canvas=cropped_img_cropping_canvas
                ),
            )

        def save_cropped_image():
            print("save cropped image........")
            self.parent.Dataloaded = False

            self.saveFile = tk.filedialog.asksaveasfile(
                defaultextension=".npy",
                filetypes=[
                    ("Numpy Array", "*.npy"),
                    ("Comma Separated Values", "*.csv"),
                    ("Text File", ".txt"),
                ],
            )
            if self.saveFile is not None:
                self.load_data_text = f"Saving cropped data ..."
                threading.Thread(target=save_cropped_image_dataloader).start()
                self.parent.parent.data_loading_screen()
                self.saveFile.close()

        def save_cropped_image_dataloader():
            print("save cropped image data loader........")
            data_to_save = crop_3d_image(
                self.parent.spectral_array,
                (self.scaled_imgX, self.scaled_imgY),
                (self.scaled_imgX1, self.scaled_imgY1),
            )
            save_datato_computer(data_to_save, self.saveFile.name)
            self.parent.Dataloaded = True

        def save_unfolded_cropped_image():
            print("save unfolded cropped image........")
            self.parent.Dataloaded = False

            self.saveFile = tk.filedialog.asksaveasfile(
                defaultextension=".npy",
                filetypes=[
                    ("Comma Separated Values", "*.csv"),
                    ("Text File", ".txt"),
                    ("Numpy Array", "*.npy"),
                ],
            )
            if self.saveFile is not None:
                self.load_data_text = f"Saving cropped data (unfolded) ..."
                threading.Thread(target=set_unfolded_dataloader).start()
                self.parent.data_loading_screen()
                self.saveFile.close()

        def set_unfolded_dataloader():
            print("set unfolded data loader........")
            dataToSave = crop_3d_image(
                self.spectral_array,
                (self.scaled_imgX, self.scaled_imgY),
                (self.scaled_imgX1, self.scaled_imgY1),
            )
            dataToSave = unfold(dataToSave)
            save_datato_computer(dataToSave, self.saveFile.name)
            self.parent.Dataloaded = True

        def save_segmented_image():
            print("save segmented image........")
            self.parent.Dataloaded = False

            self.saveFile = tk.filedialog.asksaveasfile(
                defaultextension=".npy",
                filetypes=[
                    ("Numpy Array", "*.npy"),
                    ("Comma Separated Values", "*.csv"),
                    ("Text File", ".txt"),
                ],
            )
            if self.saveFile is not None:
                self.load_data_text = f"Saving Segmented data (x,y,z) ..."
                threading.Thread(target=save_segmented_dataloader).start()
                self.parent.data_loading_screen()
                self.saveFile.close()

        def save_segmented_dataloader():
            print("save segmented data loader...")
            data_to_save = crop_3d_image(
                self.spectral_array,
                (self.scaled_imgX, self.scaled_imgY),
                (self.scaled_imgX1, self.scaled_imgY1),
            )
            print("Shape of cropped data:", data_to_save.shape)

            data_to_save = np.where(self.mask[..., None], data_to_save, 0)
            print("Shape of data after applying mask:", data_to_save.shape)
            save_datato_computer(data_to_save, self.saveFile.name)
            print("Data saved to:", self.saveFile.name)
            self.parent.parent.Dataloaded = True
            print("Dataloaded set to True")

        def save_unfolded_segmented_image():

            print("save unfolded segmented image........")
            self.parent.Dataloaded = False

            self.saveFile = tk.filedialog.asksaveasfile(
                defaultextension=".npy",
                filetypes=[
                    ("Numpy Array", "*.npy"),
                    ("Comma Separated Values", "*.csv"),
                    ("Text File", ".txt"),
                ],
            )
            if self.saveFile is not None:
                self.load_data_text = f"Saving unfolded Segmented data (x,y) ..."
                threading.Thread(
                    target=save_unfolded_segmented_dataloader).start()
                self.data_loading_screen()
                self.saveFile.close()

        def save_unfolded_segmented_dataloader():
            print("save unfolded segmented dataq loader........")
            dataToSave = crop_3d_image(
                self.spectral_array,
                (self.scaled_imgX, self.scaled_imgY),
                (self.scaled_imgX1, self.scaled_imgY1),
            )
            dataToSave = np.where(self.mask[..., None], dataToSave, 0)
            dataToSave = unfold(dataToSave)
            save_datato_computer(dataToSave, self.saveFile.name)
            self.parent.Dataloaded = True

        def apply_segmentation():
            print("apply segmentation........")
            # self.kcluster_no_seg_pre_pro = 2
            # self.kcluster_thres_pre_pro = 2
            # self.selected_SAM_model = 'ViT-B SAM Model'
            # self.default_segmentation_method = 'K means clustering'
            cropped_img = crop_3d_image(
                self.parent.spectral_array,
                (self.scaled_imgX, self.scaled_imgY),
                (self.scaled_imgX1, self.scaled_imgY1),
            )

            for widget in right_cropped_image_frame.winfo_children():
                widget.destroy()

            if (
                self.parent.default_properties.get("default_segmentation_method")
                == "K means clustering"
            ):

                segmented_img = kmeans_segmentation(
                    array=cropped_img,
                    clusters=self.parent.default_properties.get(
                        "kcluster_no_seg_pre_pro"),
                    bands=3,
                )

                # Rescale to 0-255
                segmented_img_rescaled = (
                    (segmented_img - np.min(segmented_img))
                    / (np.max(segmented_img) - np.min(segmented_img))
                    * 255
                )

                segmentedtk_image = Image.fromarray(
                    np.uint8(segmented_img_rescaled))

                numpy_image = np.array(segmentedtk_image)
                print(np.unique(numpy_image))

                cropped_img_cropping_canvas = ctk.CTkCanvas(
                    right_cropped_image_frame,
                    bg=self.parent.rgbValues(),
                    bd=0,
                    highlightthickness=0,
                    relief="ridge",
                )
                cropped_img_cropping_canvas.pack(expand=True, fill="both")
                cropped_img_cropping_canvas.bind(
                    "<Configure>",
                    lambda event: cropped_full_image(
                        event, segmentedtk_image, canvas=cropped_img_cropping_canvas
                    ),
                )
                cropped_img_cropping_canvas.bind(
                    "<1>",
                    lambda event: cropped_get_resized_image_coordinates(
                        event,
                        canvas=cropped_img_cropping_canvas,
                        tk_image=segmentedtk_image,
                        resized_tk=get_resized_canvas_image(
                            tk_image=segmentedtk_image, canvas=cropped_img_cropping_canvas
                        ),
                    ),
                )

            elif (
                self.parent.default_properties.get("default_segmentation_method")
                == "SAM Model"
            ):
                pass

        # Clear self.work_area_frame
        for widget in self.parent.work_area_frame.winfo_children():
            widget.destroy()

        # children to workMenuFrame
        left_original_image_frame = ctk.CTkFrame(master=self.parent.work_area_frame)
        right_cropped_image_frame = ctk.CTkFrame(master=self.parent.work_area_frame)
        left_bottom_button_cropping_frame = ctk.CTkFrame(
            master=self.parent.work_area_frame)
        righ_bottom_button_cropping_frame = ctk.CTkFrame(
            master=self.parent.work_area_frame)

        left_original_image_frame.place(x=0, y=0, relwidth=0.5, relheight=0.9)
        right_cropped_image_frame.place(
            relx=0.5, y=0, relwidth=0.5, relheight=0.9)
        left_bottom_button_cropping_frame.place(
            rely=0.9, x=0, relwidth=0.5, relheight=0.1)
        righ_bottom_button_cropping_frame.place(
            rely=0.9, relx=0.5, relwidth=0.5, relheight=0.1
        )

        left_bottom_button_cropping_frame.columnconfigure((0, 1, 2, 3), weight=1)
        left_bottom_button_cropping_frame.rowconfigure((0, 1), weight=1)
        righ_bottom_button_cropping_frame.columnconfigure((0, 1, 2, 3), weight=1)
        righ_bottom_button_cropping_frame.rowconfigure((0, 1), weight=1)

        save_cropped_image_button = ctk.CTkButton(
            master=righ_bottom_button_cropping_frame,
            text="Save \n Cropped Image (x,y,z)",
            command=save_cropped_image,
        )
        save_unfolded_cropped_image_button = ctk.CTkButton(
            master=righ_bottom_button_cropping_frame,
            text="Save \n Unfolded Cropped Image (x,y)",
            command=save_unfolded_cropped_image,
        )
        save_segmented_image_button = ctk.CTkButton(
            master=righ_bottom_button_cropping_frame,
            text="Save \n Segmented Image",
            command=save_segmented_image,
        )
        save_unfolded_segmented_image_button = ctk.CTkButton(
            master=righ_bottom_button_cropping_frame,
            text="Save \n Unfolded Segmented Image",
            command=save_unfolded_segmented_image,
        )

        save_cropped_image_button.grid(
            row=1, column=0, sticky="nsew", pady=10, padx=10)
        save_unfolded_cropped_image_button.grid(
            row=1, column=1, sticky="nsew", pady=10, padx=10
        )
        save_segmented_image_button.grid(
            row=1, column=2, sticky="nsew", pady=10, padx=10)
        save_unfolded_segmented_image_button.grid(
            row=1, column=3, sticky="nsew", pady=10, padx=10
        )

        # applyCroppingImageButton = ctk.CTkButton(master = leftBottomButtonCroppingFrame,
        #                                             text = 'Apply \n Cropping',
        #                                             command= savecroppedImage)
        apply_segmentation_image_button = ctk.CTkButton(
            master=left_bottom_button_cropping_frame,
            text="Apply \n Segmentation",
            command=apply_segmentation,
        )

        # applyCroppingImageButton.grid(row =1, column =0, columnspan =2, sticky = 'nsew', pady= 10, padx=10)
        apply_segmentation_image_button.grid(
            row=1, column=2, columnspan=2, sticky="nsew", pady=10, padx=10
        )

        if self.parent.raw_img_dir == None:
            pass
        else:
            for widget in left_original_image_frame.winfo_children():
                widget.destroy()
            xypos = []

            ori_img_cropping_canvas = ctk.CTkCanvas(
                left_original_image_frame,
                bg=self.parent.rgbValues(),
                bd=0,
                highlightthickness=0,
                relief="ridge",
            )

            ori_img_cropping_canvas.pack(expand=True, fill="both")
            ori_img_cropping_canvas.bind(
                "<Configure>",
                lambda event: self.parent.full_image(
                    event, tk_image=self.parent.tk_image, canvas=ori_img_cropping_canvas
                ),
            )
            ori_img_cropping_canvas.bind("<B1-Motion>", callback)
            ori_img_cropping_canvas.bind(
                "<ButtonRelease-1>", display_cropped_image)
