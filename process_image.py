# Processing, binarizing the image

import cv2 as cv
import time

image_name = 'floris_1.png'
full_image_name = 'images/' + image_name
image = cv.imread(full_image_name)


gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

contours = 0
ret,thresh = cv.threshold(gray_image,55,255,0)
contoured_image, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#cv.drawContours(contoured_image, contours, -1, (255,255,0), 3)


cv.imshow('Your picture before', image)
cv.imshow('Your picture after', gray_image)
cv.imshow('Contours? ', contoured_image)

cv.waitKey(0)

cv.destroyAllWindows()