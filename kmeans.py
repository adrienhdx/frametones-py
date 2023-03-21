# TODO : trier par teinte
import colorsys
import numpy as np
import cv2 as cv
import time
img = cv.imread(r"C:\Users\adrhd\Pictures\bato\_MG_7493.JPG")

start = time.time()
# resize to 360p for faster processing
img = cv.resize(img, (480, 360))

Z = img.reshape((-1,3))
# convert to np.float32
Z = np.float32(Z)
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

labels, counts = np.unique(label, return_counts=True)

total_pixels = img.shape[0] * img.shape[1]
heights = np.uint8(counts * 100 / total_pixels)

# make strip
output_image = np.zeros((100, 10, 3), np.uint8) # hauteur x largeur x 3 (BGR)

mt = []
for i in range(K):
    mt.append(  ((center[i][0], center[i][1], center[i][2]), heights[i])    )

# sort mt by hue
mt = sorted(mt, key=lambda x: colorsys.rgb_to_hsv(x[0][0], x[0][1], x[0][2])[2], reverse=True)

last_height = 0
for i in range(K):
    height = mt[i][1]
    output_image[last_height:last_height+height, 0:10] = (mt[i][0][0], mt[i][0][1], mt[i][0][2])
    last_height+=height


cv.flip(output_image, 0)
cv.imwrite(r"C:\Users\adrhd\Documents\GitHub\vicosis\kmeans.jpg", output_image)
print(f"Done in {time.time()-start} seconds")