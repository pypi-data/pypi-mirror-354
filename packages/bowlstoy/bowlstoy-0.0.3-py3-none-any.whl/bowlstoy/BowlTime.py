import time


def GetStampString():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))