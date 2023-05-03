import tkinter as tk
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk 

class Fen_resultat() :
    def __init__(self,width_im,height_im,titre) :
        #Initialisation de la fenêtre
        self.fen_resultat = tk.Toplevel()
        # Attributs esthétiques
        self.fen_resultat.title('Résultat de votre traitement')
        self.fen_resultat.geometry('1000x700')
        self.fen_resultat.configure(bg = 'white')
        # initialisation attributs de la classe : 
        self.width_im = width_im
        self.height_im = height_im 
        self.titre = titre 
        # lancement des widgets
        self.creer_widgets(self.fen_resultat)
        # Lancement du gestionnaire d'évènement 
        self.fen_resultat.mainloop()

    def creer_widgets(self, root) :
        self.nom_image = ttk.Label(root, text = self.titre, font = 'Arial 15')
        self.nom_image.place(x = 400, y = 40)
        self.canvas = tk.Canvas(root, bg = 'lightblue', width = self.width_im, height = self.height_im)
        self.canvas.pack(tk.BOTTOM)
        

    def coller_image_resultat(self, img) :
        imgtk = ImageTk.PhotoImage(img, master = Fen_resultat)
        id_image = self.canvas.create_image(self.width_im,self.height_im,anchor = tk.CENTER, image = imgtk)

app = Fen_resultat(800,400,"Amélie Poulain")