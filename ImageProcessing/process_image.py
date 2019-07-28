# Processing, binarizing the image

import cv2 as cv
import numpy as np
import re

def grayImage(image, show=False):
    """
    Convert the image to grayscale
    :param image: [opencv image] The image to covnert
    :param show: [boolean] Show the new image
    :return: [opencv image] Grayed image
    """
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if show:
        cv.imshow('Gray image', gray_image)
    return gray_image

def blurImage(gray_image, stringType, show=False):
    """
    Blur the image
    :param gray_image: Convert the image to grayscale
    :param stringType: [str] or [int] Type of blur to perform
        0. regular
        1. median
        2. bilateral
        3. gaussian
    :param show: [boolean] Show the new image
    :return: [opencv image] Blurred image
    """
    if stringType is "regular" or stringType is 0:
        blur = cv.blur(gray_image, (5, 5))
    elif stringType is "median" or stringType is 1:
        blur = cv.medianBlur(gray_image, 5)
    elif stringType is "bilateral" or stringType is 2:
        blur = cv.bilateralFilter(gray_image, 5, 8, 8)
    else:
        print("Error: Invalid blurImage() type parameter")
    if show:
        cv.imshow('Blurred image', blur)
    return blur

def contourImage(gray_image, show=False):
    """
    Find the contours in the image and highlight them
    :param gray_image: [opencv image] An image in grayscale
    :param show: [boolean] Show the new image
    :return: [opencv image] The contoured image
    """
    ret, thresh = cv.threshold(gray_image, 55, 255, 0)
    contoured_image, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if show:
        cv.imshow('Contour image', contoured_image)
    return contoured_image

def thresholdImage(gray_image, stringType, gaussianSize=None, show=False):
    """
    Remove all of the pixels below a treshold value
    :param gray_image: [opencv image] A grayscale image
    :param stringType: [str] or [int] The type of thresholding
        0. regular
        1. gaussian
        2. mean
        3. otsu
    :param gaussianSize: [int] if gaussian, the size of the gaussian function
    :param show: [boolean] Show the new image
    :return: [opencv image] The thresholded image
    """
    if stringType is "regular" or 0:
        ret, thresholdImage = cv.threshold(gray_image, 120, 255, cv.THRESH_BINARY)
    elif stringType is "gaussian" or 1:
        thresholdImage = cv.adaptiveThreshold(gray_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, gaussianSize )
    elif stringType is "mean" or 2:
        thresholdImage = cv.adaptiveThreshold(gray_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, gaussianSize)
    elif stringType is "otsu" or 3:
        ret, thresholdImage = cv.threshold(gray_image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    else:
        print("Error: Invalid stringtype parameter in thresholdImage()")
        return -1 # Return an error code

    if show:
        cv.imshow('Threshold image', thresholdImage)
    return thresholdImage


def morphTrans(threshold_image, stringType, intensity, iterations, show=False):
    """
    Perform a morphological transformation on the image
    :param threshold_image: [opencv image] The thresholded image that needs to be morphed
    :param stringType: [str] or [int] The type of morphing to perform
    :param intensity: [int] The intensity of the morphing
    :param iterations: [int] The number of morphs
    :param show: [boolean] Show the new image
    :return: [opencv image] The morphed image
    """
    kernel = np.ones((intensity, intensity), np.uint8)

    if stringType is "erosion" or stringType is "erode" or stringType is 0:
        morphed_image = cv.erode(threshold_image, kernel, iterations)
    elif stringType is "dilate" or stringType is "dilation" or stringType is 1:
        morphed_image = cv.dilate(threshold_image, kernel, iterations)
    elif stringType is "open" or stringType is "opening" or stringType is 2:
        morphed_image = cv.morphologyEx(threshold_image, cv.MORPH_OPEN, kernel)
    else:
        print("Error: Incorrect morphtrans() parameters")

    if show:
        cv.imshow('Morphed Image', morphed_image)

    return morphed_image

def edgeDetection(gray_image, show=False):
    """
    Perform edge detection on an image
    :param gray_image: [opencv image] A gray image to perform edge detection on
    :param show: [boolean] Show the new image
    :return: [opencv image] The edge detected image
    """
    cannied_image = cv.Canny(gray_image, 85, 155, apertureSize=3)
    if show:
        cv.imshow('Edge Detection Image', cannied_image)
    return cannied_image

def openImage(image_name, show=False):
    """
    Open an image
    :param image_name: [str] The filename of the image
    :param show: [boolean] Show the opened image
    :return:
    """
    image_ext = {'.jpg', '.png', '.gif', '.jpeg'}

    flag = False

    for file_app in image_ext:

        if re.search(file_app, image_name):
            # filename contains file-appendix
            flag = True

    if flag:
        pass
    else:
        image_name = image_name + '.png'

    try:
        imageToProcess = cv.imread(r'images/' + image_name)
    except FileNotFoundError:
        print(FileNotFoundError.strerror)
        print("Error: Image not opened")

    if show:
        cv.imshow('Opened image', imageToProcess)

    return imageToProcess


def invertImage(cv_image, show=False):
    """
    Invert the pixels of a binary (black or white) image
    :param cv_image: [opencv image] The binary image to invert
    :return: inverted_image [opencv image] The inverted image
    """
    inverted_image = cv.bitwise_not(cv_image)
    if show:
        cv.imshow('Inverted Image', inverted_image)
    return inverted_image


def processImage(image_name, displayWindows=False):

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
        # cv.imshow("Blurred", blurred_image)
        # cv.imshow("Threshold", threshold_image)
        # cv.imshow("Dilated", dilated_image)
        # cv.imshow("Eroded", eroded_image)

        cv.waitKey(0)
        cv.destroyAllWindows()

    return canny_image