# Raster.py
# A type of slicing solution, might be interesting
# Rasters the image to create a list of tool paths

# Import Statements
import cv2 as cv
import math

class Raster():

    def __init__(self, image, bed_size, line_width = 0.3):
        # The image to be processed
        self.original_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        self.line_width = line_width

        # Bed specifications
        self.max_width = bed_size[0]
        self.max_height = bed_size[1]

        # Image specifications
        shape = image.shape
        self.image_width = shape[1]  # Horizontal pixel no.
        self.image_height = shape[0]  # Vertical pixel no.

    # raster()
    # Create a rastering solution for the image
    def raster(self):

        number_cells_width = math.floor(self.max_width / self.line_width)
        number_cells_height = math.floor(self.max_height / self.line_width)

        print("These are the dimensions of the array: " + str(number_cells_width) + ", " + str(number_cells_height))

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



            cell_pixel_width = math.floor((pixel_width_pos / self.image_height) * number_cells_width)
            cell_pixel_height = math.floor((pixel_height_pos / self.image_width) * number_cells_height)

            #print(cell_pixel_width)
            #print(cell_pixel_height)

            # Change draw arr pixel
            draw_arr[cell_pixel_width][cell_pixel_height] += 1


        # Array of lines to return
        lines = []

        # Move from one point in draw_arr to the next

        for i in range(0, number_cells_width):

            for j in range(0, number_cells_height):

                # Determine whether to draw here, otherwise add point to lines after converting
                if draw_arr[i][j] > 0:

                    pixel_width_pos = math.floor((i / number_cells_width) * self.image_width)
                    pixel_height_pos = math.floor((j / number_cells_height) * self.image_height)

                    lines.append([pixel_width_pos, pixel_height_pos])

        return lines

