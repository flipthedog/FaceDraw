# Taking a picture
import cv2 as cv

capture = cv.VideoCapture(0)
ret, frame = capture.read()

cv.imshow('Your Picture', frame)

if cv.waitKey(1) & 0xFF == ord('y'):
    cv.imwrite('images/floris_1.png',frame)
    cv.destroyAllWindows()


capture.release()