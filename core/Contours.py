import utils.args.Args as Args
import cv2
import imutils

class Contours:

    coordinates = None
    considerableAreas = []


    def __init__(self, diff):
        contours = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.coordinates = imutils.grab_contours(contours)

    def process(self, frame):

        self.considerableAreas = []

        for contour in self.coordinates:
            # Not enough movement, disregard
            if cv2.contourArea(contour) < Args.args["min_area"]:
                continue

            if Args.args["show_contours"]:
                self.addRectangle(frame, contour)

            self.considerableAreas.append(contour)

    def addRectangle(self, frame, contour):
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
