# Lines.py
# Purpose: Slice the image to points to draw, will be converted into G-code
# later. This is a revision of a previous iteration of lines.py to make it more
# efficient.
# The resultant object is to be used by any of the slicer algorithms to create
# a series of moves to be interpreted by the G-code writer.

# The purpose of this is to take a pixel and then do a BFS of nearby neighbors

# Import
import math
from ImageProcessing import process_image
import numpy as np
import _datetime
import cv2 as cv
from Slicer.Pixel import Pixel


class FaceDrawImage:

    def __init__(self, image, bed_size, line_width=1.0, lock_ratio=True):
        """
        Constructor, create a Raster object to slice an image. Raster uses
            individual points as opposed to lines
        :param image: [opencv image] The image to process and slice
        :param bed_size: [mm] [n x m] The size of the bed height (n) by width
                (m)
        :param line_width: [mm] The line width of the image (dots per mm)
        :param lock_ratio: [boolean] Crop the bed size to meet the image ratio
        """

        # The image to be processed
        self.original_image = image
        self.gray_image = process_image.grayImage(self.original_image, True)
        self.edge_image = process_image.edgeDetection(self.gray_image, True)
        self.inverted_image = process_image.invertImage(self.edge_image, True)

        # Show the images to the user
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

        self.white_pixels = cv.findNonZero(self.edge_image)

        blank_image = np.zeros((self.height_number, self.width_number), np.uint8)

        for pixel in self.white_pixels:
            actual_pixel = pixel[0]

            width_pos = actual_pixel[0]
            height_pos = actual_pixel[1]

            cell_pixel_width = math.floor((width_pos / self.image_width) \
            * self.width_number)
            cell_pixel_height = math.floor((height_pos / self.image_height) \
            * self.height_number)

            # Toggle a specific square in the drawing array
            blank_image[cell_pixel_height - 1, cell_pixel_width - 1] = 255

        #img = process_image.morphTrans(blank_image, "erode", 2, 1)
        self.final_image = process_image.edgeDetection(blank_image)

        cv.imshow("eroded", blank_image)
        cv.imshow("final image", self.final_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

        self.connected_image = self.create_grid()

    def create_grid(self):
        """
        Create a grid from an input image, return as a 2D array of pixels who
        all contain their neighbors
        """

        image_width = self.width_number
        image_height = self.height_number

        # Create an empty 2D array
        connected_temp = [[0 for x in range(image_width)] for y in \
                range(image_height)]

        # Create a bunch of empty pixels objects
        for i in range(image_width):

            for j in range(image_height):

                    connected_temp[j][i] = Pixel(j, i, self.final_image[j, i])

        # Connect all the pixel objects
        for i in range(image_width):

            for j in range(image_height):

                    current_pixel = connected_temp[j][i]

                    width_number = current_pixel.width
                    height_number = current_pixel.height
                    max_width = self.width_number
                    max_height = self.height_number

                    neighbors = []

                    if width_number - 1 > 0 and height_number - 1 > 0 :
                        # top-left

                        neighbors.append(connected_temp[height_number - 1][width_number - 1])

                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if height_number - 1:
                        # top

                        neighbors.append(connected_temp[height_number - 1][width_number])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if width_number + 1 < max_width and height_number - 1 < 0:
                        # top-right
                        neighbors.append(connected_temp[height_number - 1][width_number + 1])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if width_number - 1 > 0:
                        # left
                        neighbors.append(connected_temp[height_number][width_number - 1])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if width_number + 1 < max_width:
                        # right
                        neighbors.append(connected_temp[height_number][width_number + 1])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if height_number + 1 < max_height and width_number - 1 > 0:
                        # bottom-left
                        neighbors.append(connected_temp[height_number + 1][width_number - 1])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if height_number + 1 > max_height:
                        # bottom
                        neighbors.append(connected_temp[height_number + 1][width_number])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    if height_number + 1 < max_height and width_number + 1 < max_width:
                        # bottom right
                        neighbors.append(connected_temp[height_number + 1][width_number + 1])
                    else:
                        neighbors.append(Pixel(-1, -1, -1, True))

                    connected_temp[j][i].neighbors = neighbors

        return connected_temp

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
