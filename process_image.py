# Processing, binarizing the image

import cv2 as cv
import numpy as np
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
def contourImage(gray_image):
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

# morphTrans()
# Perform a morphological transformation on the image
# Input: treshold_image: The thresholded image that needs to be morphed
# Input: stringType: A string or integer to select the type of transform
# stringType:
# "erosion" or "erode" or 0: Erode the selected image
# "dilute" or "dilution" or 1: Dilute the selected image
def morphTrans(threshold_image, stringType, iterations):

    if stringType is "erosion" or stringType is "erode" or stringType is 0:
        kernel = np.ones((5, 5), np.uint8)
        morphed_image = cv.erode(threshold_image, kernel, iterations)
    elif stringType is "dilate" or stringType is "dilation" or stringType is 1:
        print("This ran")
        kernel = np.ones((5, 5), np.uint8)
        morphed_image = cv.dilate(threshold_image, kernel, iterations)
    else:
        print("Error: Incorrect morphtrans() parameters")

    return morphed_image

# edgeDetection
# Use opencv's edge detection function Canny()
# Input: gray_image: A gray-scale image
# Output: An image with detected edges
def edgeDetection(gray_image):
    cannied_image = cv.Canny(gray_image, 155, 255)
    return cannied_image

# openImage()
# Open the image
# Input: image_name: the name of the image to be opened
# Output: The opened image
def openImage(image_name):
    try:
        full_image_name = 'images/' + image_name
        imageToProcess = cv.imread(full_image_name)
    except FileNotFoundError:
        print(FileNotFoundError.strerror)
        print("Error: Image not opened")

    return imageToProcess

def processImage(image_name, displayWindows):

    imageToProcess = openImage(image_name)
    gray_image = grayImage(imageToProcess)
    blur = blurImage(gray_image, 2)
    canny_image = edgeDetection(blur)

    # eroded_image = morphTrans(canny_image, 0, 1)
    # dilated_image = morphTrans(eroded_image, 1,10)

    # blurred_image = blurImage(gray_image, "bilateral")
    # threshold_image = thresholdImage(blurred_image, "otsu", 2)
    # #threshold_image = cv.threshold(threshold_image, 0, 255, cv.THRESH_BINARY)
    # dilated_image = morphTrans(threshold_image, 1, 1)
    # eroded_image = morphTrans(threshold_image, 0 ,100)

    # print("This is gray image width: " + str(gray_image.shape[0]))

    if displayWindows:
        cv.imshow("Original", imageToProcess)
        cv.imshow("Gray", gray_image)
        cv.imshow("Blurred", blurred_image)
        cv.imshow("Threshold", threshold_image)
        cv.imshow("Dilated", dilated_image)
        cv.imshow("Eroded", eroded_image)

        cv.waitKey(0)
        cv.destroyAllWindows()

    return canny_image