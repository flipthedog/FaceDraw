from Slicer import Raster
from ImageProcessing import process_image
from Slicer import Writer
import cv2 as cv

# create_raster_gcode.py
# Create the gcode to draw an image using a raster

# INSTRUCTION:
# 1. Create a .png image
# 2. Change the filename field below
# 3.

# Your filename here
filename = 'slicer_test_1.png'

# open the image
cv_image = process_image.openImage(filename)

# 
gray_image = process_image.grayImage(cv_image)
eroded_image = process_image.morphTrans(gray_image,"erode", 2, 1)
eroded_image2 = process_image.morphTrans(gray_image,"erode", 3, 1)


# Show results of the cv functions
# Uncomment for debugging
# cv.imshow('gray_image', gray_image)
# cv.imshow('eroded_image', eroded_image)
# cv.imshow('eroded_image2', eroded_image2)
# cv.destroyAllWindows()

# Save an intermediate image for debugging
#cv.imwrite('images/slicer_test_2.png',eroded_image2)

# Set bed size to 300mm x 300mm
cv.imshow('hello', cv_image)
cv.waitKey(0)
cv.destroyAllWindows()

bed_size = [200, 200]
raster = Raster.Raster(cv_image, 300, bed_size, 1.0)
lines = raster.raster()

print("HEre")
Writer.image_to_gcode("raster_test_1.gcode", lines, raster.max_width, raster.max_height, raster.image_width, raster.image_height)