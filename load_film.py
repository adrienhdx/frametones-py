# creates an image with the average color of each frame of a video
# painfully slow (10s for 500 1920x1080 frames on my Ryzen 7 4700U)
# TODO benchmark on VD

# TODO new benchmark on compressed 480p30 video (e08_compressed.mp4)

import cv2 #pip install opencv-python
import numpy as np
import fca_utils as fca
import time

video_path = r"C:\Users\adrhd\Videos\The Last Of Us (2023) S1\The.Last.of.Us.S01E02.mkv"

start = time.time()
nb_frames = 500

output_image = fca.single_color_image(video_path, 100, nb_frames)

cv2.imwrite(f"average_color_{nb_frames}.png", output_image)

print(f"Done in {time.time() - start} seconds")


