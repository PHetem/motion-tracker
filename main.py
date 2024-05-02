import time
import dotenv
import config.Config as Config
import utils.args.Args as Args
from utils.Timer import Timer
from core.video.Video import Video
from core.video.VideoStreamer import VideoStreamer

dotenv.load_dotenv()

Args.init()
Config.init()

video = Video()
videoStream = video.selectVideoInput()

if Args.args['delay'] > 0:
    message = 'Capture will start in {SECONDS} seconds'
    Timer.sleepWithCountdown(Args.args['delay'], 60, message)

VideoStreamer().process(videoStream)
