def swap(lst, a, b):
    """
    Swap the position of a and b in the list.
    :param lst: the list containing a and b
    :param a: the index of a in the list
    :param b: the index of b in the list
    :return: list with a and b swapped
    """
    tmp = lst[a]
    lst[a] = lst[b]
    lst[b] = tmp


def close_range(start, end, step=1):
    if end >= start:
        return range(start, end + 1, step)
    else:
        return range(start, end - 1, -step)
