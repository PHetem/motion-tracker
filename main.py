import time
import dotenv
import config.Config as Config
import utils.args.Args as Args
from core.video.Video import Video
from core.video.VideoStreamer import VideoStreamer

dotenv.load_dotenv()

Args.init()
Config.init()

video = Video()
videoStream = video.selectVideoInput()

if Args.args['delay'] > 0:
    print('Capture will start in ' + str(Args.args['delay']) + ' seconds')
    time.sleep(Args.args['delay'])

VideoStreamer().process(videoStream)
