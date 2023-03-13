import numpy as np
import cv2
import random
import colorsys
image = np.zeros((50, 200, 3), np.uint8)

colors = []
for i in range(200):
    colors.append(
        [random.randint(0, 255),
          random.randint(0, 255),
            random.randint(0, 255)])
    
for i in range(200):
    image[:, i:i+1] = (colors[i][2], colors[i][1], colors[i][0])


cv2.imwrite("output.jpg", image)
colors.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
for i in range(200):
    image[:, i:i+1] = (colors[i][2], colors[i][1], colors[i][0])
cv2.imwrite("output_sorted.jpg", image)