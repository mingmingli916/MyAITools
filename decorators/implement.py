def delegate(attribute_name, method_names):
    """
    Delegate the method_names to attribute_name
    :param attribute_name:
    :param method_names:
    :return:

    Example:
    _identitiy = lambda x: x

    @delegate('__list', ('pop', '__delitem__', '__getitem__', '__iter__', '__reversed__', '__len__', '__str__'))
    class SortedList:
        def __init__(self, sequence=None, key=None):
            self.__key = key or _identitiy
            assert hasattr(self.__key, '__call__')
            if sequence is None:
                self.__list = []
            elif isinstance(sequence, SortedList) and sequence.key == self.__key:
                self.__list = sequence.__list[:]
            else:
                self.__list = sorted(list(sequence), key=self.__key)
    """

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


def complete_comparisons(cls):
    """
    Provide the < or __lt__ function, the result comparison is created automatically.
    :param cls:
    :return:
    """
    assert cls.__lt__ is not object.__lt__, "{0} must define < and ideally ==".format(cls.__name__)
    if cls.__eq__ is object.__eq__:
        cls.__eq__ = lambda self, other: not (cls.__lt__(self, other) or cls.__lt__(other, self))
    cls.__ne__ = lambda self, other: not cls.__eq__(self, other)
    cls.__gt__ = lambda self, other: cls.__lt__(other, self)
    cls.__le__ = lambda self, other: not cls.__lt__(other, self)
    cls.__ge__ = lambda self, other: not cls.__lt__(self, other)
    return cls
