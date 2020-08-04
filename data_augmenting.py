import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# def preprocessing_function(image):
#     image = np.array(image)
#     return image

dataAugmentation = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range = 10, zoom_range = 0.1,
fill_mode = "nearest", horizontal_flip = False,
width_shift_range = 0.2, height_shift_range = 0.1)

img = load_img("sample_input/03_1596461600.4818518.jpg")
x = img_to_array(img)
x = x.reshape((1,) + x.shape)
i = 0
for batch in dataAugmentation.flow(x, batch_size=1, save_to_dir="augmented", save_prefix=i, save_format="jpg"):
    i += 1
    if (i > 100):
        break