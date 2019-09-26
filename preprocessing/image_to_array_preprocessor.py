from keras.preprocessing.image import img_to_array


# The benefit of defining a class to handle this type of image preprocessing rather than simply
# calling img_to_array on every single image is that we can now chain preprocessors together as
# we load datasets from disk.
class ImageToArrayPreprocessor:
    def __init__(self, data_format=None):
        self.data_format = data_format

    def preprocess(self, image):
        # apply the Keras utility function that correctly rearranges the dimensions of the image
        return img_to_array(image, data_format=self.data_format)
