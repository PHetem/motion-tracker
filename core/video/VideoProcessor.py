import cv2
from core.Contours import Contours

class VideoProcessor:
    def checkForMovement(frame, diff):
        ContoursObj = Contours(diff)
        ContoursObj.process(frame)

        return ContoursObj.considerableAreas

    def removeDetails(frame):
        # Remove color
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Add blur to reduce noise
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        return cv2.blur(frame, (10, 10))

    def getDifferences(firstFrame, frame):
        # Remove every pixel that is the same in both images
        diff = cv2.absdiff(firstFrame, frame)

        # Remove every pixel with no significant change
        diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        # Expand area to fill potential holes
        return cv2.dilate(diff, None, iterations = 2)