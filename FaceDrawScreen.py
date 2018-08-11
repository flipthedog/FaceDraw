# FaceDrawScreen.py
# Purpose: To manage the tkinter facedraw screen

# Imports
import tkinter

# Home-made imports
import process_image
import ImageProject

# Code
root = tkinter.Tk()

# Frames
# Level 1
titleFrame = tkinter.Frame(root)
titleFrame.pack()
main_frame = tkinter.Frame(root)
main_frame.pack()

# Level 2
option_frame = tkinter.Frame(main_frame)
image_frame = tkinter.Frame(main_frame)
option_frame.grid(row=0, column=0, sticky='N')
image_frame.grid(row=1, column=0, sticky='N')

# Level 3 - image_frame


# Level 3 - options_frame


# Shown Image Elements
image_project = ImageProject.ImageProject

image_select_button = tkinter.Button(image_name_frame, text='Select Image', )