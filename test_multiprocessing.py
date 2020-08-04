import numpy as np
import os
from sklearn.model_selection import train_test_split
from PIL import Image
import concurrent.futures
import time
start = time.perf_counter()
root_dir = "data"

def process_image(images, folder):
    # image_name = args[0]
    # folder = args[1]
    total_x = []
    total_y = []
    for a in range(len(images)):
        image_name = images[a]
        i = sorted(os.listdir(root_dir)).index(folder)
        img = Image.open(os.path.join(root_dir, folder, image_name))
        img = img.resize((224, 224))
        img = np.array(img)
        new_img = np.zeros((224, 224, 3))
        for j in range(len(img)):
            for k in range(len(img[0])):
                new_img[j][k] = np.array((img[j][k], img[j][k], img[j][k]))
        total_x.append(new_img)
        total_y.append(i)
    # print(image_name)
    return total_x, total_y

    # total_x.append(new_img)
    # total_y.append(i)

if __name__ == '__main__':
    root_dir = "data"
    folders = os.listdir(root_dir)

    total_x = []
    total_y = []

    for i in range(len(folders)):
        folder = folders[i]
        images = os.listdir(os.path.join(root_dir, folder))[:300]
        # arguments = [[images[i], folder] for i in range(len(images))]

        processes = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # result = executor.map(process_image, [images], [folder]*len(images))
            # result = executor.map(process_image, arguments)
            future1 = executor.submit(process_image, images, folder)
        val1 = future1.result()
        total_x += val1[0]
        total_y += val1[1]
            # for res in result:
            #     print(res)
    total_x = np.array(total_x)
    total_y = np.array(total_y)
    from tensorflow.keras.utils import to_categorical
    total_y = to_categorical(total_y)

    train_x, test_x = train_test_split(total_x, test_size=0.25, shuffle=True, random_state=4)
    train_y, test_y = train_test_split(total_y, test_size=0.25, shuffle=True, random_state=4)

    np.save("numpy_arrays/train_x.npy", train_x)
    np.save("numpy_arrays/test_x.npy", test_x)
    np.save("numpy_arrays/train_y.npy", train_y)
    np.save("numpy_arrays/test_y.npy", test_y)
    print("Time:", time.perf_counter() - start, "seconds")
    # 519.2204812 seconds
    print(train_x.shape)
    print(train_y.shape)
    print(train_y)
    print(test_y)