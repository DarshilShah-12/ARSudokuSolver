from keras.datasets import mnist
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import tensorflow as tf
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Flatten
from keras.layers import Reshape
from keras.layers import Activation
import os
from PIL import Image
import numpy as np
import cv2
import random

(X_train, y_train), (X_test, y_test) = mnist.load_data()
# cv2.imshow("test", X_train[0])
# cv2.waitKey()
blank_image_class = []
blank_label_class = []
folder = "better_blank"
for file in os.listdir(folder):
	image = Image.open(os.path.join(folder, file))
	image = np.asarray(image)
	blank_image_class.append(image)
	blank_label_class.append(10)
blank_image_class = np.array(blank_image_class)
blank_label_class = np.array(blank_label_class)
X_train = np.concatenate((X_train, blank_image_class[:3000]))
X_test = np.concatenate((X_test, blank_image_class[3000:]))
y_train = np.concatenate((y_train, blank_label_class[:3000]))
y_test = np.concatenate((y_test, blank_label_class[3000:]))

# random.Random(4).shuffle(X_train)
# random.Random(4).shuffle(X_test)
# random.Random(4).shuffle(y_train)
# random.Random(4).shuffle(y_test)


# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
# X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype('float32')
# X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype('float32')
# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]
# define baseline model
def baseline_model():
	# # create model
	model = Sequential()
	# model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
	# model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# # Compile model
	# model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=0.001, decay=0), metrics=['accuracy'])
	# return model
	model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(28,28,1)))
	model.add(BatchNormalization())
	model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
	model.add(BatchNormalization())
	model.add(Conv2D(128, kernel_size=(1, 1), activation='relu', padding='same'))

	model.add(Flatten())
	model.add(Dense(11))
	# model.add(Reshape((-1, 10)))
	model.add(Activation('softmax'))
	model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=0.0001, decay=0), metrics=['accuracy'])
	model.summary()
	return model
# build the model
model = baseline_model()
# Fit the model
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2], 1))

np.save("numpy_arrays/mnist/X_train.npy", X_train)
np.save("numpy_arrays/mnist/X_test.npy", X_test)
np.save("numpy_arrays/mnist/y_train.npy", y_train)
np.save("numpy_arrays/mnist/y_test.npy", y_test)

# model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=40, batch_size=200, verbose=2)
# # Final evaluation of the model
# scores = model.evaluate(X_test, y_test, verbose=0)
# print("Baseline Error: %.2f%%" % (100-scores[1]*100))
#
# model.save("vgg16_model")