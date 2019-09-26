import matplotlib.pyplot as plt
import numpy as np


def plot_loss_acc(H):
    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    X = np.arange(0, len(H.history['loss']))
    plt.plot(X, H.history["loss"], label="train_loss")
    plt.plot(X, H.history["val_loss"], label="val_loss")
    plt.plot(X, H.history["acc"], label="train_acc")
    plt.plot(X, H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.show()


def save_loss_acc(H, sava_path):
    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    X = np.arange(0, len(H.history['loss']))
    plt.plot(X, H.history["loss"], label="train_loss")
    plt.plot(X, H.history["val_loss"], label="val_loss")
    plt.plot(X, H.history["acc"], label="train_acc")
    plt.plot(X, H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig(sava_path)
    plt.close()
