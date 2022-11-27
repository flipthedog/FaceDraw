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

from matplotlib import pyplot as plt


class FaceDrawImage:

    def __init__(self, image, bed_size, line_width=1.0, lock_ratio=True, show=False):
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

        # image = cv.flip(image, 0)
        self.original_image = image
        self.gray_image = process_image.grayImage(self.original_image, show)
        self.edge_image = process_image.edgeDetection(self.gray_image, show)
        self.inverted_image = process_image.invertImage(self.edge_image, show)

        # Show the images to the user
        # cv.waitKey(0)
        # cv.destroyAllWindows()

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
        # by reducing the bed-size to maintain the height-width ratio of the
        # image

        # print("Bed size: Height:", self.max_bed_height, "Width: ", self.max_bed_width)

        if lock_ratio:
            self = self.find_compression()

        # print("Bed size: Height:", self.max_bed_height, "Width: ", self.max_bed_width)

        self.width_number = math.floor(self.max_bed_width / self.line_width)

        self.height_number = math.floor(self.max_bed_height / self.line_width)

        self.white_pixels = cv.findNonZero(self.edge_image)

        blank_image = np.zeros(
            (self.height_number, self.width_number), np.uint8)

        for pixel in self.white_pixels:
            actual_pixel = pixel[0]

            width_pos = actual_pixel[0]
            height_pos = actual_pixel[1]

            cell_pixel_width = math.floor((width_pos / self.image_width)
                                          * self.width_number)
            cell_pixel_height = math.floor((height_pos / self.image_height)
                                           * self.height_number)

            # Toggle a specific square in the drawing array
            blank_image[cell_pixel_height - 1, cell_pixel_width - 1] = 255

        # print(blank_image)

        # plt.imshow(blank_image)
        # plt.show(block=True)
        # cv.imshow(blank_image)
        # cv.waitKey(0)
        #
        #img = process_image.morphTrans(blank_image, "erode", 2, 1)
        self.final_image = process_image.edgeDetection(blank_image)

        self.connected_image = self.create_grid()

        print("Created connected grid image")
        print("Size: w", self.width_number, ", h", self.height_number)
        print("Original Image size: ", shape)
        print("Bed Size: ", self.max_bed_width, ",", self.max_bed_height)

    def __str__(self):

        for i in range(0, self.width_number - 1):

            print('| - ' * (self.height_number - 1), '|', sep='')

            for j in range(0, self.height_number - 1):

                print("|",'{000:3.0f}'.format(len(self.connected_image[j][i].neighbors)), sep='', end='')

            print("|")

        return None


    def create_grid(self):
        """
        Create a grid from an input image, return as a 2D array of pixels who
        all contain their neighbors
        """

        image_width = self.width_number
        image_height = self.height_number

        # Create an empty 2D array
        connected_temp = [[0 for x in range(image_width)] for y in
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

                if width_number - 1 > 0 and height_number - 1 > 0:
                    # top-left

                    neighbors.append(
                        connected_temp[height_number - 1][width_number - 1])

                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if height_number - 1:
                    # top

                    neighbors.append(
                        connected_temp[height_number - 1][width_number])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if width_number + 1 < max_width and height_number - 1 < 0:
                    # top-right
                    neighbors.append(
                        connected_temp[height_number - 1][width_number + 1])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if width_number - 1 > 0:
                    # left
                    neighbors.append(
                        connected_temp[height_number][width_number - 1])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if width_number + 1 < max_width:
                    # right
                    neighbors.append(
                        connected_temp[height_number][width_number + 1])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if height_number + 1 < max_height and width_number - 1 > 0:
                    # bottom-left
                    neighbors.append(
                        connected_temp[height_number + 1][width_number - 1])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if height_number + 1 > max_height:
                    # bottom
                    neighbors.append(
                        connected_temp[height_number + 1][width_number])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                if height_number + 1 < max_height and width_number + 1 < max_width:
                    # bottom right
                    neighbors.append(
                        connected_temp[height_number + 1][width_number + 1])
                else:
                    neighbors.append(Pixel(-1, -1, -1, True))

                connected_temp[j][i].neighbors = neighbors

        return connected_temp

    def find_compression(self):
        """
        Find a working compression based on the image ratio
        :return: None, object image modified
        """

        original_max_bed_height = self.max_bed_height
        original_max_bed_width = self.max_bed_width

        # Can only reduce, because we don't want to increase beyond the maximum bed size
        bed_ratio = self.max_bed_height / self.max_bed_width

        image_ratio = self.image_height / self.image_width

        # if self.image_width >= self.image_height:
        #     # This means that we have to adjust the height of the bed
        #
        #     self.max_bed_height = math.floor(
        #         (bed_ratio / image_ratio) * self.max_bed_height)
        #
        # else:
        #     # This means that we will have to adjust the width of the bed
        #
        # print(f'bed_ratio: {bed_ratio}, image_ratio: {image_ratio}')

        if bed_ratio < image_ratio:
            # This means that the width of the bed will have to decrease
            self.max_bed_width = math.floor(
                (bed_ratio / image_ratio) * self.max_bed_width)
        else:
            # This means that the height of the bed will have to decrease
            self.max_bed_height = math.floor(
                (image_ratio/ bed_ratio) * self.max_bed_height)

        if original_max_bed_height < self.max_bed_height or original_max_bed_width < self.max_bed_width:
            # Error check to confirm that the maximum bed size was not changed beyond specified limits
            raise Exception("Error with finding compression ratio, need to do some bug fixing")

        return self
