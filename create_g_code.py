# Creating the g-code

# Imports
import sys
import sysconfig
import time
import math

# Image processing imports
import process_image
import numpy as np
from numpy import sum
import _datetime
import cv2 as cv



# containsPixels()
# Look through the image to see if there are still lines to be found
# Input: check_image: A black and white image to check
# Output: Boolean value representing whether the image still contains pixels
def containsPixels(check_image):
    shape = check_image.shape
    width = shape[0]
    height = shape[1]
    # print("X: " + str(width) + " Y: " + str(height))

    zeros = np.zeros((width,height), dtype=np.uint8)
    ones = np.ones((width,height), dtype=np.uint8)
    ones = ones * 255

    indices = np.where( check_image == [255])
    coordinates = [indices[0],indices[1]]

    new_coordinates = np.asarray(coordinates,dtype=np.uint8)

    print(len(new_coordinates[0]))
    if not len(new_coordinates[0]) > 0:
        return False
    else:
        return True

    # For testing and printing all pixels in the image
    # i = 0
    # j = 0
    #
    # while i in range(0, width - 1):
    #     j = 0
    #     i = i + 1
    #     while j in range(0, height - 1):
    #         j = j + 1
    #         print(str(check_image.item(i, j, 2)))

# distanceBetween()
# Find the distance between two pixels
def distanceBetween(pixel_1, pixel_2):

    return math.sqrt((pixel_1[0] - pixel_2[0])^2 + (pixel_1[1] - pixel_2[1])^2)


# findNear()
# Find nearby black pixels to take
# Input: Image to check for nearby pixels
# x, y coordinate of the pixel

def findNear(check_image, x, y):

    home_pixel = [x, y]

    white_pixels = cv.findNonZero(cv.bitwise_not(check_image))

    results = []
    points = []
    distance = []

    for i in range(0, len(white_pixels)):

        distance = distanceBetween(white_pixels[i], home_pixel)
        print(distance)

        points.append(white_pixels[i])
        distance.append(distance)

# readLines()
# Find the lines in the image and pass them back as an array
# Input: test_image: A black and white image representing the image to be drawn
# Output: An array of lines to pass through the slicer function
def readlines(test_image):
    worked_image = test_image

    shape = test_image.shape
    width = shape[0]
    height = shape[1]

    i = 0
    j = 0

    while i in range(0, width - 1):
        j = 0
        i += 1
        while j in range(0, height - 1):


            pixel = worked_image[i, j]

            print(pixel)

            if pixel is 0:
                print("Got one")

                worked_image = findNear(worked_image, pixel)

                # This means we have a black pixel
                # Search for nearby black pixels
            else:
                # This means we have a white pixel, so do nothing
                None


            j += 1

    # An array
    lines = []

    return containsPixels(worked_image)


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


test_image = process_image.openImage('slicer_test_1.png')
black_image = np.zeros((test_image.shape[0],test_image.shape[1]), dtype=np.uint8)
blank_image = np.ones((test_image.shape[0],test_image.shape[1]), dtype=np.uint8) * 255


run_image = test_image

print(str(readlines(run_image)))

cv.imshow('original', run_image)
# cv.imshow('final', final_image)
cv.waitKey(0)
cv.destroyAllWindows()


