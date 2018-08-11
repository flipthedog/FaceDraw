# NewMain.py
# New Main File

# Image Processing
import process_image
import cv2 as cv
from PIL import Image
from PIL import ImageTk

import os
import tkinter
from tkinter import filedialog

class ImageProject:

    # Image Project Constructor
    # Input: cv_image, the image from cv to be displayed
    def __init__(self, cv_image):
        self.shown_image = cv_image

    # returnImage()
    # Input: None
    # Output: tk_image: Return a tkinter compatible image to be displayed
    def returnImage(self, resize, width, height):
        return self.convertImageToTk(self.shown_image, resize, width, height)

    # returnBlankImage()
    # Return a tkinter compatible blank image
    def returnBlankImage(self):

        blank_cv_image = process_image.openImage("blankSquare.py")
        tk_blank_image = self.convertImageToTk(blank_cv_image, True, 300, 300)

        return tk_blank_image

    # convertImageToTk()
    # Purpose: Convert a python-cv image to tkinter image
    # Input: cv_image: a python-cv image to convert
    # Input: resize: Boolean to resize the image
    # Input: width: Width of the image
    # Input: height: height of the image
    # Output: tk_image: A tkinter image
    def convertImageToTk(self, cv_image, resize, width, height):

        # Convert color to RGB
        try:
            cv_image = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
        except Exception:
            None

        pil_image = Image.fromarray(cv_image)

        if resize:
            resized_image = pil_image.resize((width, height), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_image)
        else:
            tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image