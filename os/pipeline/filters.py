import sys

import os
from chyson.decorators.coroutine import coroutine
from chyson.os.pipeline.acquirer import get_files
from chyson.os.pipeline.reporter import reporter


@coroutine
def suffix_matcher(receiver, suffixes):
    while True:
        filename = (yield)
        if filename.endswith(suffixes):
            receiver.send(filename)


@coroutine
def size_matcher(receiver, minimum=None, maximum=None):
    while True:
        filename = (yield)
        size = os.path.getsize(filename)
        if ((minimum is None or size >= minimum) and
                (maximum is None or size <= maximum)):
            receiver.send(filename)


if __name__ == '__main__':
    # notice the order in coroutine
    receiver = reporter()
    pipeline = size_matcher(receiver, minimum=1024)
    pipeline = suffix_matcher(pipeline, (".png", ".jpg", ".jpeg"))
    pipeline = get_files(pipeline)

    try:
        for file in sys.argv[1:]:
            print(file)
            pipeline.send(file)
    finally:
        pipeline.close()
        receiver.close()
