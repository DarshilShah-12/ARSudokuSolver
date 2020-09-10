import os
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2

def getPrediction():
    imageBatch = []
    root_dir = "save"
    testing = []
    for file in os.listdir(root_dir):
        image = Image.open(os.path.join(root_dir, file)).resize((224, 224)).convert("L")
        image = np.asarray(image)
        cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 3000:
                cv2.drawContours(image, [c], -1, 0, 10)
        image = cv2.dilate(image, (2, 2), iterations=1)
        image = Image.fromarray(np.uint8(image)).resize((224,224))
        image = np.asarray(image)
        for i in range(24):
            cv2.floodFill(image, None, (i, i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
            cv2.floodFill(image, None, (i, 223 - i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
            cv2.floodFill(image, None, (223 - i, i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
            cv2.floodFill(image, None, (223 - i, 223 - i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
            j = i
            if (image[j, j] != 0):
                while (image[j,j] != 0):
                    cv2.floodFill(image, None, (j, j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
                    j += 1
            j = i
            if (image[j, 223 - j] != 0):
                while (image[j, 223 - j] != 0):
                    cv2.floodFill(image, None, (j, 223 - j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
                    j += 1
            j = i
            if (image[223 - j, j] != 0):
                while (image[j, 223 - j] != 0):
                    cv2.floodFill(image, None, (223 - j, j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
                    j += 1
            j = i
            if (image[223 - j, 223 - j] != 0):
                while (image[223 - j, 223 - j] != 0):
                    cv2.floodFill(image, None, (223 - j, 223 - j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
                    j += 1
        cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 3000:
                cv2.drawContours(image, [c], -1, 0, 10)
        for i in [0, image.shape[0] - 13]:
            for j in range(image.shape[0]):
                for k in range(12):
                    cv2.floodFill(image, None, (i + k, j), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
                    cv2.floodFill(image, None, (j, i + k), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
        height, width = image.shape
        x, y, w, h = cv2.boundingRect(image)
        if (x == w or y == h):
            ROI = image[y:y + 1, x: x + 1]
        else:
            ROI = image[y:y + h, x:x + w]
        mask = np.zeros(image.shape, dtype=np.uint8)
        x = width // 2 - ROI.shape[1] // 2
        y = height // 2 - ROI.shape[0] // 2
        mask[y:y + h, x:x + w] = ROI
        image = mask
        cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 3000:
                cv2.drawContours(image, [c], -1, 0, 10)

        image = Image.fromarray(np.uint8(image)).resize((28,28))
        image = np.asarray(image)
        image = cv2.dilate(image, (3, 3), iterations=1)
        testing.append(image)
        imageBatch.append(image/255)


    imageBatch = np.array(imageBatch)
    imageBatch = imageBatch.reshape((imageBatch.shape[0], imageBatch.shape[1], imageBatch.shape[2], 1))
    # print(type(imageBatch))
    model = tf.keras.models.load_model("model")
    output = model.predict(imageBatch)
    print(output.shape)
    predicted = []
    for i in range(9):
        tmp = []
        for j in range(9):
            val = np.max(output[i*9 + j])
            if (val > 0.9):
                index = np.argmax(output[i*9 + j])
                if (index == 10):
                    # predicted.append(-1)
                    tmp.append(0)
                else:
                    # predicted.append(index)
                    tmp.append(index)
            else:
                # predicted.append(-1)
                tmp.append(0)
        predicted.append(tmp)
    return predicted