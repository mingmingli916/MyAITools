from keras.preprocessing import image


class SimpleImageLoader:
    def __init__(self, dtype):
        self.dtype = dtype

    def load_image(self, path, *args, **kwargs):
        return list([image.img_to_array(image.load_img(p, *args, **kwargs)).astype(self.dtype) for p in path])

