import functools


def positive_result(function):
    """
    Assert the result be positive.
    :param function:
    :return:
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    return wrapper


def bounded(minimum, maximum):
    """
    Bound the output between the minimum and maximum.
    :param minimum:
    :param maximum:
    :return:
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result < minimum:
                return minimum
            elif result > maximum:
                return maximum
            return result

        return wrapper

    return decorator
