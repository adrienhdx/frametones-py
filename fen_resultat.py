import tkinter as tk
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk 

class Fen_resultat() :
    def __init__(self,width_im,height_im,titre) :
        #Initialisation de la fenêtre
        self.fen_resultat = tk.Tk()
        # Attributs esthétiques
        self.fen_resultat.title('Résultat de votre traitement')
        self.fen_resultat.geometry('1000x700')
        self.fen_resultat.configure(bg = 'white')
        # Lancement du gestionnaire d'évènement 
        self.creer_widgets(self.fen_resultat)
        self.fen_resultat.mainloop()

    def creer_widgets(self, root, width_im, height_im, titre) :
        self.nom_image = ttk.Label(root, text = titre, font = 'Times New Roman 15')
        self.nom_image.place(x = 900, y = 40)
        self.canvas = tk.Canvas(root, bg = 'white', width = width_im, height = height_im)
        self.canvas.pack(side = tk.TOP)
        

    def coller_image_resultat(self, img, width_im,height_im) :
        imgtk = ImageTk.PhotoImage(img, master = Fen_resultat)
        id_image = self.canvas.create_image(width_im,height_im,anchor = tk.CENTER, image = imgtk)

app = Fen_resultat(800,400,"Amélie Poulain")