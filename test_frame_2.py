from Slicer import create_g_code
from Slicer import Slicer
from Slicer import Raster
from ImageProcessing import process_image
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
raster.raster()