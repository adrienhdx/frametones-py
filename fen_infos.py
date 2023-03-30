from tkinter import *
from tkinter import ttk 

class Fen_infos() :
    def __init__(self) :
        #Initialisation de la fenêtre
        self.fen_infos = Tk()
        # Attributs esthétiques
        self.fen_infos.title('Informations du fichier chargé')
        self.fen_infos.geometry('248x275')
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

        self.var_date = StringVar()
        self.etiquette_date = ttk.Label(root, text = 'Année de sortie')
        self.etiquette_date.place(x = 22, y = 160)
        self.entree_date = ttk.Entry(root, width = 7, textvariable = self.var_date, font = 'Arial 13' )
        self.entree_date.place(x = 22, y = 180)


        # Listbox de choix du mode de traitement
        self.listbox_genre = Listbox(root, width = 60, font = 'Arial 13')
        self.liste_genre = [    "Action",    "Aventure",    "Animation",    "Biographie",    "Comédie",
                                "Crime",    "Documentaire",    "Drame",    "Famille",    "Fantastique",
                                "Film noir",    "Histoire",    "Horreur",    "Musique",    "Comédie musicale",
                                "Mystère",    "Romance",    "Science-fiction",    "Sport",    "Thriller",    "Guerre",    "Western"]
        self.listbox_genre.insert(0, "Choisir un genre")
        for i in range (len(self.liste_genre)) :
            texte = self.liste_genre[i]
            self.listbox_genre.insert(i+1, texte)
        self.listbox_genre.place(x = 70, y = 180)

        """# Bouton option charger imdb
        self.etiquette_imdb = ttk.Label(root, \
            text = "Vous pouvez directement charger les informations restantes du film avec l'option suivante si vous le souhaitez. \n"\
                + " Champ obligatoire : Titre du film") # autres champs obligatoires ?
        self.etiquette_imdb.place()
            
        self.bouton_imdb = ttk.Button(root, text = 'Option charger depuis IMdB', width = 120)
        self.bouton_imdb.bind('<Button-1>', self.charger_depuis_imdb)
        self.bouton_imdb.place(x = 22, y = 150)"""
           
app = Fen_infos()
