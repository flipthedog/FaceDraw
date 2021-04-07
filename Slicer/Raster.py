# Raster.py
# A type of slicing solution, might be interesting
# Rasters the image to create a list of tool paths

# Import Statements
from FaceDraw/ImageProcessing import process_image
import cv2 as cv
import math

class Raster():

    def __init__(self, image, bed_size, line_width = 1.0):
        """
        Constructor, create a Raster object to slice an image. Raster uses individual points as opposed to lines
        :param image: [opencv image] The image to process and slice
        :param bed_size: [mm] [n x m] The size of the bed height (n) by width (m)
        :param line_width: [mm] The line width of the image (dots per mm)
        """

        # The image to be processed
        self.original_image = image

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

    def raster(self):
        """
        Initiate the rastering of the loaded image
        :return: [[x1 y1] [x2 y2] ... [xn yn]] Array of points
        """

        # Cell density
        number_cells_width = math.floor(self.max_bed_width / self.line_width) # Number of cells / side
        number_cells_height = math.floor(self.max_bed_height / self.line_width) # Number of cells / side

       # Define a two dimensional array on where to draw, initialize to 0
        draw_arr = [[0 for x in range(number_cells_width)] for y in range(number_cells_height)]

        # Image processing
        gray_image = process_image.grayImage(self.original_image) # Convert image to gray
        gray_edge_image = process_image.edgeDetection(gray_image) # Perform edge detection on gray image
        white_pixels = cv.findNonZero(gray_edge_image) # Find all the pixels to draw

        # Change draw_arr depending on location of white_pixels
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
