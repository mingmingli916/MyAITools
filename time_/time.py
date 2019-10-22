import time


def current_time():
    return time.asctime(time.localtime(time.time()))
