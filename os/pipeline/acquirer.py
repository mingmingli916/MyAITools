import os
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
        if os.path.isfile(path):
            receiver.send(os.path.abspath(path))
        else:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    receiver.send(os.path.abspath(os.path.join(root, filename)))
