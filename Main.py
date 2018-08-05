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

# Image frames
image_frame = tkinter.Frame(root)
image_frame2 = tkinter.Frame(root)

# Options frame
options_frame = tkinter.Frame(root)
image_name_frame = tkinter.Frame(options_frame).grid(row=0,sticky='N')
blur_option = tkinter.Frame(options_frame).grid(row=0, sticky='N')
contour_option = tkinter.Frame(options_frame).grid(row=1, sticky='N')
threshold_option = tkinter.Frame(options_frame).grid(row=2, sticky='N')
morph_option = tkinter.Frame(options_frame).grid(row=3,sticky='N')
edgedetection_option = tkinter.Frame(options_frame).grid(row=4, sticky='N')


# Title
titleLabel = Label(title, text="FaceDraw", bg="#000fff")
titleLabel.grid(row=0, sticky='N')
titleLabel.pack()

# Image frame
image_frame.grid(row=1, sticky='W')
image_frame2.grid(row=2, sticky='W')

# Options frame
options_frame.grid(row=1, sticky='E')

# Options controls


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
# Update the main tkinter window
def updateWindow():
    processed_image_label.configure(image=processed_image_tk)

    root.after(3000,updateWindow)

def getNewProcessedImage(image_name):
    None

# Opening the image
image_name = 'pap_1.png'
cvimage = process_image.openImage(image_name)
cvimage = cv.cvtColor(cvimage, cv.COLOR_BGR2RGB)

# Convert image to PIL Image, then to Tkinter image
original_image = convertImageToTk(cvimage, True, 400, 300)

processed_image = process_image.processImage(image_name, False)
processed_image_tk = convertImageToTk(processed_image, True, 200, 150)
processed_image_label = tkinter.Label(image_frame2, image=processed_image_tk)
processed_image_label.pack(side="bottom")

create_g_code.image_to_gcode(processed_image, 0.3, True, "test_1.gcode")

original_image_label = tkinter.Label(image_frame, image=original_image)
original_image_label.pack()

root.after(100, updateWindow)
root.mainloop()

