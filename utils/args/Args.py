from utils.args.ArgsParser import ArgsParser
from utils.TimeUtils import TimeUtils

def init():
    global args
    args = ArgsParser.addArgs()
    args = vars(args.parse_args())

    if args['break'] is not None:
        TimeUtils().checkFormat(args['break'])