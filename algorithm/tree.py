def left_rotate(T, center, func):
    # local operation while maintaining the binary search tree property
    # http://chyson.net/notes/algorithm/introduction-to-algorithms/note.html#sec-4-4-2
    point = center.right  # set point

    # beta part in the fig
    center.right = point.left
    if point.left != T.nil:
        point.left.p = center

    # point part
    point.p = center.p

    if center.p == T.nil:
        T.root = point
    elif center == center.p.left:
        center.p.left = point
    else:
        center.p.right = point

    # center part
    point.left = center
    center.p = point

    # size attribute
    # point.size = center.size
    # center.size = center.left.size + center.right.size + 1
    func(center, point)


def right_rotate(T, center, func):
    # http://chyson.net/notes/algorithm/introduction-to-algorithms/note.html#sec-4-4-2
    point = center.left  # set point

    # beta part
    center.left = point.right
    if point.right != T.nil:
        point.right.p = center

    # point part
    point.p = center.p

    if center.p == T.nil:
        T.root = point
    elif center == center.p.left:
        center.p.left = point
    else:
        center.p.right = point

    # center part
    point.right = center
    center.p = point

    # point.size = center.size
    # center.size = center.left.size + center.right.size + 1
    func(center, point)


def func_size(center, point):
    point.size = center.size
    center.size = center.left.size + center.right.size + 1


def func_max(center, point):
    point.max_ = center.max_
    center.max_ = max(center.left.max_, center.right.max_, center.max_)


def insert_fixup(T, z, func):
    # the inserted node's color is red
    while z.p.color == 'red':
        if z.p == z.p.p.left:
            y = z.p.p.right  # save z.p.p.right
            # case 1: z.p is z.p.p's left child and
            # z.p.p's right child is 'red'
            if y.color == 'red':
                # change z.p.p's left and right child to black
                # change z.p.p to red and z.p.p is not z that
                # need to be fixed up
                z.p.color = 'black'
                y.color = 'black'
                z.p.p.color = 'red'
                z = z.p.p
            # case 2: z.p is z.p.p's right child and
            # z.p.p's right child is 'black' and z is right child
            # Note: the following else if part is prone to be implemented with error
            else:
                if z == z.p.right:
                    z = z.p
                    left_rotate(T, z, func)

                # case 3: z is left child
                z.p.color = 'black'
                z.p.p.color = 'red'
                right_rotate(T, z.p.p, func)
        else:
            y = z.p.p.left
            if y.color == 'red':
                z.p.color = 'black'
                y.color = 'black'
                z.p.p.color = 'red'
                z = z.p.p
            else:
                if z == z.p.left:
                    z = z.p
                    right_rotate(T, z, func)
                z.p.color = 'black'
                z.p.p.color = 'red'
                left_rotate(z.p.p, func)
    T.root.color = 'black'


def transplant(T, u, v):
    if u.p == T.nil:
        T.root = v
    elif u == u.p.left:
        u.p.left = v
    else:
        u.p.right = v
    v.p = u.p


def minimum(T, x):
    while x.left != T.nil:
        x = x.left
    return x


def maximum(T, x):
    while x.right != T.nil:
        x = x.right
    return x个


def successor(T, x):
    if x.right != T.nil:
        return minimum(x.right)

    y = x.p
    while y != T.nil and x == y.right:
        x = y
        y = y.p
    return y


def predecessor(T, x):
    if x.left != T.nil:
        return maximum(T, x.left)
    y = x.p
    while y != T.nil and x == y.left:
        x = y
        y = y.p
    return y
