import json
import os

def init():
    global conf
    conf = json.load(open('config/conf.json'))

    conf['botApiToken'] = os.getenv(conf['botApiToken'])
    conf['channelId'] = os.getenv(conf['channelId'])
