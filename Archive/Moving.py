# Moving.py
# Purpose: Slice the loaded image into G-code commands

# Import
import math
from ImageProcessing import process_image
import numpy as np
import _datetime
import cv2 as cv


class Moving:

    def __init__(self, image, bed_size, line_width = 1.0, lock_ratio = True):
        """
        Initialize the object
        :param image: [opencv image] The image to process and slice
        :param bed_size: [mm] [n x m] The size of the bed height (n) by width (m)
        :param line_width: [mm] The line width of the image (dots per mm)
        :param lock_ratio: [boolean] Crop the bed size to meet the image ratio
        """

        # The image to be processed
        self.original_image = image
        self.gray_image = process_image.grayImage(self.original_image, True)
        self.binary_image = process_image.thresholdImage(self.gray_image, "regular", show=True)
        #self.edge_image = process_image.edgeDetection(self.gray_image, True)
        #self.contours_image = process_image.contourImage(self.edge_image, True)
        #self.inverted_image = process_image.invertImage(self.edge_image, True)

        cv.waitKey(0)

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

        # If lock_ratio is on, the program will maintain the ratio of the image
        # by reducing the bed- to maintain the height-width ratio of the image
        # Without this, your image will look squashed depending on camera orientation
        if lock_ratio:
            self.find_compression()

        self.width_number = math.floor(self.max_bed_width / self.line_width) # Number of possible pixels in drawing width
        self.height_number = math.floor(self.max_bed_height / self.line_width) # Number of possible pixels in drawing height

        self.white_pixels = []

        self.draw_arr = {} # Create a dictionary for the image that needs to be drawn
        # Key: tuple: (y , x), where x is the pixel number width, and y is the pixel number height

        self.used = {} # Store whether a particular pixel value has been used or not
        # Key: tuple: (y , x), where x is the pixel number width, and y is the pixel number height

        print("This is the width and height of the resultant image: ", self.width_number, self.height_number)

    def find_compression(self):
        # Can only reduce, because we don't want to increase beyond the maximum bed size
        bed_ratio = self.max_bed_height / self.max_bed_width
        image_ratio = self.image_height / self.image_width

        if bed_ratio < image_ratio:
            # This means that the width of the bed will have to decrease
            self.max_bed_width = math.floor((image_ratio / bed_ratio) * self.max_bed_width)
        else:
            # This means that the height of the bed will have to decrease
            self.max_bed_height = math.floor((image_ratio / bed_ratio) * self.max_bed_height)

    def slice(self, distance_threshold=5):
        """
        Create a list of points to process into G-code commands
        :param distance_threshold: The distance between two cells
        :return:
        """

        # Purpose:
        # Create a path out of moving average lines

        # How:
        # 1. Pop a white pixel
        # 2. Find the nearest neighbor pixel
        #    a. Check if it fits within the moving average and distance threshold
        #    b. Pop it, if it does
        #    c. Add its location to the moving average


    def get_length_dict(self):
        """
        Used for debugging to find out the length of the drawing dictionary
        """

        copy_dict =  {}
        copy_dict = self.draw_arr

        length = 0

        for i in range(0, self.width_number):

            for j in range(0, self.height_number):

                if copy_dict[(j, i)] > 0:
                    length += 1

        return length

    def get_all_nearby(self, pixel, threshold):
        """
        Return all pixels nearby given input pixel
        :param threshold: The maximum distance to check around the pixel
        :param pixel: [height, width] a pixel on the image
        :return: [pixel1, pixel2, pixel3] An array of black pixels nearby the given pixels
        """

        return return_arr

    def find_white_pixels(self, draw_dict):
        """
        Go through the array to find all the pixels that need to be drawn, return those in a new array
        :param draw_dict: A dictionary to check for pixels
        :return: [[x, y], ...] Array of points that need to be drawn
        """

        # How this works:
        #   1. Go through the draw array to find all spots that need to be drawn
        #   2. Use max bed size to calculate spot to draw on the bed

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

    # TODO: Figure out how to keep track of which pixels have been popped and which can still be used with respect to dictionary
