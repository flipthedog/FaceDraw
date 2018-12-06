# Raster.py
# A type of slicing solution, might be interesting
# Rasters the image to create a list of tool paths

# Import Statements
from Slicer import Slicer
import cv2 as cv
import math

class Raster():

    def __init__(self, image, feedrate, bed_size, line_width, z_hop=None, z_tune=None):
        # The image to be processed
        self.original_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

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

        self.line_width = line_width

    # TODO:
    # 1. Create a grid of the image based on line width
    # 2. Find out where to put down the marker
    # 3. Put it in a line

    # raster()
    # Create a rastering solution for the image
    def raster(self):

        number_cells_width = math.floor(self.max_width / self.line_width)
        number_cells_height = math.floor(self.max_height / self.line_width)

        # Define a two dimensional array on where to draw
        draw_arr = [[0 for x in range(number_cells_width)] for y in range(number_cells_height)]

        # Where the pixels to draw are
        inv_image = cv.bitwise_not(self.original_image)
        white_pixels = cv.findNonZero(inv_image)

        # Change draw_arr depending on image pixels
        for pixel2 in white_pixels:
            pixel = pixel2[0]

            # Transform from image space to draw_Arr space
            pixel_width_pos = pixel[1]
            pixel_height_pos = pixel[0]

            print(self.max_height)
            print(pixel_height_pos)
            exit()

            cell_pixel_width = math.floor((pixel_width_pos / self.max_width) * number_cells_width)
            cell_pixel_height = math.floor((pixel_height_pos / self.max_height) * number_cells_height)

            # Change draw arr pixel
            draw_arr[cell_pixel_width, cell_pixel_height] += 1


        # Array of lines to return
        lines = []

        # Move from one point in draw_arr to the next
        i = 0

        for i in range(0, number_cells_width):

            j = 0

            for j in range(0, number_cells_height):

                # Determine whether to draw here, otherwise add point to lines after converting
                if draw_arr[i, j] > 0:

                    pixel_width_pos = math.floor((i / number_cells_width) * self.image_width)
                    pixel_height_pos = math.floor((i / number_cells_height) * self.image_height)

                    if len(lines) == 0:
                        pixel_0 = [0,0]
                        previous_pixel = [pixel_width_pos, pixel_height_pos]
                        lines.append([pixel_0, previous_pixel])
                    else:
                        new_pixel = [pixel_width_pos, pixel_height_pos]
                        lines.append([previous_pixel, new_pixel])
                        previous_pixel = new_pixel

        return lines