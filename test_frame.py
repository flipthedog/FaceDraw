import process_image
import cv2 as cv

cv_image = process_image.openImage("floris_2.png")
gray_image = process_image.grayImage(cv_image)
#contour_image = process_image.contourImage(gray_image)
thresh_image = process_image.thresholdImage(gray_image, 1, 1)
eroded_image = process_image.morphTrans(thresh_image, 1, 2, 1)
edge_detect = process_image.edgeDetection(gray_image)
inv_image = process_image.invertImage(edge_detect)

#cv.imshow('image1', cv_image)
#cv.imshow('thresh image', thresh_image)
#cv.imshow('eroded image', eroded_image)


#cv.imshow('image2', contour_image)
cv.imshow('edge', edge_detect)
cv.imshow('inv', inv_image)

cv.imwrite('images/slicer_test_1.png', inv_image)

cv.waitKey(0)
cv.destroyAllWindows()