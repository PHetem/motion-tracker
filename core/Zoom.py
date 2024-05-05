import cv2
import config.Config as Config

class Zoom:
    pressed = False
    xAxis = 0
    yAxis = 0

    def zoomIn(self, event, xAxis, yAxis, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN or (self.pressed is True and event == cv2.EVENT_MOUSEMOVE):
            self.pressed = True
            self.xAxis = xAxis
            self.yAxis = yAxis
        elif event == cv2.EVENT_LBUTTONUP:
            self.pressed = False
            self.closeWindow()

    def openWindow(self, frame):
        frame = self.crop(frame)
        cv2.imshow('Zoom', frame)

    def closeWindow(self):
        cv2.destroyWindow('Zoom')

    def crop(self, frame):
        xRes, yRes = Config.conf['resolution']
        magnification = .5 / Config.conf['magnification']

        # Get amount of pixels in each axis
        xReducedRes = int(xRes * magnification)
        yReducedRes = int(yRes * magnification)

        # Get area coordinates
        xCoordinatesLeft = int(self.xAxis - xReducedRes)
        xCoordinatesRight = int(self.xAxis + xReducedRes)
        yCoordinatesUp = int(self.yAxis + yReducedRes)
        yCoordinatesDown = int(self.yAxis - yReducedRes)

        # Avoid escaping coordinates (math always looks messy)
        if xCoordinatesLeft < 0:
            xCoordinatesLeft = 0
            xCoordinatesRight = xReducedRes * 2
        elif xCoordinatesRight > xRes:
            xCoordinatesRight = xRes
            xCoordinatesLeft = xRes - (xReducedRes * 2)

        if yCoordinatesUp > yRes:
            yCoordinatesUp = yRes
            yCoordinatesDown = yRes - (yReducedRes * 2)
        elif yCoordinatesDown < 0:
            yCoordinatesDown = 0
            yCoordinatesUp = yReducedRes * 2

        # Crop frame
        frame = frame[yCoordinatesDown:yCoordinatesUp, xCoordinatesLeft:xCoordinatesRight]

        return cv2.resize(frame, Config.conf['resolution'])
