import cv2 #pip install opencv-python
import numpy as np

# find the average color of the image :
# 1. convert the image to HSV
# 2. find the average color of the image
# 3. convert the average color to RGB
# 4. return the average color
def average_color_RGB2HSV2RGB(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    avg_h = np.average(h)
    avg_s = np.average(s)
    avg_v = np.average(v)
    _avg_color_hsv = np.uint8([[[avg_h, avg_s, avg_v]]])
    _avg_color_rgb = cv2.cvtColor(_avg_color_hsv, cv2.COLOR_HSV2BGR)
    return _avg_color_rgb[0][0]

src = cv2.imread(r"C:\Users\adrhd\OneDrive - INSA Lyon\2A\Info\Projet S4\blueblue.jpeg")
avg_color = average_color_RGB2HSV2RGB(src)

print("Average Color : ", avg_color)

# show the average color as a 450x450 pixel image
color = np.zeros((450, 450, 3), np.uint8)
color[:] = (avg_color[0], avg_color[1], avg_color[2])
cv2.imshow("Average Color", color)

cv2.waitKey(0)



