from deprecated import deprecated


class list1(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.heap_size = len(self)

    def __getitem__(self, item):
        return super().__getitem__(item - 1)

    def __setitem__(self, key, value):
        super().__setitem__(key - 1, value)



@deprecated(reason='use ArrayFromOne instead.')
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


@deprecated(reason='use list1 instead')
class ArrayFromOne(list):
    def __getitem__(self, item):
        return super().__getitem__(item - 1)

    def __setitem__(self, key, value):
        super().__setitem__(key - 1, value)


if __name__ == '__main__':
    a = [1, 2, 3]
    lst = list1('abc')
    print(lst)
    print(lst.heap_size)
