# Taking a picture
import cv2 as cv
import re


# take_picture()
# input - filename: string of picture filename to be saved
def take_picture(filename='test'):

    image_ext = {'.jpg', '.png', '.gif'}

    flag = False

    for file_app in image_ext:

        if re.search(file_app, filename):
            # filename contains file-appendix
            flag = True

    capture = cv.VideoCapture(0)
    print("Taking picture")
    ret, frame = capture.read()

    cv.imshow('Your Picture: ' + filename + ' PRESS ANY KEY TO CLOSE', frame)

    print('../images/' + filename + '.png')

    while True:

        # Wait for user to press key
        if cv.waitKey(1) and cv.waitKey(0):
            # Store image in image/ folder
            print("Waiting ... ")

            if flag:
                cv.imwrite(r'images/' + filename, frame)
                cv.imwrite(r'../images/' + filename, frame)
            else:
                cv.imwrite(r'images/' + filename + '.png', frame)
                cv.imwrite(r'../images/' + filename + '.png', frame)

            cv.destroyAllWindows()
            break

    capture.release()
