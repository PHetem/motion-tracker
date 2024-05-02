
import time

class Timer:

    def sleepWithCountdown(seconds, increment, message):
        while (seconds > 0):
            if increment > seconds:
                increment = seconds

            print(message.replace('{SECONDS}', str(seconds)))
            time.sleep(increment)
            seconds -= increment

