import requests
import config.Config as Config

class Send:

    filepath = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.botApiToken = Config.conf['botApiToken']
        self.channelId = Config.conf['channelId']

    def sendVideo(self):
        url = 'https://api.telegram.org/bot' + self.botApiToken + '/sendVideo'
        files = {'video': open(self.filepath, 'rb')}
        payload = {'chat_id': self.channelId}
        requests.post(url, data=payload, files = files)
        print('Video sent')

