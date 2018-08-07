# The main file of the facedraw program
import process_image
import create_g_code
import cv2 as cv

import os

import time
import tkinter
from tkinter import filedialog
from tkinter import Label
import PIL
from PIL import Image
from PIL import ImageTk

# UI
root = tkinter.Tk()

# Frames
# Title frame
title = tkinter.Frame(root)
title.grid(row=0, sticky='n')

# Image frames
image_frame = tkinter.Frame(root)
image_frame.grid(row=1, column=0, sticky='W')
image_frame2 = tkinter.Frame(root)
image_frame2.grid(row=2, column=0, sticky='W')

# Options frame
options_frame = tkinter.Frame(root)
options_frame.grid(row=1, column=1, sticky='E')
image_name_frame = tkinter.Frame(options_frame)
image_name_frame.grid(row=0,sticky='N')
blur_option = tkinter.Frame(options_frame)
blur_option.grid(row=1, sticky='N')
contour_option = tkinter.Frame(options_frame)
contour_option.grid(row=2, sticky='N')
threshold_option = tkinter.Frame(options_frame)
threshold_option.grid(row=3, sticky='N')
edgedetection_option = tkinter.Frame(options_frame)
edgedetection_option.grid(row=4, sticky='N')
morph_option = tkinter.Frame(options_frame)
morph_option.grid(row=5,sticky='N')

# Image options

def selectFileToOpen():
    user_selected_image = filedialog.askopenfilename(initialdir="./images", title='FaceDraw: Open File')
    # Opening the image
    path, file_name = os.path.split(user_selected_image)
    cvimage = process_image.openImage(file_name)
    cvimage = cv.cvtColor(cvimage, cv.COLOR_BGR2RGB)

    updateWindowImages(cvimage,user_selected_image)

image_select_button = tkinter.Button(image_name_frame, text='Select Image', command=selectFileToOpen)
image_select_button.grid(row=0, column=0)

# updateWindow()
# Purpose: Update the main tkinter window
def refresh():
    if threshold_type is "gaussian":
        threshold_gaussiansize_box.grid(row=0, column=2)

refresh_button = tkinter.Button(image_name_frame, text='Refresh', command=refresh)
refresh_button.grid(row=0, column=1)

# Blur Elements
blur_check = tkinter.IntVar()
blur_checkbox = tkinter.Checkbutton(blur_option, text = "Blur Image", variable = blur_check, onvalue = 1, offvalue = 0)
blur_checkbox.grid(row=0, column=0)
blur_type_options = {'regular', 'median', 'bilateral'}
blur_type = tkinter.StringVar()
blur_menu = tkinter.OptionMenu(blur_option, blur_type, *blur_type_options)
blur_type.set("Choose Filter")
blur_menu.grid(row=0,column=1)

# Contour Elements
contour_check = tkinter.IntVar()
contour_checkbox = tkinter.Checkbutton(contour_option, text = "Find Contours", variable = contour_check, onvalue = 1, offvalue = 0)
contour_checkbox.pack()

# Threshold Elements
threshold_check = tkinter.IntVar()
threshold_checkbox = tkinter.Checkbutton(threshold_option, text = "Perform Thresholding", variable = threshold_check, onvalue = 1, offvalue = 0)
threshold_checkbox.grid(row=0, column=0)
threshold_type_options = {'regular', 'gaussian', 'mean'}
threshold_type = tkinter.StringVar()
threshold_menu = tkinter.OptionMenu(threshold_option, threshold_type, *threshold_type_options)
threshold_type.set("Choose Filter")
threshold_menu.grid(row=0, column=1)
threshold_gaussiansize = tkinter.IntVar()
threshold_gaussiansize_box = tkinter.Entry(threshold_option)

# Edge Detection
edge_check = tkinter.IntVar()
edge_checkbox = tkinter.Checkbutton(edgedetection_option, text = "Perform Edge Detection", variable = edge_check, onvalue = 1, offvalue = 0)
edge_checkbox.pack()

# Morphing
dilate_check = tkinter.IntVar()
erode_check = tkinter.IntVar()
dilate_checkbox = tkinter.Checkbutton(morph_option, text = "Dilate Image", variable = dilate_check, onvalue = 1, offvalue = 0)
erode_checkbox = tkinter.Checkbutton(morph_option, text = "Erode Image", variable = erode_check, onvalue = 1, offvalue = 0)
erode_checkbox.pack()
dilate_checkbox.pack()

# Title
titleLabel = Label(title, text="FaceDraw", bg="#000fff")
titleLabel.grid(row=0, sticky='N')

# Image frame
image_frame.grid(row=1, sticky='W')
image_frame2.grid(row=2, sticky='W')

# Options frame
options_frame.grid(row=1, sticky='E')

# Set window size
root.geometry("800x700")

# convertImageToTk()
# Purpose: Convert a python-cv image to tkinter image
# Input: cv_image: a python-cv image to convert
# Output: tk_image: A tkinter image
def convertImageToTk(cv_image, resize, width, height):
    pil_image = Image.fromarray(cv_image)
    if resize:
        resized_image = pil_image.resize((width, height), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(resized_image)
    else:
        tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

# # updateWindow()
# # Purpose: Update the main tkinter window
# def updateWindow():
#     new_image = getNewProcessedImage()
#     processed_image_label.configure(image=processed_image_tk)
#     root.after(3000,updateWindow)

def updateWindowImages(cvimage, selected_image_name):
    # Convert image to PIL Image, then to Tkinter image
    # Original image GUI variables
    original_image = convertImageToTk(cvimage, True, 400, 300)
    o_image_text = tkinter.StringVar()
    path, file_name = os.path.split(selected_image_name)
    o_image_text.set("Your image: " + file_name)
    original_image_label_text = tkinter.Label(image_frame, textvariable=o_image_text, anchor='center')
    original_image_label_text.grid(row=0, sticky='N')
    original_image_label = tkinter.Label(image_frame, image=original_image, anchor='center')
    original_image_label.grid(row=1, sticky='N')

    # Processed image GUI variables

    # processed_image = getNewProcessedImage(cvimage)
    # processed_image_tk = convertImageToTk(processed_image, True, 400, 300)
    # p_image_text = tkinter.StringVar()
    # p_image_text.set("Your processed image: ")
    # processed_image_label_text = tkinter.Label(image_frame2, textvariable=p_image_text, anchor='center')
    # processed_image_label_text.grid(row=0, sticky='N')
    # processed_image_label = tkinter.Label(image_frame2, image=processed_image_tk, anchor='center')
    # processed_image_label.grid(row=1, sticky='N')

# getNewProcessedImage()
# Purpose: Find a new processed image, with user settings
# Input: cv_image: An image opened by open-cv
# Output: tkinter_image: The image to be displayed by tkinter
def getNewProcessedImage(cv_image):
    gray_image = process_image.grayImage(cv_image)

    return gray_image
    # If statements to process user filter options
    if blur_check is 1:
        # Blur the image

        if blur_type is not "Choose Filter":
            blur_image = process_image.blurImage(gray_image, blur_type)

    else:
        blur_image = gray_image

    if contour_check is 1:
        # Find contours of the image

        contour_image = process_image.contourImage(blur_image)

    else:

        contour_image = blur_image

    if threshold_check is 1:

        threshold_image = process_image.thresholdImage(blur_image, threshold_type)

    else:

        threshold_image = blur_image

    return threshold_image

# Create G-code from the processed image
# create_g_code.image_to_gcode(processed_image, 0.3, True, "test_1.gcode")

#root.after(100, refresh)
root.mainloop()