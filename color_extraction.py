# experimentation on extracting colors from images

import cv2 #pip install opencv-python
import numpy as np
import os
import fast_colorthief as ct
import vicosis_utils as utils
import colorsys
import cv2
import time

#video_path = r"C:\Users\adrhd\Documents\GitHub\vicosis\videoplayback.mp4"
video_path = r"C:\Users\adrhd\Videos\e08_compressed.mp4"
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis\images'

filename = os.path.splitext(os.path.basename(video_path))[0]

start = time.time()

nb_frames = 1500 # most important, 1000 frames per hour is satisfactory

frames = utils.load_video(video_path, nb_frames) 

output_image = np.zeros((100, nb_frames, 3), np.uint8) # hauteur x largeur x 3 (BGR)
for i in range(nb_frames):
    output_image[:, i] = utils.fx_strip(frames[i])[:, 0]
    print(f"Frame {i+1}/{nb_frames} done")

os.chdir(out_path)

cv2.imwrite(f"FX_{filename}_{nb_frames}_{time.time() - start:.2f}.jpg", output_image)
# filename_nbframes_time.jpg

print(f"Done in {time.time() - start:.2f} seconds")