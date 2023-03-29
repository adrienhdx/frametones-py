#Axelle et Albane... et Youssef et Adrien bande de bgggggggggggggggggggggg

import tkinter as tk
from tkinter import filedialog
from RangeSlider import RangeSliderH


# >> A faire : déterminer les placements et tailles des objets pour que ça soit propre
# >> Déterminer exactement ce qu'on met dans les 2 dernières fenêtres et la page web + comment ça s'implémente
# >> Rédiger les fonctions callback (lien avec backend)
# def les conditions de lancement des fenetres secondaires
# option imdb : quels sont les champs obligatoires ? comment récupérer base de données imdb ?

class Fenetre() :
    def __init__(self) :
        # Initialisation de la fenêtre racine
        self.racine = tk.Tk()
        # Attributs esthétiques de la fenêtre
        self.racine.title('Menu principal')
        self.racine.geometry('720x480')
        # Lancement de la boucle événementielle 
        self.racine.mainloop()
        # Initialisation des fenêtres secondaires
        self.fen_infos = None
        self.fen_traitement = None
        self.fen_resultat = None 
        # Initialisation des attributs de la classe
        self.duree_film = 0 # en min, à récupérer lors du chargement du fichier
        # Lancement des fonctions
        self.creer_widgets(self.racine)


    def creer_widgets(self, root) :
        # Bouton de sélection du fichier
        self.bouton_charger_fichier = tk.Button(root, text = 'Sélectionner fichier')
        self.bouton_charger_fichier.bind('<Button-1>', self.charger_fichier)
        self.bouton_charger_fichier.pack(side = tk.TOP)

        # Listbox de choix du mode de traitement
        self.listbox_mode_de_traitement = tk.Listbox(root, text = 'Choisir le mode de traitement')
        self.listbox_mode_de_traitement.insert(1, "Couleur moyenne par image - bandes")
        self.listbox_mode_de_traitement.insert(2, "Couleur moyenne par image - circulaire")
        self.listbox_mode_de_traitement.insert(3, "Couleurs par clusters")
        self.listbox_mode_de_traitement.bind('<Button-1>', self.clic_listbox)
        self.listbox_mode_de_traitement.pack(side = tk.TOP)

        # Slider de choix de l'extrait à analyser (en min)
        self.tps_min = tk.IntVar() # variable réglable gauche
        self.tps_max = tk.IntVar()  # variable réglable droite
        self.etiquette_slider = tk.Label (root, text = "Sélectionner le début et la fin de l'extrait à analyser")
        self.etiquette_slider.pack()
        self.slider = RangeSliderH(root, [self.tps_min, self.tps_max], Width=230, Height=55, padX=17, min_val=0, max_val=self.duree_film, font_size=12,\
            line_s_color='black',line_color='black', bar_color_inner='black')
        self.slider.pack(side = tk.TOP)

        # Bouton de lancement du traitement 
        self.bouton_lancer = tk.Button(root, text = 'Lancer le traitement')
        self.bouton_lancer.bind('<Button-1>', self.lancer_traitement)
        self.bouton_lancer.pack(side = tk.BOTTOM)


        ### Fenêtre infos ###        
        def ouvrir_fenetre_infos(self) :
            if (self.fen_infos != None) :
                self.fen_infos.destroy()
            # Construction fenêtre
            self.fen_infos = tk.Toplevel(root)
            self.fen_infos.title('Informations fichier')
            self.fen_infos.geometry('300x200')
            self.fen_infos.mainloop()

            # Box contenant les zones d'entrées
            self.fen_infos.etiquette_infos_film = tk.Label(self.fen_infos, text = 'Remplir les informations du film')
            self.fen_infos_etiquette_titre.pack(anchor = tk.W)

            self.var_titre = tk.StringVar()
            self.fen_infos.entree_titre = tk.Entry(self.fen_infos, textvariable = self.var_titre, text = 'Titre du film' )
            self.fen_infos.entree_titre.pack()

            self.var_genre = tk.StringVar()
            self.fen_infos.entree_genre = tk.Entry(self.fen_infos, textvariable = self.var_genre, text = 'Genre du film' )
            self.fen_infos.entree_genre.pack()

            self.var_date = tk.StringVar()
            self.fen_infos.entree_date = tk.Entry(self.fen_infos, textvariable = self.var_date, text = 'Date du film' )
            self.fen_infos.entree_date.pack()

            self.var_real = tk.StringVar()
            self.fen_infos.entree_real = tk.Entry(self.fen_infos, textvariable = self.var_real, text = 'Réalisateur du film' )
            self.fen_infos.entree_real.pack()

            # Bouton option charger imdb
            self.fen_infos.bouton_imdb = tk.Button(self.fen_infos, text = 'Option charger depuis IMdB')
            self.fen_infos.bouton_imdb.bind('<Button-1>', self.charger_depuis_imdb)
            self.fen_infos.bouton_imdb.pack(side = tk.BOTTOM)
            self.fen_infos.etiquette_imdb = tk.Label(self.fen_infos, \
                text = "Vous pouvez directement charger les informations restantes du film avec l'option suivante si vous le souhaitez. \n"\
                    + " Champ obligatoire : Titre du film") # autres champs obligatoires ?
            self.fen_infos.etiquette_imdb.pack(side = tk.BOTTOM)

        
        ### Fenêtre traitement ###
        def ouvrir_fenetre_traitement(self) :
            if (self.fen_traitement != None) :
                self.fen_traitement.destroy()
            self.fen_traitement = tk.Toplevel(root)
            self.fen_traitement.title('Traitement du fichier')
            self.fen_traitement.geometry('300*200')
            self.fen_traitement.mainloop()
        # autres widgets 
        # Bouton de renvoi à la bibliothèque constituée
        self.bouton_biblio = tk.Button(self.fen_traitement, text = 'Afficher la bibliothèque')
        self.bouton_biblio.bind('<Button-1>', ouvrir_page_web)
        self.bouton_biblio.pack(side = tk.BOTTOM)


        ### Fenêtre de présentation de l'image résultat ###
        # condition de lancement de la fonction : pop up quand le traitement est terminé
        def ouvrir_fenetre_resultat(self) :
            if (self.fen_resultat != None) :
                self.fen_resultat.destroy()
            self.fen_resultat = tk.Toplevel(root)
            self.fen_resultat.title('Résultat du traitement de votre fichier')
            self.fen_resultat.geometry('600*400')
            self.fen_resultat.mainloop()
        #widgets à installer à definir

        ### Page web Bibliothèque ###
        def ouvrir_page_web(self, event) :
            pass

    # Fonctions callback 
    def clic_listbox(self, event) :
        i = self.listbox_mode_de_traitement.curselection()
        if i == 1 :
            self.listbox_mode_de_traitement.appliquer_mode_1()
        elif i == 2 :
            self.listbox_mode_de_traitement.appliquer_mode_2()
        else : 
            self.listbox_mode_de_traitement.appliquer_mode_3()

    def charger_fichier(self, event) :
        pass
    def lancer_traitement(self, event) :
        # Lancement des fenêtres d'information et de traitement 
        ouvrir_fen_infos()
        ouvrir_fen_traitement()
        #fonction à ajouter
    def charger_depuis_imdb(self, event) :
        pass
    

    # Autres fonctions appelées
    def appliquer_mode_1(self) :
        pass
    def appliquer_mode_2(self) :
        pass
    def appliquer_mode_3(self) :
        # Curseur de qualité
        self.var_qualité = tk.DoubleVar()
        self.curseur_qualité = tk.Scale(root, orient = 'horizontal', variable = self.var_qualité)
        self.curseur_qualité.pack(side = tk.TOP)
        # fonction à ajouter

app = Fenetre()

