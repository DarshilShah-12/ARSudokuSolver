from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

image = Image.open("blank.png").convert("L")
image = np.asarray(image)
row, col = (200, 200)
mean = 20
var = 0.5
sigma = var ** 0.5
for i in range(1016):
    row, col = image.shape
    s_vs_p = 0.5
    amount = 0.05
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
    out[coords] = 1

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
    out[coords] = 0
    # print(image.shape)
    # print(gauss.shape)
    # print(noisy.shape)
    # noisy = Image.fromarray(noisy).convert("L")
    # if (noisy == image):
    #     print("True")
    # else:
    #     print(image - noisy)
    # image = Image.fromarray(image)
    # plt.imshow(image)
    # plt.show()
    # plt.imshow(noisy)
    # plt.show()
    out = Image.fromarray(out).convert("L")
    out.save("data/Sample000/blank_" + str(i) + ".png")