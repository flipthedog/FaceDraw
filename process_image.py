# Processing, binarizing the image

import cv2 as cv
import time

# grayImage
# Grayscale the color of the image
def grayImage(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray_image

# blurImage
# Input: A grayscale image
# Blur the image with different possible filters
# "regular", 0 = regular blur with cv.Blur()
# "median", 1 = median blur with cv.medianBlur()
# "bilateral", 2 = bilateral blur with cv.bilateralFilter()
# "gaussian", 3 = gaussian blur with cv.GaussianBlur()
def blurImage(gray_image, stringType):
    if stringType is "regular" or stringType is 0:
        blur = cv.blur(gray_image, (5, 5))
    elif stringType is "median" or stringType is 1:
        blur = cv.medianBlur(gray_image, 5)
    elif stringType is "bilateral" or stringType is 2:
        blur = cv.bilateralFilter(gray_image, 5, 8, 8)
    else:
        print("Error: Invalid blurImage() type parameter")

    return blur

# contourImage
# Input: A grayscale image
# Finds the contours of an image
def contourImage(image):
    ret, thresh = cv.threshold(gray_image, 55, 255, 0)
    contoured_image, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contoured_image

# thresholdImage
# Input: A (blurred) grayscale image
# Input: A string or integer specifying the thresholding type
# Find the threshold with different function types and parameters
# "regular" or 0: Global thresholding with cv.threshold()
# "gaussian" or 1: Adaptive mean thresholding with cv.adaptiveThreshold()
# "mean" or 2: Adaptive gaussian thresholding with cv.adaptiveThreshold()
def thresholdImage(gray_image, stringType, gaussianSize):
    if stringType is "regular" or 0:
        ret, thresholdImage = cv.threshold(gray_image, 127, 255, cv.THRESH_BINARY)
    elif stringType is "gaussian" or 1:
        thresholdImage = cv.adaptiveThreshold(gray_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, gaussianSize )
    elif stringType is "mean" or 2:
        thresholdImage = cv.adaptiveThreshold(gray_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, gaussianSize)
    elif stringType is "otsu" or 3:
        ret, thresholdImage = cv.threshold(gray_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    else:
        print("Error: Invalid stringtype parameter in thresholdImage()")
        return -1 # Return an error code

    return thresholdImage

# 
def morphTrans(threshold_image, stringType)


# Opening the image
image_name = 'pap_1.png'

def processImage(image, imagename):

    try:
        if image is not None:
            full_image_name = 'images/' + image_name
            imageToProcess = cv.imread(full_image_name)
        else:
            imageToProcess = image
    except Exception:
        print("Error: Image not opened")

    gray_image = grayImage(imageToProcess)
    blurred_image = blurImage(gray_image)
    threshold_image = thresholdImage(blurred_image)


#cv.drawContours(contoured_image, contours, -1, (255,255,0), 3)
cv.imshow('Original', image)
#cv.imshow('Your picture after', gray_image)
cv.imshow('Contours? ', contoured_image)
cv.imshow("Blurred", blur)
cv.imshow("Median Blur", medianBlur)
cv.imshow("Gaussian thresh", th2)
cv.imshow("Blurred Gaussian Thresh", th3)
cv.imshow("Median Blur, Gaussian thresh", th4)
cv.imshow("Bilateral Blur, Gaussian thresh", th5)
cv.waitKey(0)

cv.destroyAllWindows()