import numpy as np
import cv2 #pip install opencv-python
import matplotlib.pyplot as plt
import extcolors
import colorsys
import fast_colorthief as thief
import time
import os

# Video Color Analysis (ViCoSIS) Utilities
# this file will hold all color analysis functions as well as other practicalities

#   TODO :
#   - color palette extraction with priority to the most dominant colors and not bullshit random heights
#   - GUI (tkinter)
#
#   36 FPS using fx_strip

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

def downsize(video_path, resolution=(640, 480), output_path=r"C:\Users\adrhd\Documents\GitHub\vicosis\video_outputs"):
    """return a video with a smaller resolution

    Args:
        video_path (string): path to the video
        resolution (tuple): new resolution (width, height)

    Returns:
        np.array: video with a smaller resolution
    """
    filename = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    width, height = resolution
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    os.chdir(output_path)
    out = cv2.VideoWriter(f'{filename}_compressed.mp4', fourcc, 2, (width, height)) # 2 FPS

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.resize(frame, resolution, interpolation = cv2.INTER_AREA)
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def average_strip(video_path, output_height, nb_frames):
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
        output_image[:, i] = (avg_colors[i][2], avg_colors[i][1], avg_colors[i][0]) # check

    return output_image

def plot_histogram(frame):  
    for i, col in enumerate(['b', 'g', 'r']):
        hist = cv2.calcHist([frame], [i], None, [256], [0, 256])
        plt.plot(hist, color = col)
        plt.xlim([0,256])
    plt.show()

def rgb2hex(triple):
    return '#{:02x}{:02x}{:02x}'.format(triple[0], triple[1], triple[2])

# generate X random integers so that their sum adds up to 100
def generate_random_importance(nb_colors, max):
    random_importance = np.random.randint(0, max, nb_colors)
    random_importance = random_importance*max // random_importance.sum()
    return random_importance

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

"""
Pour ouvrir un dossier ou un fichier dans l'explorateur de fichier :
en gros pour charger le film depuis tkinter

from tkinter import filedialog
tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
folder_path = filedialog.askdirectory()
"""

def fx_strip(image, color_count=7, quality=1, height=100):
    # reshape to rgba
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

    palette = thief.get_palette(image, color_count=color_count, quality=quality) #OMG ITS SO FAST

    # hue sort 
    palette = sorted(palette, key=lambda x: colorsys.rgb_to_hsv(x[0], x[1], x[2])[0])

    output_image = np.zeros((height, 1, 3), np.uint8) # hauteur x largeur x 3 (BGR)

    heights = generate_random_importance(color_count, height)
    last_height = 0
    for i in range(len(palette)):
        height = heights[i]
        output_image[last_height:last_height+height, 0] = (palette[i][2], palette[i][1], palette[i][0])
        last_height+=height

    # invert top and bottom
    output_image = cv2.flip(output_image, 0)

    return output_image
