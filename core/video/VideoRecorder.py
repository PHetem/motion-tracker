import cv2
import random
import datetime
import os
import pathlib
import config.Config as Config
import utils.args.Args as Args
from utils.StorageUtils import StorageUtils
from core.Send import Send

class VideoRecorder:

    recorder = None
    fourcc = None
    filename = None
    filepath = None

    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    def reset(self):
        if self.recorder is not None:
            self.recorder.release()

        print(f"Recording finished at {datetime.datetime.now().strftime('%I:%M:%S')}. Saving video.")

    def newRecording(self):
        self.filename = 'recordings/' + datetime.datetime.now().strftime("%d_%m_%Y_%I_%M_%S_") + str(random.randrange(10000, 99999)) + '.mp4'
        self.filepath = pathlib.PureWindowsPath(os.getcwd() + '/' + self.filename)
        self.recorder = cv2.VideoWriter(self.filename, self.fourcc, Config.conf['fps'], Config.conf['resolution'])
        print(f"New recording started at {datetime.datetime.now().strftime('%I:%M:%S')}")


    def endRecording(self, send):
        self.reset()
        StorageUtils('recordings').manageStorageSpace()

        if send and Args.args["send"]:
            Send(self.filepath).sendVideo()