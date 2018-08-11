# FaceDrawScreenHelpers.py
# Different Helper functions for FaceDrawScreen.py

import tkinter
from tkinter import filedialog
import os

import process_image

# selectFileToOpen
# Purpose: Open a file based on user input, call window update function
# Input: None
# Output: cvimage: A user-specified and opened open-cv image
# Output: file_name: User-specified image file-name
def selectFileToOpen():

    user_selected_image = filedialog.askopenfilename(initialdir="./images", title='FaceDraw: Open File')
    # Opening the image
    path, file_name = os.path.split(user_selected_image)
    cvimage = process_image.openImage(file_name)

    return cvimage, file_name
