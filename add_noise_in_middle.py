import cv2
from PIL import Image
import numpy as np
import random

image = Image.open("true_blank.png").resize((28,28))
for _ in range(6000):
    test = np.zeros((28,28))
    for i in range(5, 23):
        for j in range(5, 23):
            test[i][j] = random.choice([0]*98 + [255]*2)
    dilation = cv2.dilate(test,(3,3),iterations = 1)
    # cv2.imshow("test2", dilation)
    # cv2.waitKey()
    cv2.imwrite("better_blank/better_blank_" + str(_) + ".png", dilation)