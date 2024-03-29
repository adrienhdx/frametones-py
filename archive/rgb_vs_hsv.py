import utils
import cv2
import time

# just testing which technique is faster

img_path = r"C:\Users\adrhd\Pictures\bato\_MG_7493.JPG"

img = cv2.imread(img_path)
start = time.time()
print(utils.avg_strip_HSV(img))
m1_time = time.time() - start
print(f"Method 1 in {m1_time:.2f} seconds")
print(utils.avg_strip_RGB(img))
m2_time = time.time() - start - m1_time
print(f"Method 2 in {m2_time:.2f} seconds")