import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img


def augment(image_path, save_to_dir, save_prefix='augmented', save_format='jpg', num=10,
            rotation_range=10,
            width_shift_range=.1,
            height_shift_range=.1,
            shear_range=.2,
            zoom_range=.2,  # [1-zoom_range, 1+zoom_range]
            horizontal_flip=True,
            fill_mode='nearest'):
    # load the input image, convert it to a numpy array,
    # and then reshape it to have an extra dimension
    print('[INFO] loading example image...')
    image = load_img(image_path)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # construct the image data generator for data augmentation
    # then initialize the total number of images generated thus far
    aug = ImageDataGenerator(rotation_range=rotation_range,
                             width_shift_range=width_shift_range,
                             height_shift_range=height_shift_range,
                             shear_range=shear_range,
                             zoom_range=zoom_range,  # [1-zoom_range, 1+zoom_range]
                             horizontal_flip=horizontal_flip,
                             fill_mode=fill_mode)

    total = 0
    # construct the actual Python generator
    print('[INFO] generating images...')
    image_gen = aug.flow(image,
                         batch_size=1,  # only one image
                         save_to_dir=save_to_dir,
                         save_prefix=save_prefix,
                         save_format=save_format)

    # loop over examples from our image data augmentation generator
    for image in image_gen:
        total += 1

        # if we have reached 10 examples, break from the loop
        if total == num:
            break
