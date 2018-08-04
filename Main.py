# The main file of the facedraw program
import process_image
import create_g_code
import cv2 as cv

import tkinter
from tkinter import StringVar
from tkinter import Label
import PIL
from PIL import Image
from PIL import ImageTransform

# UI
root = tkinter.Tk()

# Frames
title = tkinter.Frame(root)

image_frame = tkinter.Frame(root)
options_frame = tkinter.Frame(root)

# Title
titleLabel = Label(title, text="FaceDraw", bg="#000fff")
titleLabel.grid(row=0, sticky='N')
titleLabel.pack()

# Image frame
image_frame.grid(row=1, sticky='W')

# Options frame
options_frame.grid(row=1, sticky='E')

# Set window size
root.geometry("300x300")

# Opening the image
image_name = 'pap_1.png'
cvimage = process_image.openImage(image_name)

pil_image = Image.fromarray(cvimage)
tk_image =
processed_image = process_image.processImage(image_name, False)

create_g_code.image_to_gcode(processed_image, 0.3, True, "test_1.gcode")

def updateWindow():
    image_label = tkinter.Label(image_frame, image=pil_image)

    root.after(100,updateWindow())

updateWindow()
root.mainloop()