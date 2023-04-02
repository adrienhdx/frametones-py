import utils
import os
import cv2

input_folder = r"C:\Users\adrhd\Videos\Captures\queue"
output_folder = r"C:\Users\adrhd\Desktop"

settings = [300, 1500]
extensions = [".mp4", ".avi", ".mkv"]

for file in os.listdir(input_folder):
    print(f"Processing {file}...")
    if os.path.splitext(file)[1] in extensions:
        nb_frames = settings[1]
        height = settings[0]
        K=7
        # load video as a cv2 object
        cap = cv2.VideoCapture(os.path.join(input_folder, file))
        output_image = utils.process_kmeans(source=cap, frame_count=nb_frames, output_height=height, color_count=K, high_res=True, end_credits=14400)
        cv2.imwrite(os.path.join(output_folder, f"{file}.jpg"), output_image)

print('DONE')
