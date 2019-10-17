import functools


def positive_result(function):
    @functools.wraps(function)
    # simplify
    # wrapper.__name__ = function.__name__
    # wrapper.__doc__ = function.__doc__
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        assert result >= 0, function.__name__ + "() result isn't >=0"
        return result

    return wrapper


# In some cases it would be useful to be able to parameterize a decorator, but at
# first sight this does not seem possible since a decorator takes just one argument,
# a function or method. But there is a neat solution to this. We can call a
# function with the parameters we want and that returns a decorator which can
# then decorate the function that follows it.
def bounded(minimum, maximum):
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
