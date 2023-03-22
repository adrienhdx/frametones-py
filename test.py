import vicosis_utils as utils
import cv2
import numpy as np
import time

img_path = r"C:\Users\adrhd\Pictures\bato\_MG_7493.JPG"

img = cv2.imread(img_path)
start = time.time()
print(utils.average_frame_color_HSV(img))
m1_time = time.time() - start
print(f"Method 1 in {m1_time:.2f} seconds")
print(utils.average_frame_color_RGB(img))
m2_time = time.time() - start - m1_time
print(f"Method 2 in {m2_time:.2f} seconds")