# Scan.py
# Purpose: Slice the loaded image into G-code commands

# Import
import math
from ImageProcessing import process_image
import cv2 as cv


class Scan:

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
        # Create a path out of scanning lines from top to bottom, left to right

        # How:
        # 1. Take in a binarized image
        # 2. Convert it into cells
        # 3. Color the cells black or white
        # 4. Draw all black pixels in a row

        # Cell density
        number_cells_width = math.floor(self.max_bed_width / self.line_width) # Number of cells / side
        number_cells_height = math.floor(self.max_bed_height / self.line_width) # Number of cells / side

       # Define a two dimensional array on where to draw, initialize to 0
        draw_arr = [[0 for x in range(number_cells_width)] for y in range(number_cells_height)]

        # Image processing
        white_pixels = cv.findNonZero(self.edge_image) # Find all the pixels to draw

        for pixel2 in white_pixels:
            pixel = pixel2[0]

            # Transform from image space to draw_Arr space
            # findNonZero flips image X and Y
            pixel_width_pos = pixel[0]
            pixel_height_pos = pixel[1]

            cell_pixel_width = math.floor((pixel_width_pos / self.image_width) * number_cells_width)
            cell_pixel_height = math.floor((pixel_height_pos / self.image_height) * number_cells_height)

            # Change draw arr pixel
            draw_arr[cell_pixel_height -1 ][cell_pixel_width - 1] += 1

        # Form array of lines to return
        points = []
        # Array of points [x, y]

        # Move from one point in draw_arr to the next
        for i in range(0, number_cells_width):

            for j in range(0, number_cells_height):

                # Determine whether to draw here, otherwise add point to lines after converting
                if draw_arr[j][i] > 0:

                    # Calculate the pixel coordinates to draw a point
                    pixel_width_pos = math.floor((i / number_cells_width) * self.max_bed_width)
                    pixel_height_pos = math.floor((j / number_cells_height) * self.max_bed_height)

                    # Now change to X-first, then Y [x, y]
                    points.append([pixel_width_pos, pixel_height_pos])

        return points

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

        return None

    def find_white_pixels(self, draw_dict):
        """
        Go through the array to find all the pixels that need to be drawn, return those in a new array
        :param draw_dict: A dictionary to check for pixels
        :return: [[x, y], ...] Array of points that need to be drawn
        """

        # How this works:
        #   1. Go through the draw array to find all spots that need to be drawn
        #   2. Use max bed size to calculate spot to draw on the bed

        return None

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
