import functools
import inspect
import logging
import os
import tempfile


def delegate(attribute_name, method_names):
    def decorator(cls):
        # We must use nonlocal so that the nested function uses the attribute_name from
        # the outer scope rather than attempting to use one from its own scope.
        nonlocal attribute_name
        # public and private attribute
        if attribute_name.startswith('__'):
            attribute_name = '_' + cls.__name__ + attribute_name
        for name in method_names:
            setattr(cls, name, eval('lambda self, *a, **kw: self.{0}.{1}(*a, **kw)'.format(attribute_name, name)))
        return cls

    return decorator


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


if __debug__:
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(tempfile.gettempdir(), 'logged.log'))

    logger.addHandler(handler)


    def logged(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            log = 'called: ' + function.__name__ + '('
            log += ', '.join(
                ['{0!r}'.format(a) for a in args] + ['{0!s}={1!r}'.format(k, v) for k, v in kwargs.items()])
            result = exception = None
            try:
                result = function(*args, *kwargs)
                return result
            except Exception as err:
                exception = err
            finally:
                log += (
                    (') -> ' + str(result)) if exception is None else ') {0}: {1}'.format(type(exception), exception))
                logger.debug(log)
                if exception is not None:
                    raise exception

        return wrapper
else:
    def logged(function):
        return function


# If we want to give meaning to annotations, for example, to provide type checking,
# one approach is to decorate the functions we want the meaning to apply to
# with a suitable decorator.
def strictly_typed(function):
    """
    # This decorator requires that every argument and the return value must be
    # annotated with the expected type.
    # Notice that the checking is done only in debug mode (which is Python’s default
    # mode—controlled by the -O command-line option and the PYTHONOPTIMIZE environment variable).

    :param function:
    :return:
    """
    annotations = function.__annotations__
    arg_spec = inspect.getfullargspec(function)

    # assert all type is given
    assert 'return' in annotations, 'missing type for return value'
    for arg in arg_spec.args + arg_spec.kwonlyargs:  # keyword only args
        assert arg in annotations, 'missing type for parameter "{}"'.format(arg)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # argument check
        # zip() returns an iterator and dictionary.times() returns a dictionary view
        # we cannot concatenate them directly, so first we convert them both to lists.
        all_args = list(zip(arg_spec.args, args)) + list(kwargs.items())
        for name, arg in all_args:
            assert isinstance(arg, annotations[name]), (  # the () protect the format
                'expected argument "{}" of {} get {}'.format(name, annotations[name], type(arg)))

        # result check
        result = function(*args, **kwargs)
        assert isinstance(result, annotations['return']), (
            'expected return of {} got {}'.format(annotations['return'], type(result)))

        return result

    return wrapper


def complete_comparisons(cls):
    assert cls.__lt__ is not object.__lt__, "{0} must define < and ideally ==".format(cls.__name__)
    if cls.__eq__ is object.__eq__:
        cls.__eq__ = lambda self, other: not (cls.__lt__(self, other) or cls.__lt__(other, self))
    cls.__ne__ = lambda self, other: not cls.__eq__(self, other)
    cls.__gt__ = lambda self, other: cls.__lt__(other, self)
    cls.__le__ = lambda self, other: not cls.__lt__(other, self)
    cls.__ge__ = lambda self, other: not cls.__lt__(self, other)
    return cls
