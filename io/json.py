import json


def save(filename, content, mode='w', encoding='utf8'):
    with open(filename, mode) as f:
        json.dump(content, f)
