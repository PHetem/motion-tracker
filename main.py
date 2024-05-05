import time
import dotenv
import config.Config as Config
import utils.args.Args as Args
from core.video.Video import Video
from core.video.VideoStreamer import VideoStreamer
from utils.TimeUtils import TimeUtils

dotenv.load_dotenv()

Args.init()
Config.init()

video = Video()
videoStream = video.selectVideoInput()


if Args.args['start'] is not None:
    timeUtilsObj = TimeUtils()
    timeUtilsObj.setTimeLimit(Args.args['start'])
    print('Capture will start at ' + Args.args['start'])

    while not timeUtilsObj.aboveSetTime():
        time.sleep(1)

VideoStreamer().process(videoStream)
