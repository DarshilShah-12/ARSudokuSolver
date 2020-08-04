import numpy as np
import os
from sklearn.model_selection import train_test_split
from PIL import Image
import tensorflow as tf
import time

start = time.perf_counter()

total_x = []
total_y = []

root_dir = "data"
folders = os.listdir(root_dir)

for i in range(len(folders)):
    folder = folders[i]
    images = os.listdir(os.path.join(root_dir, folder))[:400]

    for image_name in images:
        img = Image.open(os.path.join(root_dir, folder, image_name)).convert("L")
        img = img.resize((224, 224))
        img = np.array(img)
        new_img = np.zeros((224, 224, 3))
        for j in range(len(img)):
            for k in range(len(img[0])):
                new_img[j][k] = np.array((img[j][k], img[j][k], img[j][k]))
        print(image_name)
        total_x.append(new_img)
        total_y.append(i)

total_x = np.array(total_x)
total_y = np.array(total_y)
total_y = tf.keras.utils.to_categorical(total_y)

train_x, test_x = train_test_split(total_x, test_size=0.25, shuffle=True, random_state=4)
train_y, test_y = train_test_split(total_y, test_size=0.25, shuffle=True, random_state=4)

np.save("numpy_arrays/train_x.npy", train_x)
np.save("numpy_arrays/test_x.npy", test_x)
np.save("numpy_arrays/train_y.npy", train_y)
np.save("numpy_arrays/test_y.npy", test_y)

print("Time:", time.perf_counter() - start, "seconds")

print(train_x.shape)
print(train_y.shape)
print(train_y)
print(test_y)