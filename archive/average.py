# creates an image combining 1px stripes of the average color of each frame from a video

import cv2 #pip install opencv-python
import numpy as np
import utils
import time
import os

#video_path = r"C:\Users\adrhd\Documents\GitHub\vicosis\videoplayback.mp4"
video_path = r"C:\Users\adrhd\Videos\Captures\max_leon.mkv"
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis'

filename = os.path.splitext(os.path.basename(video_path))[0]

start = time.time()

nb_frames = 1500 # most important, 1000 frames per hour is satisfactory

video = cv2.VideoCapture(video_path)

output_height = 128

output_image = utils.process_avg(source=video, frame_count=nb_frames, output_height=output_height, logging=True, high_res=True, end_credits=15000)

os.chdir(out_path)

cv2.imwrite(f"AVG_{filename}_{nb_frames}_{time.time() - start:.2f}.jpg", output_image)
# filename_nbframes_time.jpg

print(f"Done in {time.time() - start:.2f} seconds")


