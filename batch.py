import utils
import os
import cv2

input_folder = r"C:\Users\adrhd\Videos\Captures\queue"
output_folder = r"C:\Users\adrhd\Desktop\images"

settings = [300, 1500]

mode = 0 #kmeans : 1, avg: 0

extensions = [".mp4", ".avi", ".mkv"]

for file in os.listdir(input_folder):
    print(f"Processing {file}...")
    if os.path.splitext(file)[1] in extensions:

        nb_frames = settings[1]
        height = settings[0]
        cap = cv2.VideoCapture(os.path.join(input_folder, file))

        if mode == 1:
            K=7
            output_image = utils.process_kmeans(source=cap, frame_count=nb_frames, output_height=height, color_count=K, high_res=True, end_credits=10000)
            cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(file)[0]}.png"), output_image)
        else:
            output_image = utils.process_avg(source=cap, frame_count=nb_frames, output_height=height, high_res=True, end_credits=10000)
            cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(file)[0]}.png"), output_image)


print('DONE')
