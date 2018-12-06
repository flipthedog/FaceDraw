# Slicer.py
# Purpose: Slice the image to G-code commands

# Import
import math
from ImageProcessing import process_image
import numpy as np
import _datetime
import cv2 as cv

# Slicer Class
class Slicer:

    def __init__(self, image, feedrate, bed_size, z_hop=None, z_tune=None):
        # The image to be processed
        self.original_image = image

        # Bed specifications
        self.max_width = bed_size[0]
        self.max_height = bed_size[1]

        # Image specifications
        shape = image.shape
        self.image_width = shape[1] # Horizontal pixel no.
        self.image_height = shape[0] # Vertical pixel no.

        # User specified settings
        # Vertical distance (mm) to z-hop
        if z_hop == None:
            self.z_hop = 0.3
        else:
            self.z_hop = z_hop

        # Vertical adjustment (mm)
        if z_tune == None:
            self.z_tune = 0
        else:
            self.z_tune = z_tune

        self.feedrate = feedrate

    # containsPixels()
    # Look through the image to see if there are still lines to be found
    # Input: check_image: A black and white image to check
    # Output: Boolean value representing whether the image still contains pixels
    def containsPixels(self, check_image):

        zeros = np.zeros((self.width, self.height), dtype=np.uint8)
        ones = np.ones((self.width, self.height), dtype=np.uint8)
        ones = ones * 255

        indices = np.where(check_image == [255])
        coordinates = [indices[0], indices[1]]

        new_coordinates = np.asarray(coordinates, dtype=np.uint8)

        if not len(new_coordinates[0]) > 0:
            # There are no more pixels to process, image contains no pixels
            return False
        else:
            # There are still pixels to process, image still contains pixels
            return True

    # distanceBetween()
    # Find the distance between two pixels
    # Input: pixel_1[width, height]
    # Input: pixel_2[width, height]
    # Output: Number representing the distance
    def distanceBetween(self, pixel_1, pixel_2, printout=False):

        if printout:
            # Print out the two pixels
            print("Pixel: " + str(pixel_1[0]) + " , " + str(pixel_1[1]))

        return math.sqrt((pixel_1[0] - pixel_2[0]) ** 2 + (pixel_1[1] - pixel_2[1]) ** 2)

    # distancePointLine()
    # Return the distance between a point and a line
    # Input: A point
    # Input: Line: An array representing the factors of the line equation
    def distancePointLine(self, point, line):

        x = point[0]
        y = point[1]

        slope = line[0]
        y_int = line[1]

        if not (slope == 0):
            inv_slope = (-1) * (1 / slope)
        else:
            inv_slope = 0

        # Convert from y = mx+b

        a = - slope
        b = 1
        c = - y_int

        distance = ((abs(a * x + b * y + c)) / math.sqrt(a ** 2 + b ** 2))

        return distance

    # distanceclosestpoint()
    # Find the closest point to the line of best fit
    # Input: line_points: An array of points in the line of best fit
    # Input: point: The point to be checked
    # Output: boolean: Whether the point is close enough to the line of best fit
    def distanceclosestpoint(self, line_points, point, fit):

        # The minimum distance to the point
        min_distance = 9999999

        # Iterate through the line to find the shortest distance to the point
        for fit_point in line_points:

            distance = self.distanceBetween(fit_point, point)

            if distance <= min_distance:
                min_distance = distance

        if distance <= fit:

            # The distance is close, point is valid, return True
            return True

        # The distance is too far, point is not valid, return False
        return False

    # findNear()
    # Find nearby black pixels to take
    # Input: Image to check for nearby pixels
    # x, y coordinate of the pixel
    def findNear(self, check_image, x, y, fit):

        # The image to return
        return_image = np.copy(check_image)

        # The original pixel passed into the function
        home_pixel = [x, y]

        # Find all the white pixels in the image
        white_pixels = cv.findNonZero(check_image)

        # An array of tuples containing (distance to home pixel, point[x,y])
        points = []

        # Done TODO Loop through and find all points that are not in a line yet
        # TODO Create a loop to form a line
        # TODO Form a trend out of all the points currently in the line
        # TODO Create a function that decides whether the point is within the trend
        # TODO If the point is in the trend, remove the point from the image and add it to the line
        # TODO Then add the line to the rest of the lines

        # Put all white points in an array along with their distance to home point
        for pixel in white_pixels:
            distance = self.distanceBetween(pixel[0], home_pixel)
            points.append((distance, pixel[0]))

        # Sort the list with respect to distance to home pixel
        sorted_points = sorted(points, key=lambda point1: point1[0])

        # To print all the points in an array
        # for point in sorted_points:
        #     print("This is distance: " + str(point[0]) + ", Point: " + str(point[1][0]) + ", " + str(point[1][1]))

        # Swap the list to allow pop()
        sorted_points.reverse()

        # Pull the first point off the array, and start forming a line
        point_1 = sorted_points.pop()[1]

        # Start arrays of x's and y's
        x = [home_pixel[0], point_1[0]]  # List of all the x's of the points
        y = [home_pixel[1], point_1[1]]  # List of all the y's of the points

        # Create the first polynomial
        first_poly = np.polyfit(x, y, 1)

        line = []  # List of points representing the line

        # Add the first two points
        line.append(home_pixel)
        line.append(point_1)

        looping = True

        while looping and sorted_points:

            # Keep pulling points off the sorted list until points no longer match
            popped_point = sorted_points.pop()[1]

            distance_to_line = self.distancePointLine(popped_point, first_poly)

            # print("This is the calculated distance: " + str(distance_to_line))

            fit = 5
            fit2 = 100

            close_enough = self.distanceclosestpoint(line, popped_point, fit2)

            if distance_to_line <= fit and close_enough:

                return_image[popped_point[1], popped_point[0]] = 100

                # Make the pixel white and add it to the line
                line.append(popped_point)
                x.append(popped_point[0])
                y.append(popped_point[1])
                first_poly = np.polyfit(x, y, 1)

        print(str(len(line)))
        cv.imshow('original', check_image)
        cv.imshow('modified', return_image)
        cv.waitKey(0)

        return line, return_image

    # readLines()
    # Find the lines in the image and pass them back as an array,
    # Input: test_image: A GRAYSCALE image representing the image to be drawn
    # Output: An array of lines to pass through the slicer function
    def readlines(self, test_image=None):

        if test_image == None:
            test_image = self.original_image

        # Convert image to grayscale just to be sure
        worked_image = cv.cvtColor(test_image, cv.COLOR_BGR2GRAY)

        # Print the shape of the image
        print(worked_image.shape)

        # Image specs
        shape = worked_image.shape
        height = shape[0]  # The number of horizontal pixels
        width = shape[1]  # The number of vertical pixels

        print("This is the width, height: " + str(width) + ", " + str(height))

        # Invert the image to make the lines white pixels
        inv_image = cv.bitwise_not(worked_image)

        arrayLines = []

        i = 0

        # Iterate through the entire image to find all the white pixels
        while i in range(0, width):

            i = i + 1
            j = 0

            while j in range(0, height):

                j = j + 1

                pixel = inv_image[i, j]

                # Pixel is white
                if pixel == 255:
                    # This means we have a black pixel
                    # Search for nearby black pixels

                    # Analyze the lines around the pixel
                    # i represents the width (x)
                    # j represents the height (y)
                    lines, inv_image = self.findNear(inv_image, i, j, 3)

                    # Add the line to the rest of the lines
                    arrayLines.append(lines)

        return arrayLines

    # image_to_gcode
    # Input: image: the grayscale, line image to be converted into g-code commands
    # Input: linewidth: The width of the line to be drawn
    # Input: raster: Boolean, whether to raster or not
    # Input: filename: the name of the file generated
    # Go through the picture pixel by pixel
    def image_to_gcode(self, filename, image=None, linewidth=None, raster=None):

        # Check for file existence and overwrite if necessary
        try:
            # File already exists, overwrite it
            # TODO, overwrite the file
            filename = "./GCode/" + filename
            file = open(str(filename), 'w', 1)

        except FileNotFoundError:
            # File does not exist, create it
            # TODO Create a file
            print(FileNotFoundError.strerror)
            file = open(str(filename), 'w+x')

        self.writeIntroduction(file)
        self.linetogcode(file)
        # writeBody(file, image, linewidth)
        self.writeConclusion(file)

        # cv.imshow("This image", image)
        # cv.waitKey(0)

        file.close()

    # writeIntroduction()
    # Write the introduction and settings of the G-code file
    # Input: file: The file to write the introduction to
    def writeIntroduction(self, file):
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
    def writeBody(self, file, image, linewidth):
        # TODO Write the G-code writing functions

        if linewidth is None:
            linewidth = 0.3

        imageWidth = image.shape[0]
        imageHeight = image.shape[1]
        widthCellNumber = int(imageWidth / linewidth)
        heightCellNumber = int(imageHeight / linewidth)

        print("This is 1,1: " + str(image[1, 1]))
        print("This is 100,100: " + str(image[100, 100]))
        print("This is 155,155: " + str(image[305, 233]))

        for i in range(0, widthCellNumber):

            for j in range(0, heightCellNumber):
                None

    # writeConclusion()
    # Write the conclusion of the file
    # Input: file: the
    def writeConclusion(self, file):
        # TODO write the conclusion of this

        file.write("\n; That is all for now")
        file.write("\n; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
        file.write("\n")
        file.write("; Thanks")

        None

    # linetogcode()
    # Convert an array of points to G-code moves
    # Input: file: The file to write the text to
    # Input: max_width: The maximum width to move in
    # Input: max_height: The maximum height to move in
    # Input: z_hop: The height to hop in between draw moves
    # Input: lines: An array of lines to be drawn
    # Output: None
    def linetogcode(self, file, lines):
        # Assumptions: All the points are in order representing a path

        # Convert to bed coordinates
        width_ratio = self.max_width / self.image_width
        height_ratio = self.max_height / self.image_height

        # Iterate through all the lines to draw
        for line in lines:

            # Move to the new position, set feedrate
            first_point = line[0]

            g_code_x = first_point[0] * width_ratio
            g_code_y = first_point[1] * height_ratio
            g_code_z = self.z_tune

            file.write("G1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(g_code_z)+ " F" + str(self.feedrate))

            # Put down the head
            file.write("G1 " + "Z" + str(self.z_tune) + " ; Move down the toolhead")

            # Iterate through all the points in the line
            for point in line:

                # Point = (height, width)
                x = point[0]
                y = point[1]

                # The G-code position
                g_code_x = x * width_ratio
                g_code_y = y * height_ratio
                g_code_z = self.z_tune

                file.write("G1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(g_code_z))

            g_code_z = self.z_tune + self.z_hop

            file.write("G1 " + "Z" + str(g_code_z) + " ; Move up the toolhead")

        file.write("; Done drawing lines")