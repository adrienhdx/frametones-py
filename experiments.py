import cv2 #pip install opencv-python
import numpy as np
import matplotlib.pyplot as plt
import vicosis_utils as vcs
import extcolors
import time
import os
import vicosis_utils as utils
import colorsys

path = r"C:\Users\adrhd\Documents\GitHub\vicosis\output_sorted.jpg"
img = cv2.imread(path)

palette = vcs.fx_strip(img, 10)
print(palette)

