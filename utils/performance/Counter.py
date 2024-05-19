import datetime

class Counter:

    startingTime = 0
    endingTime = 0
    lastStepEnd = 0
    average = 0
    maxSteps = 0
    iterations = []

    def start(self, maxSteps = 0):
        self.maxSteps = maxSteps
        self.startingTime = datetime.datetime.now().timestamp()

    def end(self):
        self.endingTime = datetime.datetime.now().timestamp()
        print(f"Average per step was {str(self.getAverage())}")
        print(f"Total seconds elapsed was {str(self.endingTime - self.startingTime)}")
        self.iterations = []
        self.lastStepEnd = 0
        self.start(self.maxSteps)

    def addStep(self):
        lastStepEnd = self.lastStepEnd if self.lastStepEnd > 0 else self.startingTime
        self.iterations.append(datetime.datetime.now().timestamp() - lastStepEnd)

        self.lastStepEnd = datetime.datetime.now().timestamp()
        if self.maxSteps > 0 and len(self.iterations) >= self.maxSteps:
            self.end()

    def getAverage(self):
        return sum(self.iterations) / len(self.iterations)