import os
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
imageBatch = []
root_dir = "sample_input"
import cv2
testing = []
for file in os.listdir(root_dir):
    image = Image.open(os.path.join(root_dir, file)).resize((224, 224)).convert("L")
    # plt.imshow(image)
    # plt.show()
    image = np.asarray(image)
    # Filter using contour area and remove small noise
    image = image[30:210, 24:200] # UNCOMMENT # image = image[23:199, 23:199] # UNCOMMENT
    cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 2500:
            cv2.drawContours(image, [c], -1, 0, 10)
    image = Image.fromarray(np.uint8(image)).resize((224,224))
    image = np.asarray(image)
    # for i in range(24):
        # cv2.floodFill(image, None, (i, i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
        # cv2.floodFill(image, None, (i, 223 - i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
        # cv2.floodFill(image, None, (223 - i, i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
        # cv2.floodFill(image, None, (223 - i, 223 - i), 0, loDiff=(5, 5, 5, 5), upDiff=(2, 2, 2, 2))
        # j = i
        # if (image[j, j] != 0):
        #     while (image[j,j] != 0):
        #         cv2.floodFill(image, None, (j, j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
        #         j += 1
        # j = i
        # if (image[j, 223 - j] != 0):
        #     while (image[j, 223 - j] != 0):
        #         cv2.floodFill(image, None, (j, 223 - j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
        #         j += 1
        # j = i
        # if (image[223 - j, j] != 0):
        #     while (image[j, 223 - j] != 0):
        #         cv2.floodFill(image, None, (223 - j, j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
        #         j += 1
        # j = i
        # if (image[223 - j, 223 - j] != 0):
        #     while (image[223 - j, 223 - j] != 0):
        #         cv2.floodFill(image, None, (223 - j, 223 - j), 0, loDiff=(20, 20, 20, 20), upDiff=(20, 20, 20, 20))
        #         j += 1
    # cv2.imshow("frame", image)
    # cv2.waitKey()
    height, width = image.shape
    # x, y, w, h = cv2.boundingRect(image)
    x, y, w, h = 60, 24, 125, 190
    # cv2.imshow("test", image[y: y + h, x: x + w])
    # cv2.waitKey()
    # Create new blank image and shift ROI to new coordinates
    mask = np.zeros(image.shape, dtype=np.uint8)
    ROI = image[y:y + h, x:x + w]
    # cv2.imshow("frame", ROI)
    # cv2.waitKey()
    # x = width // 2 - ROI.shape[1] // 2
    # y = height // 2 - ROI.shape[0] // 2
    x = int(width / 2 - ROI.shape[1] / 2)
    y = int(height / 2 - ROI.shape[0] / 2) - 10
    # if (mask[y:y + h, x:x + w].shape != ROI.shape):
    #     # print(image.shape)
    #     # print(type(image))
    #     # cv2.imshow("frame", image)
    #     # cv2.waitKey()
    #     # mask[y: y + h, x: x + w] = ROI[y:y + h, x:x + w]
    #     while (mask[y:y + h, x:x + w].shape[0] < ROI.shape[0]):
    #         ROI = ROI[:-1, :]
    #     while (mask[y:y + h, x:x + w].shape[1] < ROI.shape[1]):
    #         ROI = ROI[:, :-1]
    # else:
    mask[y:y + h, x:x + w] = ROI
    image = mask
    cnts = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 3000:
            cv2.drawContours(image, [c], -1, 0, 10)
    # cv2.imshow('ROI', ROI)
    # cv2.imshow('mask', mask)
    # cv2.imshow("image", image)
    # cv2.waitKey()

    # new_img = np.zeros((224, 224, 3))
    # for j in range(len(image)):
    #     for k in range(len(image[0])):
    #         new_img[j][k] = np.array((image[j][k], image[j][k], image[j][k]))
    # new_img = Image.fromarray(np.uint8(new_img))
    # new_img.resize((28,28))
    # new_img = np.asarray(new_img)
    # imageBatch.append(new_img)
    image = Image.fromarray(np.uint8(image)).resize((28,28))
    image = np.asarray(image)
    # image = cv2.erode(image,(2,2),iterations = 2)
    image = cv2.dilate(image, (2, 2), iterations=1)
    testing.append(image)
    # imageBatch.append(image.flatten()/255)
    imageBatch.append(image/255)
imageBatch = np.array(imageBatch)
imageBatch = imageBatch.reshape((imageBatch.shape[0], imageBatch.shape[1], imageBatch.shape[2], 1))
print(type(imageBatch))
model = tf.keras.models.load_model("vgg16_model")
output = model.predict(imageBatch)
print(output.shape)
for i in range(len(output)):
    print(np.argmax(output[i]))
    print(output[i])
    # image = imageBatch[i]
    # image = Image.fromarray(np.uint8(image)).convert("L")
    # image = np.asarray(image)
    # print(type(image))
    # cv2.imshow("testing", testing[i])
    # cv2.waitKey()
predicted = []
for i in range(len(output)):
    val = np.max(output[i])
    if (val > 0.5):
        index = np.argmax(output[i])
        if (index == 10):
            predicted.append(-1)
        else:
            predicted.append(index)
    else:
        predicted.append(-1)
# predicted = [np.argmax(scores) - 1 for scores in output]
row1 = [-1, -1, -1, 8, -1, 1, -1, -1, -1]
row2 = [-1, -1, -1, -1, -1, -1, 4, 3, -1]
row3 = [5, -1, -1, -1, -1, -1, -1, -1, -1]
row4 = [-1, -1, -1, -1, 7, -1, 8, -1, -1,]
row5 = [-1, -1, -1, -1, -1, -1, 1, -1, -1]
row6 = [-1, 2, -1, -1, 3, -1, -1, -1, -1]
row7 = [6, -1, -1, -1, -1, -1, -1, 7, 5]
row8 = [-1, -1, 3, 4, -1, -1, -1, -1, -1]
row9 = [-1, -1, -1, 2, -1, -1, 6, -1, -1]

expected = row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9

score = 0
for i in range(len(predicted)):
    if (predicted[i] == expected[i]):
        score += 1
    else:
        # print(expected[i])
        print(predicted[i])
        print(expected[i])
        print(output[i])
        cv2.imshow("frame", testing[i])
        cv2.waitKey()
print("Score:", score)