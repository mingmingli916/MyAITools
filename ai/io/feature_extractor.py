import random

import numpy as np
import progressbar
from imutils import paths
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from sklearn.preprocessing import LabelEncoder

from .hdf5_dataset_writer import HDF5DatasetWriter
from ..messages import info
from ..utils import label_utils


class FeatureExtractor:
    def __init__(self, model, vector_length, target_size, batch_size=32, buffer_size=100):
        """

        :param model: model used to extract feature
        :param vector_length: the vector length extracted by the model
        :param target_size: the input image size to model
        :param batch_size: batch size to model
        :param buffer_size: buffer size during writing data into HDF5 file
        """
        self.model = model
        self.vector_length = vector_length
        self.target_size = target_size
        self.batch_size = batch_size,
        self.buffer_size = buffer_size

    def extract(self, dataset, output_path):
        # grab the list of images then randomly shuffle them to allow for easy
        # training and testing splits via array slicing during training time
        print(info.loading_image)
        image_paths = list(paths.list_images(dataset))

        # since we’ll be working with datasets too large to fit into memory, we won’t be
        # able to perform this shuffle in memory – therefore, we shuffle the image paths before
        # we extract the features.
        random.shuffle(image_paths)

        # extract the class labels from the image paths then encode the labels
        labels = label_utils.get_labels(image_paths)
        le = LabelEncoder()
        labels = le.fit_transform(labels)

        # initialize the HDF5 dataset writer, then store the class label names in the dataset
        dataset = HDF5DatasetWriter((len(image_paths), self.vector_length), output_path, data_key='features',
                                    buf_size=self.buffer_size)
        dataset.store_class_labels(le.classes_)

        # initialize the progress bar
        widgets = ['Extracting Features: ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ',
                   progressbar.ETA()]
        pbar = progressbar.ProgressBar(maxval=len(image_paths), widgets=widgets).start()

        for i in np.arange(0, len(image_paths), self.batch_size):  # similar to range(0, len(image_paths), bs)
            # extract the batch of images and labels, then initialize the list of actual images that
            # will be passed through the network for feature extraction
            batch_paths = image_paths[i:i + self.batch_size]
            batch_labels = labels[i:i + self.batch_size]
            batch_images = []

            # loop over the images and labels in the current batch
            for j, image_path in enumerate(batch_paths):
                image = load_img(image_path, target_size=self.target_size)
                image = img_to_array(image)

                # preprocess the image by (1) expanding the dimensions and
                # (2) subtracting the mean RGB pixel intensity from the
                # ImageNet dataset
                image = np.expand_dims(image, axis=0)
                image = imagenet_utils.preprocess_input(image)  # subtract mean
                batch_images.append(image)

            # pass the images through the network and use the output as our actual features
            batch_images = np.vstack(batch_images)
            features = self.model.predict(batch_images, batch_size=self.batch_size)

            # reshape the features so that each image is represented by
            # a flattened feature vector of the 'MaxPooling2D' output
            features = features.reshape(features.shape[0], self.vector_length)

            # add the features and labels to our HDF5 dataset
            #     raise TypeError("Can't broadcast %s -> %s" % (target_shape, self.mshape))
            # TypeError: Can't broadcast (96000,) -> (1024,)
            # I made the above bug because of I mistype batch_labels into labels
            dataset.add(features, batch_labels)
            pbar.update(i)

        dataset.close()
        pbar.finish()
