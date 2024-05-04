import json
import os

def init():
    global conf
    conf = json.load(open('config/conf.json'))

    conf['botApiToken'] = os.getenv(conf['botApiToken'])
    conf['channelId'] = os.getenv(conf['channelId'])

    if conf['magnification'] <= 0:
        raise Exception('Magnification has to be higher than 0.')

    if conf['magnification'] > 100:
        raise Exception('Magnification cannot be higher than 100.')
