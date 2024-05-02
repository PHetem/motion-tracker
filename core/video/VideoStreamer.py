import cv2
import datetime
import config.Config as Config
import utils.args.Args as Args
from core.video.Video import Video
from core.video.VideoRecorder import VideoRecorder
from core.video.VideoProcessor import VideoProcessor

class VideoStreamer:

    send = False
    firstFrame = None
    isCapturing = False
    noMovementTimer = 0
    captureTimer = 0
    consecutiveMotionFrames = 0
    sequenceCounter = 0
    resetTimer = 0
    videoObj = None
    recorderObj = None
    hasMovement = False
    showPreview = True

    def process(self, videoStream):

        print('Video processing starting')

        self.videoObj = Video()
        self.recorderObj = VideoRecorder()

        # Run every frame
        while True:

            self.hasMovement = False

            # Get current frame
            frame = self.videoObj.getFrame(videoStream)

            simplifiedFrame = VideoProcessor.removeDetails(frame)

            # Select base frame for comparison
            if self.firstFrame is None or self.resetTimer >= Config.conf['timeReset'] or self.sequenceCounter >= Config.conf['maxSequence']:
                self.updateBaseFrame(simplifiedFrame)
                continue

            diff = VideoProcessor.getDifferences(self.firstFrame, simplifiedFrame)

            movementDetected = VideoProcessor.checkForMovement(frame, diff)

            if movementDetected:
                # First frame captured
                if self.isCapturing is False:
                    self.startCapture()

                # Reached recording min size
                if self.consecutiveMotionFrames >= Config.conf['minFrames']:
                    self.send = True

                # Reached recording limit
                if self.captureTimer >= Config.conf['maxFrames']:
                    self.resetRecording()
                    continue

                self.consecutiveMotionFrames += 1

                self.setMovement(True)
                self.addText(frame)
                self.write(frame)

            elif self.isCapturing:
                # Reached recording limit
                if self.noMovementTimer >= Config.conf['noMovementLimit'] or self.captureTimer >= Config.conf['maxFrames']:
                    self.resetRecording()
                    continue

                self.setMovement(False)
                self.addText(frame)
                self.write(frame)

            self.resetTimer += 1
            self.showView(frame, diff)

            if self.checkUserInput() == 'q':
                print('Stopping execution')
                break

        self.videoObj.cleanUp(videoStream)

    def addText(self, frame):
        if self.noMovementTimer > 0:
            cv2.putText(frame, "No movement. Recording will stop in " + str(Config.conf['noMovementLimit'] - self.noMovementTimer) + ' frames', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        elif self.hasMovement:
            cv2.putText(frame, "Movement detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if Args.args["timestamp"]:
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

    def showView(self, frame, diff):
        if Args.args["preview"] and self.showPreview:
            cv2.imshow("Base", frame)

        if Args.args["delta"]:
            cv2.imshow("diff", diff)

    def endRecording(self):
        self.recorderObj.endRecording(self.send)
        self.send = False

    def resetRecording(self):
        self.endRecording()
        self.noMovementTimer = 0
        self.captureTimer = 0
        self.isCapturing = False

    def updateBaseFrame(self, simplifiedFrame):
        print('Base frame updated')
        self.resetTimer = 0
        self.sequenceCounter = 0
        self.firstFrame = simplifiedFrame

    def setMovement(self, movement):
        if movement:
            self.hasMovement = True
            self.noMovementTimer = 0
        else:
            self.consecutiveMotionFrames = 0
            self.noMovementTimer += 1

    def startCapture(self):
        self.recorderObj.newRecording()
        self.sequenceCounter += 1
        self.isCapturing = True

    def checkUserInput(self):
        key = cv2.waitKey(1)

        if key == ord("q"):
            return 'q'

    def write(self, frame):
        self.captureTimer += 1
        self.recorderObj.recorder.write(frame)
