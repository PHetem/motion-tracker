class StreamState:

    hasMovement = False
    isCapturing = False
    canSend = False
    breakExecution = False

    # Counter variables
    noMovementTimer = 0
    captureTimer = 0
    consecutiveMotionFrames = 0
    sequenceCounter = 0
    resetTimer = 0

    def setMovement(self, movement):
        if movement:
            self.hasMovement = True
            self.noMovementTimer = 0
        else:
            self.consecutiveMotionFrames = 0
            self.noMovementTimer += 1

    def setRecording(self, recording):
        if recording:
            self.sequenceCounter += 1
            self.isCapturing = True
        else:
            self.canSend = False
            self.isCapturing = False
            self.noMovementTimer = 0
            self.captureTimer = 0

    def baseFrameUpdated(self):
        self.resetTimer = 0
        self.sequenceCounter = 0

    def newFrame(self):
        self.captureTimer += 1
