from utils.args.ArgsParser import ArgsParser

def init():
    global args
    args = ArgsParser.addArgs()
    args = vars(args.parse_args())