# experimentation on extracting colors from images

import cv2 #pip install opencv-python
import numpy as np
import os
import vicosis_utils as utils
import time

video_path = r"C:\Users\adrhd\Videos\Captures\acid_interstate.mp4"
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis'

filename = os.path.splitext(os.path.basename(video_path))[0] # get filename without extension for saving the image file

start = time.time()

nb_frames = 500 # 1000 frames per hour is satisfactory
height = 128 #nb_frames // 10 # 10 frames per pixel

# load video as a cv2 object
cap = cv2.VideoCapture(video_path)
all_film_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_step = all_film_frames // nb_frames

output_image = np.zeros((height, nb_frames, 3), np.uint8) # height x width x 3 (BGR)

for i in range(nb_frames):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_step * i)                # set the frame to load
    ret, frame = cap.read()                                         # get the frame ndarray
    output_image[:, i] = utils.kmeans_strip(frame,color_count=7, strip_height=height)[:, 0]    # get the average color of the frame and put it in the output image
    print(f"Frame {i+1}/{nb_frames} done")

# crop the image at the top to remove the rounding errors black lines
output_image = output_image[4:, :, :]

os.chdir(out_path)


cv2.imwrite(f"FX_{filename}_{nb_frames}_{time.time() - start:.2f}.jpg", output_image)
# filename_nbframes_time.jpg

print(f"Done in {time.time() - start:.2f} seconds")
print(f"FPS: {nb_frames / (time.time() - start):.2f}")              

# 100% CPU, 2-6FPS dep. resolution and color count
# 50% GPU mem. 