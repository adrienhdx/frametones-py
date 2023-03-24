#Axelle et Albane bande de bgggggggggggggggggggggg

import tkinter as tk
from tkinter import filedialog
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV 

class Fenetre() :
    def __init__(self) :
        # Initialisation de la fenêtre racine
        self.racine = tk.Tk()
        # Attributs esthétiques de la fenêtre
        self.racine.title('Menu principal')
        self.racine.geometry('720x480')
        # Lancement de la boucle événementielle 
        
        # Initialisation des attributs de la classe

        # Lancement des fonctions
        self.creer_widgets(self.racine)
        self.racine.mainloop()

    def creer_widgets(self, root) :
        self.bouton_charger_fichier = tk.Button(root, text = 'Sélectionner fichier')
        self.bouton_charger_fichier.bind('<Button-1>', self.charger_fichier)
        self.bouton_charger_fichier.pack(side = tk.TOP)

        self.listbox_mode_de_traitement = tk.Listbox(root)
        self.listbox_mode_de_traitement.insert(1, "Couleur moyenne par image - bandes")
        self.listbox_mode_de_traitement.insert(2, "Couleur moyenne par image - circulaire")
        self.listbox_mode_de_traitement.insert(3, "Couleurs par clusters")
        self.listbox_mode_de_traitement.pack(side = tk.TOP)

        TpsMin = tk.IntVar() # left handle variable
        TpsMax = tk.IntVar()  # right handle variable
        rs1 = RangeSliderH(root, [TpsMin, TpsMax], Width=230, Height=55, padX=17, min_val=0, max_val=5, font_size=12,\
            line_s_color='black',line_color='black', bar_color_inner='black')
        rs1.place(x=150, y=420)

        # à faire apparaître uniquement pour le k_means
        self.var_qualité = tk.DoubleVar()
        self.curseur_qualité = tk.Scale(root, orient = 'horizontal', variable = self.var_qualité)
        self.curseur_qualité.pack(side = tk.TOP)

        self.bouton_lancer = tk.Button(root, text = 'Lancer le traitement')
        self.bouton_lancer.bind('<Button-1>', self.lancer_traitement)
        self.bouton_lancer.pack(side = tk.BOTTOM)


        # Construction de la fenêtre infos
        self.fen_infos = tk.Toplevel(root)
        self.fen_infos.title('Informations fichier')
        self.fen_infos.geometry('300x200')
        self.fen_infos.mainloop()

        self.var_titre = tk.StringVar()
        self.fen_infos.etiquette_titre = tk.Label(self.fen_infos, text = 'Titre du film')
        self.fen_infos_etiquette_titre.pack(anchor = tk.W)
        self.fen_infos.entree_titre = tk.Entry(self.fen_infos, textvariable = self.var_titre )
        self.fen_infos.entree_titre.pack()

        self.var_genre = tk.StringVar()
        self.fen_infos.etiquette_genre = tk.Label(self.fen_infos, text = 'Genre du film')
        self.fen_infos_etiquette_genre.pack(anchor = tk.W)
        self.fen_infos.entree_genre = tk.Entry(self.fen_infos, textvariable = self.var_genre )
        self.fen_infos.entree_genre.pack()

        self.var_date = tk.StringVar()
        self.fen_infos.etiquette_date = tk.Label(self.fen_infos, text = 'Date du film')
        self.fen_infos_etiquette_date.pack(anchor = tk.W)
        self.fen_infos.entree_date = tk.Entry(self.fen_infos, textvariable = self.var_date )
        self.fen_infos.entree_date.pack()

        self.var_real = tk.StringVar()
        self.fen_infos.etiquette_real = tk.Label(self.fen_infos, text = 'Réalisateur du film')
        self.fen_infos_etiquette_real.pack(anchor = tk.W)
        self.fen_infos.entree_real = tk.Entry(self.fen_infos, textvariable = self.var_real )
        self.fen_infos.entree_real.pack()

        self.fen_infos.bouton_imdb = tk.Button(self.fen_infos, text = 'Option charger depuis IMdB')
        self.fen_infos.bouton_imdb.bind('<Button-1>', self.charger_depuis_imdb)
        self.fen_infos.bouton_imdb.pack()

        # ajouter étiquettes qui disent quel champ est obligatoire (é def) 
        # + expliquer à l'utilisateur ce que fait l'option imdb 
        



        
    def charger_fichier(self, event) :
        pass
    def lancer_traitement(self, event) :
        pass
    def charger_depuis_imdb(self, event) :
        pass

app = Fenetre()

