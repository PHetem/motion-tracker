from imutils.video import VideoStream
from pygrabber.dshow_graph import FilterGraph
import time
import cv2
import config.Config as Config

class Video:
    def selectVideoInput(self):
        source = self.selectCameraSource()
        vs = VideoStream(source, resolution = Config.conf['resolution'], framerate = Config.conf['fps']).start()
        time.sleep(2.0)

        return vs

    def selectCameraSource(self):
        cameras = self.getAvailableCameras()

        self.printCameraMessage(cameras)

        response = int(input())

        if response >= len(cameras):
            print('Invalid selection. Exiting program')
            exit(1)

        return response

    def getAvailableCameras(self):
        return FilterGraph().get_input_devices()

    def printCameraMessage(self, cameras):
        message = 'Please select which webcam should be used: \n'

        index = 0
        for camera in cameras:
            message += '[' + str(index) + '] ' + str(camera) + '\n'
            index += 1

        print(message)

    def getFrame(self, videoStream):
        frame = videoStream.read()
        return frame.copy()

    def cleanUp(self, videoStream):
        videoStream.stop()
        cv2.destroyAllWindows()