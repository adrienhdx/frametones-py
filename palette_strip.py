# creates a 100x1 strip with the most important colors of the image

import cv2 #pip install opencv-python
import numpy as np
import vicosis_utils as vcs
import time
import os

#video_path = r"C:\Users\adrhd\Documents\GitHub\vicosis\videoplayback.mp4"
video_path = r"C:\Users\adrhd\Videos\Captures\celeste-2.mp4"
palette_path = r'C:\Users\adrhd\Documents\GitHub\vicosis\palette strips'
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis\images'

filename = os.path.splitext(os.path.basename(video_path))[0]
os.chdir(palette_path)

start = time.time()

nb_frames = 15 # most important, 1000 frames per hour is satisfactory

frames = vcs.load_video(video_path, nb_frames) 

output_image = np.zeros((100, nb_frames, 3), np.uint8) # hauteur x largeur x 3 (BGR)
for i in range(nb_frames):
    print(f"Processing frame {i+1}/{nb_frames}")
    path = os.path.join(palette_path, f"frame{i}.jpg")
    cv2.imwrite(path, frames[i])
    output_image[:, i] = vcs.palette_strip_hue(path, 7)[:, 0]
    print(f"Frame {i+1}/{nb_frames} done")

os.chdir(out_path)

cv2.imwrite(f"strip_{filename}_{nb_frames}_{time.time() - start:.2f}.jpg", output_image)
# filename_nbframes_time.jpg

print(f"Done in {time.time() - start:.2f} seconds")


