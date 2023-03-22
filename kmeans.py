import cv2 #pip install opencv-python
import numpy as np
import os
import vicosis_utils as utils
import time

video_path = r"C:\Users\adrhd\Videos\Captures\blade_runner_2049.mp4"
out_path = r'C:\Users\adrhd\Documents\GitHub\vicosis'

filename = os.path.splitext(os.path.basename(video_path))[0] # get filename without extension for saving the image file

start = time.time()

nb_frames = 1500 # 1000 frames per hour is satisfactory
height = 128 #nb_frames // 10 # 10 frames per pixel
K=7
# load video as a cv2 object
cap = cv2.VideoCapture(video_path)

output_image = utils.process_kmeans(source=cap, frame_count=nb_frames, output_height=height, color_count=K, logging=True, high_res=True)

os.chdir(out_path)

cv2.imwrite(f"K_{K}_{filename}_{start-time.time()}.jpg", output_image)
# K_filename_time.jpg
         