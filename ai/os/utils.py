import os_


def list_files(path):
    result = []
    all = list_dirs(path)
    for a in all:
        if os_.path.isfile(os_.path.join(path, a)):
            result.append(a)
    return result


def list_dirs(path):
    result = []
    all = os_.listdir(path)
    for a in all:
        if os_.path.isdir(os_.path.join(path, a)):
            result.append(a)
    return result


def join(lst):
    lst.remove('')
    return os_.path.sep.join(lst)
