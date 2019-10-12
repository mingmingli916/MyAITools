import os


def list_files(path):
    result = []
    all = list_dirs(path)
    for a in all:
        if os.path.isfile(os.path.join(path, a)):
            result.append(a)
    return result


def list_dirs(path):
    result = []
    all = os.listdir(path)
    for a in all:
        if os.path.isdir(os.path.join(path, a)):
            result.append(a)
    return result


def join(lst):
    lst.remove('')
    return os.path.sep.join(lst)
