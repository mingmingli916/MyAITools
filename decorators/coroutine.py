import functools


def coroutine(function):
    """
    call next() function before the first yield
    :param function: coroutine
    :return:
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper
