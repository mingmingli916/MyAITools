def swap(lst, a, b):
    tmp = lst[a]
    lst[a] = lst[b]
    lst[b] = tmp


@DeprecationWarning
class A1:
    def __init__(self, A):
        self.A = A
        self._heap_size = len(A)

    def __getitem__(self, item):
        return self.A[item - 1]

    def __setitem__(self, key, value):
        self.A[key - 1] = value

    def __len__(self):
        return len(self.A)

    def __str__(self):
        return str(self.A)

    @property
    def heap_size(self):
        return self._heap_size

    @heap_size.setter
    def heap_size(self, value):
        self._heap_size = value

    def append(self, item):
        self.A.append(item)


class ArrayFromOne(list):
    def __getitem__(self, item):
        return super().__getitem__(item - 1)

    def __setitem__(self, key, value):
        super().__setitem__(key - 1, value)


def new_range(start, end, step=1):
    if end >= start:
        return range(start, end + 1, step)
    else:
        return range(start, end - 1, -step)
