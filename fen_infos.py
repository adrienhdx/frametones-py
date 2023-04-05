
import tkinter as tk
from tkinter import *
from tkinter import ttk 


class Fen_infos() :
    def __init__(self) :
        #Initialisation de la fenêtre
        self.fen_infos = Tk()
        # Attributs esthétiques
        self.fen_infos.title('Informations du fichier chargé')
        self.fen_infos.geometry('235x575')
        self.fen_infos.configure(bg = 'white')
        # Lancement du gestionnaire d'évènement 
        self.creer_widgets(self.fen_infos)
        self.fen_infos.mainloop()

    def creer_widgets(self, root) :
        # Box contenant les zones d'entrées
        self.etiquette_infos_film = ttk.Label(root, text = 'Remplir les informations du film')
        self.etiquette_infos_film.place(x = 22, y = 20)

        self.var_titre = StringVar()
        self.etiquette_titre = ttk.Label(root, text = 'Titre du film')
        self.etiquette_titre.place(x = 22, y = 60)
        self.entree_titre = ttk.Entry(root, textvariable = self.var_titre, width = 20, font = 'Arial 13')
        self.entree_titre.place(x = 22, y = 80)

        self.var_real = StringVar()
        self.etiquette_real = ttk.Label(root, text = 'Nom du réalisateur ')
        self.etiquette_real.place(x = 22, y = 110)
        self.entree_real = ttk.Entry(root, textvariable = self.var_real, width = 20, font = 'Arial 13')
        self.entree_real.place(x = 22, y = 130)

        self.var_annee = StringVar()
        self.etiquette_annee = ttk.Label(root, text = 'Année de sortie')
        self.etiquette_annee.place(x = 22, y = 160)
        self.entree_annee = ttk.Entry(root, textvariable = self.var_annee, width = 10, font = 'Arial 13')
        self.entree_annee.place(x = 22, y = 180)

        # Listbox de choix du mode de traitement
        self.etiquette_genre = ttk.Label(root, text = 'Genre du film')
        self.etiquette_genre.place(x = 22, y = 210)
        self.scrollbar_genre = ttk.Scrollbar(root)
        self.listbox_genre = tk.Listbox(root, width = 20, font = 'Arial 13')
        self.liste_genre = ["Comédie", "Science-fiction", "Horreur", "Romance", "Action", "Thriller", "Drama", "Mystère", "Policier", "Animation", "Aventure", "Fantasy","Comédie-Romance", "Comédie-Action", "Super-héro"]
        for i in range (len(self.liste_genre)-1) :
            texte = self.liste_genre[i]
            self.listbox_genre.insert(i+1, texte)
        self.listbox_genre.place(x = 22, y = 240,)
        
        self.listbox_genre.config(yscrollcommand = self.scrollbar_genre.set)
        self.scrollbar_genre.place(x = 210, y = 240, height = 205)

        #Bouton option charger imdb
        self.etiquette_imdb = ttk.Label(root, \
            text = "Vous pouvez directement charger \n les informations restantes du film avec \n l'option suivante si vous le souhaitez. \n"\
                + " Champ obligatoire : Titre du film") # autres champs obligatoires ?
        self.etiquette_imdb.place(x = 14, y = 470)
            
        self.bouton_imdb = ttk.Button(root, text = 'Option charger depuis IMdB', width = 30)
        self.bouton_imdb.bind('<Button-1>', self.charger_depuis_imdb)
        self.bouton_imdb.place(x = 22, y = 535)

    def charger_depuis_imdb(self, event) :
        pass
           
app = Fen_infos()
