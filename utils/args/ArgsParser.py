import argparse

class ArgsParser:
    def addArgs() -> argparse.ArgumentParser:
        ap = argparse.ArgumentParser()
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size to consider movement")
        ap.add_argument("-p", "--preview", action="store_true", help="show image preview")
        ap.add_argument("-d", "--delta", action="store_true", help="show delta image")
        ap.add_argument("-b", "--start", help="start program at this time. 24h format (hh:mm)")
        ap.add_argument("-e", "--stop", help="stop program at this time. 24h format (hh:mm)")
        ap.add_argument("-c", "--show-contours", action="store_true", help="add contours to movement")
        ap.add_argument("-t", "--timestamp", action="store_true", help="add timestamp")
        ap.add_argument("-s", "--send", action="store_true", help="send file through telegram")
        return ap