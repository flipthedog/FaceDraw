# Creating the g-code

# Imports
import sys
import sysconfig
import time
import process_image
import cv2 as cv
import _datetime
import cv2 as cv

test_image = process_image.openImage('slicer_test_1.png')
cv.imshow('test', test_image)
cv.waitKey(0)
cv.destroyAllWindows()

def readlines(test_image):


# image_to_gcode
# Input: image: the grayscale, line image to be converted into g-code commands
# Input: linewidth: The width of the line to be drawn
# Input: raster: Boolean, whether to raster or not
# Input: filename: the name of the file generated
# Go through the picture pixel by pixel
def image_to_gcode(image, linewidth, raster, filename):

    # Check for file existence and overwrite if necessary
    try:
        # File already exists, overwrite it
        # TODO, overwrite the file
        file = open(str(filename), 'w', 1)

    except FileNotFoundError:
        # File does not exist, create it
        # TODO Create a file
        print(FileNotFoundError.strerror)
        file = open(str(filename), 'w+x')

    writeIntroduction(file)
    writeBody(file, image, linewidth)
    writeConclusion(file)

    # cv.imshow("This image", image)
    # cv.waitKey(0)

    file.close()

# writeIntroduction()
# Write the introduction and settings of the G-code file
# Input: file: The file to write the introduction to
def writeIntroduction(file):
    # TODO Write the settings to the file
    today = str(_datetime.datetime.today())
    file.write("; Created by FaceDraw on: " + str(today))
    file.write("\n")
    file.write("; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
    file.write("\n")
    file.write("; Settings:")

# writeBody()
# Write the body, actual g-code to the file
# Input: file: The file to write the body to
# Input: image: The image to write the G-code from
# Input: linewidth: The width of the pen-drawing
    # Default: 0.3 mm
def writeBody(file, image, linewidth):
    # TODO Write the G-code writing functions

    if linewidth is None:
        linewidth = 0.3

    imageWidth = image.shape[0]
    imageHeight = image.shape[1]
    widthCellNumber = int(imageWidth / linewidth)
    heightCellNumber = int(imageHeight / linewidth)

    print("This is 1,1: " + str(image[1,1]))
    print("This is 100,100: " + str(image[100,100]))
    print("This is 155,155: " + str(image[305,233]))

    for i in range(0, widthCellNumber):

        for j in range(0, heightCellNumber):



            None

# writeConclusion()
# Write the conclusion of the file
# Input: file: the
def writeConclusion(file):
    # TODO write the conclusion of this
    #
    None