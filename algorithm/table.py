import numpy as np


class Table:
    def __init__(self, x_len, y_len, x_shift=1, y_shift=1, dtype='int'):
        """

        :param x_len:
        :param y_len:
        :param x_shift:
        :param y_shift:
        :param dtype:
        """
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.table = np.zeros((x_len, y_len), dtype=dtype)

    def get(self, i, j):
        return self.table[i - self.x_shift][j - self.y_shift]

    def set(self, i, j, value):
        self.table[i - self.x_shift][j - self.y_shift] = value

    def __str__(self):
        return str(self.table)
