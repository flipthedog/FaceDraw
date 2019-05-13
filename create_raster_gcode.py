from Slicer import Raster
from ImageProcessing import process_image
from ImageProcessing import takepicture
from Slicer import Writer
import cv2 as cv

# create_raster_gcode.py
# Create the gcode to draw an image using a raster

# INSTRUCTIONS:
# 1. Change the filename field below
# 2. Change the printer configuration below
# 3. Run the Script

# Your filename here
filename = 'slicer_test'

# Printer configuration
bed_size = [200, 200] # The size of your printer bed
feedrate = 750 # The feedrate of your x-y moves
z_hop = 3.0 # The total Z-hop between each dot
z_tune = 0.0 # Tune the Z-axis

# Take the picture
takepicture.take_picture(filename)

# open the image
cv_image = process_image.openImage(filename)

# Perform image processing
gray_image = process_image.grayImage(cv_image)
gray_edge_image = process_image.edgeDetection(gray_image)

# Show results of the cv functions
# Uncomment for debugging
cv.imshow('gray_image', gray_image)
cv.imshow('gray_edge', process_image.invertImage(gray_edge_image))

cv.waitKey(0)
cv.destroyAllWindows()

raster = Raster.Raster(cv_image, 300, bed_size, 1.0)
lines = raster.raster()

Writer.image_to_gcode("raster_1.gcode", lines, feedrate, raster.max_width, raster.max_height, raster.image_width, raster.image_height, z_hop=z_hop, z_tune=z_tune)