# creates an image combining 1px stripes of the average color of each frame from a video
# painfully slow (10s for 500 1920x1080 frames on my Ryzen 7 4700U)
# actually, it's not that slow, but it's not fast either
# update : works a lot faster on compressed 360p or 480p video (obviously)
# although it is faster to run the script on uncompressed video instead
# of compressing 1080p via external software, then running.
# 1000 frames per hour is satisfactory
# output height as 1/10 of the length is satisfactory

import cv2 #pip install opencv-python
import numpy as np
import vicosis_utils as vcs
import time

#video_path = r"C:\Users\adrhd\Documents\GitHub\vicosis\videoplayback.mp4"
video_path = r"C:\Users\adrhd\Videos\Captures\celeste.mp4"

start = time.time()
nb_frames = 1000
output_height = 100

output_image = vcs.single_color_image(video_path, output_height, nb_frames)

cv2.imwrite(f"average_color_{nb_frames}.png", output_image)

print(f"Done in {time.time() - start} seconds")


