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
filename = 'dog.jpg'

# Printer configuration
bed_height = 280
bed_width = 220
bed_size = [bed_height, bed_width] # The size of your printer bed
feedrate = 1000 # The feedrate of your x-y moves

z_hop = 3.0 # The total Z-hop between each dot (mm)
z_tune = 0.0 # Tune the Z-axis

# Take the picture
# takepicture.take_picture(filename) # Uncomment this if you want to take a picture

# open the image
cv_image = process_image.openImage(filename)


# Perform image processing
gray_image = process_image.grayImage(cv_image)
gray_edge_image = process_image.edgeDetection(gray_image)

# Show results of the cv functions
# Uncomment for debugging
resized = cv.resize(cv_image, (1320, 720))
cv.imshow('image', resized)
resized = cv.resize(gray_image, (1320, 720))
cv.imshow('gray_image', resized)
resized = cv.resize(process_image.invertImage(gray_edge_image), (1320, 720))
cv.imshow('gray_edge', resized)

# Wait for user to press key
cv.waitKey(0)
cv.destroyAllWindows() # delete all windows

# Create a raster object to slice the image
raster = Raster.Raster(cv_image, bed_size, line_width=1.0)
points = raster.raster()

Writer.points_to_gcode(filename, points, feedrate, z_hop=z_hop, z_tune=z_tune)