import re

import requests
from chyson.decorators.coroutine import coroutine


@coroutine
def regex_matcher(receiver, regex):
    while True:
        text = (yield)  # suspends execution waiting for the yield expression
        for match in regex.finditer(text):
            receiver.send(match)


@coroutine
def receiver(func):
    while True:
        match = (yield)
        if match is not None:
            func(match)


if __name__ == '__main__':

    URL_RE = re.compile(r'''href=(?P<quote>['"])(?P<url>[^\1]+?)(?P=quote)''', re.IGNORECASE)
    flags = re.MULTILINE | re.IGNORECASE | re.DOTALL
    H1_RE = re.compile(r'<h1>(?P<h1>.+?)</h1>', flags)
    H2_RE = re.compile(r'<h2>(?P<h2>.+?)</h2>', flags)


    def just_print(match):
        ignore = frozenset({'style.css', 'index.html'})
        groups = match.groupdict()
        if 'url' in groups and groups['url'] not in ignore:
            print('    URL:', groups['url'])
        elif 'h1' in groups:
            print('    H1:', groups['h1'])
        elif 'h2' in groups:
            print('    H2:', groups['h2'])


    recei = receiver(just_print)
    matchers = (regex_matcher(recei, URL_RE),
                regex_matcher(recei, H1_RE),
                regex_matcher(recei, H2_RE))

    try:

        response = requests.get('http://chyson.net')
        html = response.text
        for matcher in matchers:
            matcher.send(html)
    finally:
        for matcher in matchers:
            matcher.close()
        recei.close()
