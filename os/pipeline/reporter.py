from chyson.decorators.coroutine import coroutine


@coroutine
def reporter():
    while True:
        filename = (yield)
        print(filename)
