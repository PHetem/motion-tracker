from utils.args.ArgsParser import ArgsParser
from utils.TimeUtils import TimeUtils

def init():
    global args
    args = ArgsParser.addArgs()
    args = vars(args.parse_args())

    if args['start'] is not None:
        TimeUtils().checkFormat(args['start'])

    if args['stop'] is not None:
        TimeUtils().checkFormat(args['stop'])
