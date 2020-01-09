import json


def save(filename, content, mode='w', encoding='utf8'):
    """
    Save object that can be serialized to json into json file.
    :param filename: json filename
    :param content: object to be serialzied
    :param mode: read or write
    :param encoding: 
    :return: 
    """
    with open(filename, mode) as f:
        json.dump(content, f)


def load(filename, encoding='utf8'):
    """
    Read json file into object.
    :param filename: json filename
    :param encoding: 
    :return: the loaded object
    """
    with open(filename, encoding=encoding) as f:
        obj = json.load(f)
        return obj
