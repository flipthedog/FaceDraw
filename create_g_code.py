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

    if not len(new_coordinates[0]) > 0:
        # There are no more pixels to process, image contains no pixels
        return False
    else:
        # There are still pixels to process, image still contains pixels
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

    # print("Pixel: " + str(pixel_1[0]) + " , " + str(pixel_1[1]))
    return math.sqrt((pixel_1[0] - pixel_2[0])**2 + (pixel_1[1] - pixel_2[1])**2)

# distancePointLine()
# Return the distance between a point and a line
# Input: A point
# Input: Line: An array representing the factors of the line equation
def distancePointLine(point, line):

    x = point[0]
    y = point[1]

    slope = line[0]
    y_int = line[1]

    inv_slope = (-1)*(1/slope)

    # Convert from y = mx+b


    a = -slope
    b = 1
    c = -y_int

    distance = ((abs(a * x + b * y + c))/ math.sqrt(a**2 + b**2))

    return distance

# findNear()
# Find nearby black pixels to take
# Input: Image to check for nearby pixels
# x, y coordinate of the pixel
def findNear(check_image, x, y, fit):

    # The image to return
    return_image = np.copy(check_image)

    shape = check_image.shape
    width = shape[1]
    height = shape[0]

    # The original pixel of the line
    home_pixel = [x, y]

    #cv.imshow('lol', check_image)
    #cv.imshow('inverted', cv.bitwise_not(check_image))

    #cv.waitKey(0)
    #cv.destroyAllWindows()

    # Find all the white pixels in the image
    white_pixels = cv.findNonZero(check_image)

    results = []
    points = []

    # Done TODO Loop through and find all points that are not in a line yet
    # TODO Create a loop to form a line
    # TODO Form a trend out of all the points currently in the line
    # TODO Create a function that decides whether the point is within the trend
    # TODO If the point is in the trend, remove the point from the image and add it to the line
    # TODO Then add the line to the rest of the lines
    # print("This is len white: " + str(len(white_pixels)))


    # Put all white points in an array along with their distance to home point

    i = 0

    for i in range(0, len(white_pixels)):

        # print("Taking off: " + str(white_pixels[i][0]))
        distance = distanceBetween(white_pixels[i][0], home_pixel)
        #print(distance)

        points.append((distance, white_pixels[i][0]))

        i = i + 1

    # Sort the list with respect to distance to home pixel
    sorted_points = sorted(points, key=lambda point1: point1[0])

    # print("Home Point: ")
    # print(home_pixel)
    # for point in sorted_points:
    #     print("This is distance: " + str(point[0]) + ", Point: " + str(point[1][0]) + ", " + str(point[1][1]))
    #

    # Swap the list to allow pop()
    sorted_points.reverse()

    # print("This is the sorted_point length: " + str(len(sorted_points)) )

    # Pull the first point off the array, and start forming a line
    point_1 = sorted_points.pop()

    x = [home_pixel[0], point_1[1][0]] # List of all the x's of the points
    y = [home_pixel[0], point_1[1][1]] # List of all the y's of the points

    # Create the first polynomial
    first_poly = np.polyfit(x, y, 1)

    # print(first_poly)
    # print("This is the sorted_point length: " + str(len(sorted_points)) )

    line = [] # List of points representing the line

    line.append(home_pixel)
    line.append(point_1)

    looping = True
    looped = 0

    while looping and sorted_points:

        # Keep pulling points off the sorted list until points no longer match
        popped_point = sorted_points.pop()[1]

        distance_to_line = distancePointLine(popped_point,first_poly)

        print("This is the calculated distance: " + str(distance_to_line))

        if distance_to_line <= fit and popped_point[1] < width and popped_point[0] < height:

            return_image[popped_point[1], popped_point[0]] = 0

            # Make the pixel white and add it to the line
            line.append(popped_point)
            x.append(popped_point[0])
            y.append(popped_point[1])
            first_poly = np.polyfit(x, y, 1)

    print(str(len(line)))
    cv.imshow('original', check_image)
    cv.imshow('modified', return_image)

    cv.waitKey(0)
    cv.destroyAllWindows()
    exit()
    return return_image, line

# readLines()
# Find the lines in the image and pass them back as an array,
# Input: test_image: A GRAYSCALE image representing the image to be drawn
# Output: An array of lines to pass through the slicer function
def readlines(test_image):

    # Convert image to grayscale just to be sure
    worked_image = cv.cvtColor(test_image, cv.COLOR_BGR2GRAY)

    print(worked_image.shape)
    # Image specs
    shape = worked_image.shape
    width = shape[1]
    height = shape[0]

    i = 0
    j = 0

    while i in range(0, width - 1):

        i = i + 1
        j = 0


        while j in range(0, height - 1):
            j = j + 1

            print("This is i,j " + str(i) + ", " + str(j))
            pixel = worked_image[i, j]

            if pixel == 0:

                print("Got one")

                lol = findNear(cv.bitwise_not(worked_image), i, j, 3)

                # This means we have a black pixel
                # Search for nearby black pixels
            else:
                # This means we have a white pixel, so do nothing
                None




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


