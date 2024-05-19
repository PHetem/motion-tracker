import datetime

class TimeUtils:

    breakAt = None

    def setTimeLimit(self, argument):
        hours, minutes = argument.split(':')
        now = datetime.datetime.now()

        breakAt = now.replace(hour = int(hours), minute = int(minutes), second = 0)
        if breakAt < now:
            breakAt += datetime.timedelta(days = 1)

        self.breakAt = breakAt

    def checkFormat(self, argument):
        if not ((len(argument) == 5) and (':' in argument) and (argument.replace(':', '').isdigit())):
            raise Exception('Incorrect break argument format.')

        hours, minutes = argument.split(':')

        if not (0 <= int(hours) < 24 and 0 <= int(minutes) < 60):
            raise Exception('Incorrect break argument format.')

    def aboveSetTime(self):
        now = datetime.datetime.now()
        return self.breakAt is not None and self.breakAt < now

    def setTimer(self, seconds):
        breakAt = datetime.datetime.now()
        breakAt += datetime.timedelta(seconds = seconds)

        self.breakAt = breakAt

    def resetTimer(self):
        self.breakAt = None

