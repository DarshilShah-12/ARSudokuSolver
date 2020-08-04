import tensorflow as tf
from PIL import Image
import numpy as np
import cv2

model = tf.keras.models.load_model("vgg16_model")

test_image = Image.open("true_blank.png").resize((28, 28)).convert("L")
test_image_arr = np.asarray(test_image)
test_image_arr = cv2.bitwise_not(test_image_arr)
imageBatch = [test_image_arr/255]
print(type(imageBatch))
imageBatch = np.asarray(imageBatch)
imageBatch = imageBatch.reshape((imageBatch.shape[0], imageBatch.shape[1], imageBatch.shape[2], 1))
print(type(imageBatch))
# print(imageBatch)
print(imageBatch.shape)
output = model.predict(imageBatch)
print(output.shape)
print(output)
print(np.argmax(output[0]))