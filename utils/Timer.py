
import time

class Timer:

    def sleepWithCountdown(seconds, increment, message):
        while (seconds >= 0):
            print(message.replace('{SECONDS}', str(seconds)))
            time.sleep(increment)
            seconds -= increment

