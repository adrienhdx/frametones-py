### RangeSlider

'''
from tkinter import *
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV

root = Tk()
root.geometry("600x600")

hVar1 = IntVar() # left handle variable
hVar2 = IntVar()  # right handle variable

rs1 = RangeSliderH(root, [hVar1, hVar2], Width=230, Height=55, padX=17, min_val=0, max_val=5, font_size=12,\
     line_s_color='black',line_color='black', bar_color_inner='black')

rs1.place(x=150, y=420)
 
root.mainloop()
'''

### Ouvrir explorateur de fichier
from tkinter import *
from tkinter import filedialog

def browseFiles():
    filename = filedialog.askopenfilename(title = "Choisir un fichier", filetypes = (("Video files", "*.mp4"), ("all files", "*.*")))
    print(filename)

window = Tk()
window.title('Explorateur de fichier')
window.geometry("500x500")
window.config(background = "white")

button_explore = Button(window, text = "Séléctionner Fichier", command = browseFiles)
button_explore.grid(column = 1, row = 2)

window.mainloop()