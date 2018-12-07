from Slicer import create_g_code
from Slicer import Slicer
from Slicer import Raster
from ImageProcessing import process_image
from Slicer import Writer

import cv2 as cv

cv_image = process_image.openImage('slicer_test_1.png')
# gray_image = process_image.grayImage(cv_image)
# eroded_image = process_image.morphTrans(gray_image,"erode",2,1)
# eroded_image2 = process_image.morphTrans(gray_image,"erode",3,1)
#
# cv.imshow('gray_image', gray_image)
# cv.imshow('eroded_image', eroded_image)
# cv.imshow('eroded_image2', eroded_image2)
#
# cv.imwrite('images/slicer_test_2.png',eroded_image2)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

# Set bed size to 300mm x 300mm

cv.imshow('hello', cv_image)
cv.waitKey(0)
cv.destroyAllWindows()

bed_size = [300, 300]
raster = Raster.Raster(cv_image, 300, bed_size, 0.3)
lines = raster.raster()

Writer.image_to_gcode("raster_test_1.gcode", lines, raster.max_width, raster.max_height, raster.image_width, raster.image_height)