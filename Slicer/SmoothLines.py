# SmoothLines.py
# Purpose: Slice the image to G-code commands

# Import
import math
from ImageProcessing import process_image
import numpy as np
import _datetime
import cv2 as cv

class Slicer:

    def __init__(self, image, bed_size, line_width = 1.0, lock_ratio = True):
        """
        Constructor, create a Slicer object to slice an image.
        :param image: [opencv image] The image to process and slice
        :param bed_size: [mm] [n x m] The size of the bed height (n) by width (m)
        :param line_width: [mm] The line width of the image (dots per mm)
        :param lock_ratio: [boolean] Crop the bed size to meet the image ratio
        """

        # The image to be processed
        self.original_image = image
        self.gray_image = process_image.grayImage(self.original_image, True)
        self.edge_image = process_image.edgeDetection(self.gray_image, True)
        self.inverted_image = process_image.invertImage(self.edge_image, True)

        cv.waitKey(0)
        cv.destroyAllWindows()

        # The resolution of the image
        self.line_width = line_width
        # Increasing the line width will result in a lower resolution
        # Decreasing the line width will result in a higher resolution
        # This might change depending on your marker size or XY accuracy

        # Bed specifications
        self.max_bed_height = bed_size[0]
        self.max_bed_width = bed_size[1]

        # Image specifications
        shape = image.shape
        self.image_height = shape[0]  # Vertical pixel number
        self.image_width = shape[1]  # Horizontal pixel number

        # If lock_ratio is on, the program will maintain the ratio of the image by reducing the bed-size
        # to maintain the height-width ratio of the image
        if lock_ratio:
            self.find_compression()

        self.width_number = math.floor(self.max_bed_width / self.line_width) # Number of possible pixels in drawing width
        self.height_number = math.floor(self.max_bed_height / self.line_width) # Number of possible pixels in drawing height

        self.white_pixels = []

    def find_compression(self):
        """
        Find a working compression based on the image ratio
        :return: None, object image modified
        """
        # Can only reduce, because we don't want to increase beyond the maximum bed size
        bed_ratio = self.max_bed_height / self.max_bed_width
        image_ratio = self.image_height / self.image_width

        if bed_ratio < image_ratio:
            # This means that the width of the bed will have to decrease
            self.max_bed_width = math.floor((image_ratio / bed_ratio) * self.max_bed_width)
        else:
            # This means that the height of the bed will have to decrease
            self.max_bed_height = math.floor((image_ratio / bed_ratio) * self.max_bed_height)

    def slice(self, distance_threshold):
        """
        Create a list of points representing G-code moves based on object loaded image
        :param: distance_threshold : Int : The maximum distance between pixels
        :return: [[x1, y1] ...] An array of x-y points
        """

        # IDEA:
        # 1. Take a pixel that needs to be drawn
        # 2. See if it has any neighbors
        # 3. Take the neighbor and add it to the line

    def find_white_pixels(self, array):
        """
        Go through the array to find all the pixels that need to be drawn, return those in a new array
        :param array: The array to check for pixels
        :return: [[x, y], ...] Array of points that need to be drawn
        """
        # How this works:
        #   1. Go through the draw array to find all spots that need to be drawn
        #   2. Use max bed size to calculate spot to draw on the bed

        draw_pixels = []
        for i in range(0, self.width_number):

            for j in range(0, self.height_number):

                if array[j][i] > 0:
                    x_position = i * (self.max_bed_width / self.width_number)
                    y_position = j * (self.max_bed_height / self.height_number)

                    draw_pixels.append([x_position, y_position])

        return draw_pixels

    @staticmethod
    def distance_between(pixel_1, pixel_2, printout=False):
        """
        Find the distance between two pixels
        :param pixel_1: [height, width] The first pixel
        :param pixel_2: [height, width] The second pixel
        :param printout: [boolean] Output distance
        :return: The distance between the two pixels
        """
        if printout:
            # Print out the two pixels
            print("Pixel: " + str(pixel_1[0]) + " , " + str(pixel_1[1]))
        return math.sqrt((pixel_1[0] - pixel_2[0]) ** 2 + (pixel_1[1] - pixel_2[1]) ** 2)