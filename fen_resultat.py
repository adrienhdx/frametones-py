import tkinter as tk
from tkinter import *
from tkinter import ttk 
from PIL import Image 

class Fen_resultat() :
    def __init__(self) :
        #Initialisation de la fenêtre
        self.fen_resultat = Toplevel()
        # Attributs esthétiques
        self.fen_resultat.title('Résultat de votre traitement')
        self.fen_resultat.geometry('800x600')
        self.fen_resultat.configure(bg = 'white')
        # Lancement du gestionnaire d'évènement 
        self.creer_widgets(self.fen_resultat)
        self.fen_resultat.mainloop()
        # Initialisation des autres attributs
        #self.titre_film = ...

    def creer_widgets(self, root) :
        self.nom_image = ttk.Label(root, text = 'Amelie Poulain', font = 'Times New Roman 15')
        self.nom_image.place(x = 300, y = 40)
        self.canvas = tk.Canvas(root, bg = 'white', width = 750, height = 400)
        self.canvas.pack(side = tk.Toplevel)
        
    def coller_image_resultat(self) :
        pass
app = Fen_resultat