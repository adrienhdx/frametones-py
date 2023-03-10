import numpy as np
import cv2

# Video Color Analysis (ViCoSIS) Utilities
# this file will hold all color analysis functions

#   TODO :
#   - color palette instead of average color (k-means clustering)
#   - GUI (tkinter)
#   - video compression (ffmpeg)


def average_frame_color(image_path):
    """return the average color of a given frame as np.uint8 array of size 3 (BGR)

    Args:
        image_path (string): path to the image

    Returns:
        np.uint8 array : BGR average color of the frame
    """
    #img = cv2.imread(image_path)

    hsv = cv2.cvtColor(image_path, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    avg_h = np.average(h)
    avg_s = np.average(s)
    avg_v = np.average(v)
    _avg_color_hsv = np.uint8([[[avg_h, avg_s, avg_v]]])
    _avg_color_rgb = cv2.cvtColor(_avg_color_hsv, cv2.COLOR_HSV2BGR)
    return _avg_color_rgb[0][0]

def load_video(video_path, nb_frames):
    """return a list of frames from a video

    Args:
        video_path (string): path to the video
        nb_frames (int): number of frames to load

    Returns:
        list: list of frames as np.array
    """
    cap = cv2.VideoCapture(video_path)
    frames = []

    all_film_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = all_film_frames // nb_frames
    

    for i in range(0, all_film_frames, frame_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        frames.append(frame)
        print(f"Loaded frame {i+1}/{all_film_frames}")
    
    """for i in range(nb_frames):
        ret, frame = cap.read()
        frames.append(frame)"""
    
    return frames


def single_color_image(video_path, output_height, nb_frames):
    """return an image with the average color of each frame of a video

    Args:
        video_path (string): path to the video
        output_height (int): height of the output image
        nb_frames (int): number of frames to load

    Returns:
        np.array: image with the average color of each frame of a video
    """
    frames = load_video(video_path, nb_frames)
    print(f"Loaded {len(frames)} frames")

    avg_colors = []
    for i in range(len(frames)):
        avg_color = average_frame_color(frames[i])
        avg_colors.append(avg_color)
        print(f"Processed frame {i+1}/{len(frames)}")

    output_image = np.zeros((output_height, len(avg_colors), 3), np.uint8) # hauteur x largeur x 3 (BGR)

    for i in range(len(avg_colors)):
        output_image[:, i] = (avg_colors[i][0], avg_colors[i][1], avg_colors[i][2])

    return output_image

# implement kmeans clustering to get a color palette instead of a single color
def color_palette_image(video_path, output_height, nb_frames):
    pass
