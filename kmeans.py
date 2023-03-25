import cv2 #pip install opencv-python
import os
import vicosis_utils as utils
import time
from tkinter import filedialog

video_path = filedialog.askopenfilename(title = "Choisir un fichier", filetypes = (("Video files", "*.mp4"), ("all files", "*.*")))

filename = os.path.splitext(os.path.basename(video_path))[0] # get filename without extension for saving the image file

start = time.time()

# mandatory parameters
nb_frames = 1500 # 1000 frames per hour is satisfactory
height = 128 #nb_frames // 10 # 10 frames per pixel
K=7
# load video as a cv2 object
cap = cv2.VideoCapture(video_path)

output_image = utils.process_kmeans(source=cap, frame_count=nb_frames, output_height=height, color_count=K, high_res=True)

out_path = filedialog.askdirectory(title = "Choisir un dossier de destination", mustexist=True)
os.chdir(out_path)

cv2.imwrite(f"K_{K}_{filename}_{time.time() - start}.jpg", output_image)
# K_filename_time.jpg
         