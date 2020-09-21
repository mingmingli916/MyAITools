import math
from chyson.algorithm.array import list1
from chyson.algorithm.utils import *
import sys
import copy


def parent(i):
    return math.floor(i / 2)


def left(i):
    return 2 * i


def right(i):
    return 2 * i + 1


class MaxPriorityQueue:
    def __init__(self):
        self.A = list1([])
        self.heap_size = len(self.A)
        # self.heapify()

    def max_heapify(self, i):
        l = left(i)
        r = right(i)

        # find the largest element
        if l <= self.heap_size and self.A[l].key > self.A[i].key:
            largest = l
        else:
            largest = i
        if r <= self.heap_size and self.A[r].key > self.A[largest].key:
            largest = r

        if largest != i:
            swap(self.A, i, largest)
            self.max_heapify(largest)

    def heapify(self):
        heap_size = self.heap_size
        for i in close_range(math.floor(heap_size / 2), 1):
            self.max_heapify(i)

    def maximum(self):
        return self.A[1]

    def increase_key(self, i, obj):
        if obj.key < self.A[i].key:
            raise Exception('new key is smaller than current key')
        self.A[i] = obj
        while i > 1 and self.A[parent(i)].key < self.A[i].key:
            swap(self.A, i, parent(i))
            i = parent(i)

    def insert(self, obj):
        self.heap_size = self.heap_size + 1
        oo = copy.deepcopy(obj)
        oo.key = -sys.maxsize
        if self.heap_size > len(self.A):
            self.A.append(oo)
        else:
            self.A[self.heap_size] = oo
        self.increase_key(self.heap_size, obj)

    def __str__(self):
        return str(self.A)

    def extract_max(self):
        if self.heap_size < 1:
            raise Exception('heap underflow')
        max = self.A[1]
        self.A[1] = self.A[self.heap_size]
        self.heap_size = self.heap_size - 1
        self.max_heapify(1)
        return max

    def __len__(self):
        return self.heap_size


class MinPriorityQueue:
    def __init__(self):
        self.A = list1([])
        self.heap_size = len(self.A)
        # self.heapify()

    def min_heapify(self, i):
        l = left(i)
        r = right(i)

        # find the smallest element
        if l <= self.heap_size and self.A[l].key < self.A[i].key:
            smallest = l
        else:
            smallest = i

        if r <= self.heap_size and self.A[r].key < self.A[smallest].key:
            smallest = r

        if smallest != i:
            swap(self.A, i, smallest)
            self.min_heapify(smallest)

    def heapify(self):
        heap_size = self.heap_size
        for i in close_range(math.floor(heap_size / 2), 1):
            self.min_heapify(i)

    def minimum(self):
        return self.A[1]

    def decrease_key(self, i, obj):
        # print('obj.key: {}; A[{}].key: {}'.format(obj.key, i, self.A[i].key))
        if obj.key > self.A[i].key:
            raise Exception('new key is larger than current key')
            # pass

        self.A[i] = obj
        while i > 1 and self.A[parent(i)].key > self.A[i].key:
            swap(self.A, i, parent(i))
            i = parent(i)

    def insert(self, obj):
        self.heap_size = self.heap_size + 1
        oo = copy.deepcopy(obj)
        oo.key = sys.maxsize  # sentinel
        if self.heap_size > len(self.A):
            self.A.append(oo)
        else:
            self.A[self.heap_size] = oo
        # print('heap_size: {}; object key: {}'.format(self.heap_size, obj.key))
        self.decrease_key(self.heap_size, obj)

    def __str__(self):
        return str(self.A)

    def extract_min(self):
        if self.heap_size < 1:
            raise Exception('heap underflow')
        min = self.A[1]
        self.A[1] = self.A[self.heap_size]
        self.heap_size = self.heap_size - 1
        self.min_heapify(1)
        return min

    def __len__(self):
        return self.heap_size


if __name__ == '__main__':
    class C:
        def __init__(self, key, character='a'):
            self.key = key
            self.character = character


    heap = MaxPriorityQueue()
    print(heap)
    lst = [1, 5, 2, 3, 6, 10, 7, 20, 15, 24]
    lc = []
    for i in lst:
        lc.append(C(i))
    for i in lc:
        heap.insert(i)
    print(heap)

    for i in range(len(lst)):
        print(heap.extract_max().key)

    heap = MinPriorityQueue()
    print(heap)
    lst = [1, 5, 2, 3, 6, 10, 7, 20, 15, 24]
    lc = []
    for i in lst:
        lc.append(C(i))
    for i in lc:
        heap.insert(i)
    print(heap)

    for i in range(len(lst)):
        print(heap.extract_min().key)
