import os_
from chyson.decorators.coroutine import coroutine


@coroutine
def get_files(receiver):
    """
    A wrapper of os.walk()
    :param receiver:
    :return:
    """
    while True:
        path = (yield)
        if os_.path.isfile(path):
            receiver.send(os_.path.abspath(path))
        else:
            for root, dirs, files in os_.walk(path):
                for filename in files:
                    receiver.send(os_.path.abspath(os_.path.join(root, filename)))
