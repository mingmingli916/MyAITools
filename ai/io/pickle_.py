import pickle


def save(model, filename):
    with open(filename, 'wb') as f:
        f.write(pickle.dumps(model))


def load(filename):
    with open(filename, 'rb') as f:
        return pickle.loads(f.read())
