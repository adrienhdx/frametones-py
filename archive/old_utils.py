# Unused

import extcolors
import numpy as np
import cv2
import time
import colorsys
import fast_colorthief as thief
import matplotlib.pyplot as plt


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
    print(f"Frame step: {frame_step}")

    for i in range(0, all_film_frames, frame_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        frames.append(frame)
        print(f"Loaded frame {i+1}/{all_film_frames}")
    
    """ Load the first nb_frames frames instead (super fast)
    for i in range(nb_frames):
        ret, frame = cap.read()
        frames.append(frame)"""
    
    return frames

def load_frame(video_path, frame_number):
    """UNUSED - return a frame from a video

    Args:
        video_path (string): path to the video
        frame_number (int): number of the frame to load

    Returns:
        np.array: frame as np.array
    """
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    return frame


def plot_histogram(frame):  
    for i, col in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
        plt.plot(hist, color = col)
        plt.xlim([0,256])
    plt.show()

def palette_strip_priority(image_path, no_colors=7):

    # returns a 100x1 strip with the most important colors of the image
    # the height of each color is proportional to its importance
    # the colors are sorted from the most important to the least important
    #TODO: image needs to be either loaded from PIL or read from disk. First one requires pillow which I don't want to use
    # since we're already using opencv. Second one is slow af.
    # So it's either I rewrite all the functions to use PIL or I find a way to read the image from disk without using cv2.imread, 
    # or I tweak the extcolors library to use cv2 instead of pillow, if that's possible
    # Since I probably will end up writing my own extcolors library, I'll just leave it like that for now
    #TODO: make it faster (ie find optimal tolerance, compress image, etc.)
    # Latest benchmark on celeste.webm : 1336s (22min) for 500 frames (0.37 fps) so it's a total shitshow
    # CPU usage is moderate (35%), I guess the bottleneck is the number of iterations
    #TODO: customize the height
    #TODO: sort the colors by hue not by importance
    # note : reducing the tolerance is faster, but also lessens the average importance of each color
    # potential solution would be some kind of multiplier

    colors, pixel_count = extcolors.extract_from_path(image_path, tolerance=10) # slow af but that's a start
    importance = []
    image_colors = []
    for i in range(len(colors)):
        importance.append(colors[i][1]/pixel_count)
        image_colors.append(colors[i][0])

    # get the first 7 colors (most important)
    importance = importance[:no_colors]
    image_colors = image_colors[:no_colors]
    # round the importance to int
    sum_importance = sum(importance)
    importance = [int((i*100)/sum_importance) for i in importance]
    
    output_image = np.zeros((100, 1, 3), np.uint8) # height x width x 3 (BGR)

    last_height = 0
    for i in range(len(image_colors)):
        height = importance[i]
        output_image[last_height:last_height+height, 0:10] = (image_colors[i][2], image_colors[i][1], image_colors[i][0])
        last_height += height

    # invert top and bottom 
    output_image = cv2.flip(output_image, 0)

    return output_image

def palette_strip_hue(image_path, no_colors=7):

    # current average speed : (tolerance=10, colors=7) 0.15 fps

    start = time.time()
    colors, pixel_count = thief.get_palette(image_path) # slow af but that's a start

    extraction_time = time.time()-start
    print(f"*    Extracted colors in {extraction_time:.02f} seconds")

    importance = []
    image_colors = []
    for i in range(len(colors)):
        importance.append(colors[i][1]/pixel_count)
        image_colors.append(colors[i][0])

    # get the first 7 colors (most important)
    importance = importance[:no_colors]
    image_colors = image_colors[:no_colors]
    # round the importance to int
    sum_importance = sum(importance)
    importance = [int(  (i*100) / sum_importance) for i in importance]

    rgb_colors = {}
    for i in range(len(image_colors)):
        rgb_colors[image_colors[i]] = importance[i]

    # sort colors by hue


    rgb_colors = {k: v for k, v in sorted(rgb_colors.items(), key=lambda item: colorsys.rgb_to_hsv(*item[0]))}
    sorted_time = time.time()-start-extraction_time
    print(f"*    Sorted colors in {sorted_time} seconds")

    output_image = np.zeros((100, 1, 3), np.uint8) # height x width x 3 (BGR)

    sorted_image_colors = list(rgb_colors.keys())

    last_height = 0
    for i in range(len(rgb_colors)):
        height = rgb_colors[sorted_image_colors[i]]
        output_image[last_height:last_height+height, 0] = (sorted_image_colors[i][2], sorted_image_colors[i][1], sorted_image_colors[i][0])
        last_height += height

    # invert top and bottom 
    output_image = cv2.flip(output_image, 0)

    output_time = time.time()-start-extraction_time-sorted_time
    print(f"*    Image created in {output_time} seconds")
    print(f"*    Total processing time : {extraction_time+sorted_time+output_time:.02f} seconds ({1/(extraction_time+sorted_time+output_time):.02f} fps)")

    return output_image


# generate X random integers so that their sum adds up to 100
# used in fx_strip
def generate_random_importance(nb_colors, max):
    random_importance = np.random.randint(0, max, nb_colors)
    random_importance = random_importance*max // random_importance.sum()
    return random_importance