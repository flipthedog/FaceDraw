# The main file of the facedraw program
import process_image
import create_g_code
import cv2 as cv

import tkinter
from tkinter import StringVar
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
blur_option.grid(row=0, sticky='N')
contour_option = tkinter.Frame(options_frame)
contour_option.grid(row=1, sticky='N')
threshold_option = tkinter.Frame(options_frame)
threshold_option.grid(row=2, sticky='N')
morph_option = tkinter.Frame(options_frame)
morph_option.grid(row=3,sticky='N')
edgedetection_option = tkinter.Frame(options_frame)
edgedetection_option.grid(row=4, sticky='N')

# Option elements

# Blur Elements
blur_check = tkinter.IntVar()
blur_checkbox = tkinter.Checkbutton(blur_option, text = "Blur Image", variable = blur_check, onvalue = 1, offvalue = 0)
blur_checkbox.pack()

# Contour Elements
contour_check = tkinter.IntVar()
contour_checkbox = tkinter.Checkbutton(contour_option, text = "Contour Image", variable = contour_check, onvalue = 1, offvalue = 0)
contour_checkbox.pack()

# Threshold Elements
thresh


# Title
titleLabel = Label(title, text="FaceDraw", bg="#000fff")
titleLabel.grid(row=0, sticky='N')

# Image frame
image_frame.grid(row=1, sticky='W')
image_frame2.grid(row=2, sticky='W')

# Options frame
options_frame.grid(row=1, sticky='E')

# Set window size
root.geometry("300x300")

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

# updateWindow()
# Purpose: Update the main tkinter window
def updateWindow():
    processed_image_label.configure(image=processed_image_tk)
    root.after(3000,updateWindow)

def getNewProcessedImage(opened_image):
    gray_image = process_image.grayImage(opened_image)

    None

# Opening the image
image_name = 'pap_1.png'
cvimage = process_image.openImage(image_name)
cvimage = cv.cvtColor(cvimage, cv.COLOR_BGR2RGB)

# Convert image to PIL Image, then to Tkinter image
# Original image GUI variables
original_image = convertImageToTk(cvimage, True, 400, 300)
o_image_text = tkinter.StringVar()
o_image_text.set("Your image: " + image_name)
original_image_label_text = tkinter.Label(image_frame, textvariable=o_image_text, anchor='center').grid(row=0, sticky='N')
original_image_label = tkinter.Label(image_frame, image=original_image, anchor='center')
original_image_label.grid(row=1, sticky='N')

# Processed image GUI variables
processed_image = process_image.processImage(image_name, False)
processed_image_tk = convertImageToTk(processed_image, True, 400, 300)
p_image_text = tkinter.StringVar()
p_image_text.set("Your processed image: ")
processed_image_label_text = tkinter.Label(image_frame2, textvariable=p_image_text, anchor='center').grid(row=0, sticky='N')
processed_image_label = tkinter.Label(image_frame2, image=processed_image_tk, anchor='center')
processed_image_label.grid(row=1, sticky='N')

# Create G-code from the processed image
create_g_code.image_to_gcode(processed_image, 0.3, True, "test_1.gcode")

root.after(100, updateWindow)
root.mainloop()