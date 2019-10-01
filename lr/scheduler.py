import numpy as np


def step_decay(epoch):
    # initialize the base initial learning rate, drop factor, and epochs to drop every
    init_alpha = .01
    factor = .5
    drop_every = 5

    # compute learning rate for the current epoch
    alpha = init_alpha * (factor ** np.floor((1 + epoch) / drop_every))

    return alpha


def poly_decay(epoch):
    max_epochs = 100
    base_lr = 1e-1
    power = 1.0  # linear rate decay

    # compute the new learning rate based on polynomial decay
    alpha = base_lr * (1 - (epoch / float(max_epochs))) ** power

    return alpha
