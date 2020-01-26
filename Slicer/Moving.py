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
        self.edge_image = process_image.edgeDetection(self.gray_image, True)
        self.inverted_image = process_image.invertImage(self.edge_image, True)

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

        self.draw_arr = {} # Create a dictionary for the image that needs to be drawn
        # Key: tuple: (y , x), where x is the pixel number width, and y is the pixel number height

        self.used = {} # Store whether a particular pixel value has been used or not
        # Key: tuple: (y , x), where x is the pixel number width, and y is the pixel number height

        # Storage: Array: [pixelvalue, used]
        #       pixelvalue: The value of the pixel (typically 0 or 1)
        #       used: Boolean value representing whether it has been used or not

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

        # Initialize the dict to 0
        for x in range(self.width_number):

            for y in range(self.height_number):

                self.draw_arr[(y, x)] = 0

        print(self.draw_arr)

        self.white_pixels = cv.findNonZero(self.edge_image)

        for pixel in self.white_pixels:
            actual_pixel = pixel[0]

            width_pos = actual_pixel[0]
            height_pos = actual_pixel[1]

            cell_pixel_width = math.floor((width_pos / self.image_width) * self.width_number)
            cell_pixel_height = math.floor((height_pos / self.image_height) * self.height_number)

            # Toggle a specific square in the drawing array
            self.draw_arr[(cell_pixel_height, cell_pixel_width)] += 1

        # Find the compressed white pixels to draw
        self.white_pixels = self.find_white_pixels(self.draw_arr)

        current_averageX = 0  # Store the x position of the moving average
        current_averageY = 0  # Store the y position of the moving average
        total_average_number = 0  # The total number of pixels in the moving average

        commands = []  # Array of move & draw commands

        while len(self.white_pixels) > 1:

            # Pop one pixel, choose it  as the origin from which to draw a moving average
            # line

            pixel = self.white_pixels.pop(0)

            pixel_width_pos = pixel[0]
            pixel_height_pos = pixel[1]

            total_X = pixel_width_pos
            total_Y = pixel_height_pos
            current_averageX = pixel_width_pos
            current_averageY = pixel_height_pos
            total_average_number += 1

            commands.append([-1, -1])  # Insert move command

            # Keep looping until we reach a stopping condition
            stop_flag = False

            while ~stop_flag:

                print("Current dict length:", self.get_length_dict())

                near_pixels = self.get_all_nearby([current_averageY, current_averageX], distance_threshold)

                if len(near_pixels) > 0:
                    # There is at least one pixel nearby

                    first_near_x = near_pixels[0][1]
                    first_near_y = near_pixels[0][0]

                    # Pop the near pixel from the draw_arr
                    self.draw_arr[(first_near_y, first_near_x)] = 0

                else:
                    continue  # Break the loop, there are no pixels nearby

                total_average_number += 1

                total_X += first_near_x
                total_Y += first_near_y

                current_averageX = total_X / total_average_number
                current_averageY = total_Y / total_average_number

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
        Return all pixels nearby other pixels
        :param threshold: The maximum distance to check around the pixel
        :param pixel: [height, width] a pixel on the image
        :return: [pixel1, pixel2, pixel3] An array of black pixels nearby the given pixels
        """

        home_x = pixel[1]
        home_y = pixel[0]

        distance_dir = threshold / 2

        # Form the minimum barrier
        min_x = int(home_x - distance_dir)
        min_y = int(home_y - distance_dir)

        if min_x < 0:
            min_x = 0
        if min_y < 0:
            min_y = 0

        # Form the maximum barrier
        max_x = int(home_x + distance_dir)
        max_y = int(home_y + distance_dir)

        if max_x > self.width_number:
            max_x = self.width_number - 1
        if max_y > self.height_number:
            max_y = self.height_number - 1

        # The array of pixels that will be returned
        return_arr = []

        for y in range(min_y, max_y):

            for x in range(min_x, max_x):

                if self.draw_arr[(y, x)] > 0:
                    # There is a pixel in this location, so add it!

                    return_arr.append([y, x])

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

        draw_pixels = []

        for i in range(0, self.width_number):

            for j in range(0, self.height_number):

                if draw_dict[(j, i)] > 0:
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

    #TODO: Figure out how to keep track of which pixels have been popped and which can still be used with respect to dictionary