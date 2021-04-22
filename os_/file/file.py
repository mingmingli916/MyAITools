#!/usr/bin/env python3
"""
@project: chyson
@file: file
@author: mike
@time: 2021/2/7
 
@function:
"""

if sys.platform.startswith('win'):
    def get_files(names):
        for name in names:
            if os.path.isfile(name):
                yield name
            else:
                for file in glob.iglob(name):
                    if not os.path.isfile(file):
                        continue
                    yield file
else:
    def get_files(names):
        return (file for file in names if os.path.isfile(file))
