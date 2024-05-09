import cv2
import datetime
import config.Config as Config
import utils.args.Args as Args
from utils.TimeUtils import TimeUtils
from core.video.Video import Video
from core.video.VideoRecorder import VideoRecorder
from core.video.VideoProcessor import VideoProcessor
from core.video.StreamState import StreamState
from core.Zoom import Zoom
class VideoStreamer:
    firstFrame = None

    # Runtime objectss
    videoObj = None
    recorderObj = None
    zoomObj = None
    timeUtilsObj = None
    state = None

    def process(self, videoStream):

        print('Video processing starting')

        self.videoObj = Video()
        self.recorderObj = VideoRecorder()
        self.zoomObj = Zoom()
        self.state = StreamState()

        if Args.args['stop'] is not None:
            self.timeUtilsObj = TimeUtils()
            self.timeUtilsObj.setTimeLimit(Args.args['stop'])

        # Run every frame
        while True:

            self.state.hasMovement = False

            # Get current frame
            frame = self.videoObj.getFrame(videoStream)

            simplifiedFrame = VideoProcessor.removeDetails(frame)

            # Select base frame for comparison
            if self.firstFrame is None or self.state.resetTimer >= Config.conf['timeReset'] or self.state.sequenceCounter >= Config.conf['maxSequence']:
                self.updateBaseFrame(simplifiedFrame)
                continue

            diff = VideoProcessor.getDifferences(self.firstFrame, simplifiedFrame)

            movementDetected = VideoProcessor.checkForMovement(frame, diff)

            if movementDetected:
                # First frame captured
                if self.state.isCapturing is False:
                    self.startCapture()
                    if Args.args['sound_chime']:
                        print('\a')

                # Reached recording min size
                if self.state.consecutiveMotionFrames >= Config.conf['minFrames']:
                    self.state.canSend = True

                # Reached recording limit
                if self.state.captureTimer >= Config.conf['maxFrames']:
                    self.resetRecording()
                    continue

                self.state.consecutiveMotionFrames += 1

                self.state.setMovement(True)
                self.addText(frame)
                self.write(frame)

            elif self.state.isCapturing:
                # Reached recording limit
                if self.state.noMovementTimer >= Config.conf['noMovementLimit'] or self.state.captureTimer >= Config.conf['maxFrames']:
                    self.resetRecording()
                    continue

                self.state.setMovement(False)
                self.addText(frame)
                self.write(frame)
            else:
                self.addText(frame)

            self.state.resetTimer += 1
            self.showView(frame, diff)

            if self.state.breakExecution:
                print('Stopping execution due to user input')
                break

            if Args.args['stop'] is not None and self.timeUtilsObj.aboveSetTime():
                print('Stopping execution due to time limit constraint')
                break

        self.videoObj.cleanUp(videoStream)

    def addText(self, frame):
        if self.state.noMovementTimer > 0:
            cv2.putText(frame, "No movement. Recording will stop in " + str(Config.conf['noMovementLimit'] - self.state.noMovementTimer) + ' frames', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif self.state.hasMovement:
            cv2.putText(frame, "Movement detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if Args.args["timestamp"]:
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

    def showView(self, frame, diff):
        if Args.args["preview"]:
            cv2.imshow('Base', frame)
            self.checkUserInput(frame)

        if Args.args['delta']:
            cv2.imshow('diff', diff)

    def resetRecording(self):
        self.recorderObj.endRecording(self.state.canSend)
        self.state.setRecording(False)

    def updateBaseFrame(self, simplifiedFrame):
        print('Base frame updated')
        self.state.baseFrameUpdated()
        self.firstFrame = simplifiedFrame

    def startCapture(self):
        self.recorderObj.newRecording()
        self.state.setRecording(True)

    def checkUserInput(self, frame):
        self.checkZoom(frame)
        key = cv2.waitKey(1)

        if key == ord('u'):
            self.firstFrame = None

        if key == ord('q'):
            self.state.breakExecution = True

    def write(self, frame):
        self.state.newFrame()
        self.recorderObj.recorder.write(frame)

    def checkZoom(self, frame):
        cv2.setMouseCallback('Base', self.zoomObj.zoomIn)

        if self.zoomObj.pressed:
            self.zoomObj.openWindow(frame.copy())
