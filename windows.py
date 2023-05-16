
import tkinter as tk
from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
import os
import json

#Description du document : 
#Definition des classes InfoWindow et Resultswindow (fenêtres secondaires), appelées dans le main
#lorsqu'on souhaite respectivement récupérer les informations du film ou afficher le résultat du traitement

class InfoWindow() :
    def __init__(self, master, out_path) :
        #Initialisation de la fenêtre
        self.master = master
        self.window = Toplevel(self.master)
        # Attributs esthétiques
        self.window.title('Informations du fichier chargé')
        self.window.geometry('235x290')
        self.window.configure(bg = 'white')
        # Lancement du gestionnaire d'évènement 
        self.db_path = ""
        self.out_path = out_path
        self.creer_widgets(self.window)
        self.window.mainloop()

    def creer_widgets(self, root) :
        # Box contenant les zones d'entrées
        self.etiquette_infos_film = ttk.Label(root, text = 'Informations du film' , font = 'Arial 11 bold')
        self.etiquette_infos_film.place(x = 22, y = 20)

        self.var_titre = StringVar()
        self.etiquette_titre = ttk.Label(root, text = 'Titre du film', font='Arial 10')
        self.etiquette_titre.place(x = 22, y = 60)
        self.entree_titre = ttk.Entry(root, textvariable = self.var_titre, width = 20, font = 'Arial 10')
        self.entree_titre.place(x = 22, y = 80)

        self.var_real = StringVar()
        self.etiquette_real = ttk.Label(root, text = 'Nom du réalisateur ', font='Arial 10')
        self.etiquette_real.place(x = 22, y = 110)
        self.entree_real = ttk.Entry(root, textvariable = self.var_real, width = 20, font = 'Arial 10')
        self.entree_real.place(x = 22, y = 130)

        self.var_annee = StringVar()
        self.etiquette_annee = ttk.Label(root, text = 'Année de sortie', font='Arial 10')
        self.etiquette_annee.place(x = 22, y = 160)
        self.entree_annee = ttk.Entry(root, textvariable = self.var_annee, width = 10, font = 'Arial 10')
        self.entree_annee.place(x = 22, y = 180)

        #A changer pour un système similaire à mainloop (entry désactivée)
        # TODO
        self.texte = ttk.Label(root, \
            text = "Merci de vérifier les informations\navant de cliquer sur Valider.", font='Arial 10') # autres champs obligatoires ?
        self.texte.place(x = 22, y = 210)
            
        self.bouton_valider = ttk.Button(root, text = 'Valider', command=self.valider)
        self.bouton_valider.place(x = 75, y = 250)

    def valider(self) :
        # vérifier que les champs sont remplis
        if self.var_titre.get() == '' or self.var_real.get() == '' or self.var_annee.get() == '' :
            # afficher un message d'erreur
            self.texte.configure(text = 'Merci de remplir tous les champs.')
            return
        elif not self.var_annee.get().isdigit() :
            self.texte.configure(text = 'Merci de rentrer une année valide.')
            return
        
        #       ouvrir la base de données
        #   demander le fichier à charger
        self.db_path = filedialog.askopenfilename(title = "Choisir le fichier de base de données", filetypes = [('Fichiers JSON', '.json')], initialdir=os.path.expanduser('~\Documents\GitHub'))

        if self.db_path == '':
            self.texte.configure(text = 'Merci de choisir un fichier valide.')
            return
    
        self.charger_fichier()

    def charger_fichier(self):
        #   Tout est valide, on peut charger le fichier
        with open(self.db_path, 'r') as db_file :
            db = json.load(db_file)
        
        #   vérifier que le film n'est pas déjà dans la base de données
        # TODO
        films_in_db = [list(e.values())[0] for e in db]
        for film in films_in_db :
            if film == self.var_titre.get():
                # display error message asking the user if he wants to overwrite
                self.texte.configure(text = 'Le film est déjà dans la base de données. \n il n\'est pas possible de l\'ajouter.')
                return
            
        #   ajouter le film à la base de données
        
        film_object = {
            "title": self.var_titre.get(),
            "year": self.var_annee.get(),
            "director": self.var_real.get(),
            "img_name": self.out_path + "/output_image.png"
        }

        db.append(film_object)

        new_db = json.dumps(db, indent=4)

        with open(self.db_path, 'w') as f:
            f.write(new_db)

        ResultsWindow(self.master, self.db_path)

        self.window.destroy()


class ResultsWindow():
        def __init__(self, master, path) -> None:

            self.window = Toplevel(master)
            self.window.configure(bg='white')
            self.window.title("Résultats")
            self.window.geometry(f"720x420")
            self.window.resizable(False, False)

            self.film_name=''
            self.director_name=''
            self.year=''
            self.img_path=''
            self.img=None

            self.create_widgets(path)
        
        def create_widgets(self, path):
            # load info from json
            with open(path, 'r') as db_file :
                db = json.load(db_file)

            # get last film
            film = db[-1]
            self.film_name = film['title']
            self.director_name = film['director']
            self.year = film['year']
            self.img_path = film['img_name']
            self.img = PhotoImage(file=self.img_path, master=self.window)
            
            # Zoom image to fit window if it's too small
            if self.img.width()< 700 and self.img.height()< 400:
                if self.img.width()< self.img.height():
                    zoom_factor = 400//self.img.height()
                    self.img = self.img.zoom(zoom_factor)
                else:
                    zoom_factor = 600//self.img.width()
                    self.img = self.img.zoom(zoom_factor)
            # dezoom if too big
            elif self.img.width()> 700 or self.img.height()> 400:
                if self.img.width()> self.img.height():
                    zoom_factor = self.img.width()//600
                    print(zoom_factor)
                    self.img = self.img.subsample(zoom_factor)
                else:
                    zoom_factor = self.img.height()//400
                    print(zoom_factor)
                    self.img = self.img.subsample(zoom_factor)
            
            # Resize window height
            self.window.geometry(f"720x{self.img.height()+150}")


            # Labels
            self.output_image_title = ttk.Label(self.window, text = 'Résultats', font='Arial 13 bold', style='white.TLabel')
            self.output_image_title.pack()

            # titre du film
            self.output_image_film_title = ttk.Label(self.window, text = f'Film : {self.film_name}', font='Arial 10', style='white.TLabel')
            self.output_image_film_title.pack()

            # Réalisateur
            self.output_image_director = ttk.Label(self.window, text = f'Réalisateur : {self.director_name}', font='Arial 10', style='white.TLabel')
            self.output_image_director.pack()

            # Année
            self.output_image_year = ttk.Label(self.window, text = f'Année : {self.year}', font='Arial 10', style='white.TLabel')
            self.output_image_year.pack()

            # Image
            self.output_image_display = tk.Label(self.window, image=self.img)
            self.output_image_display.pack()
            # Evil GC hack
            self.output_image_display.image = self.img

            # Bouton Ouvrir avec Photos
            self.output_image_display_button = ttk.Button(self.window, text = 'Ouvrir avec Photos', command=self.open_folder)
            self.output_image_display_button.pack()

            # Bouton Retour
            self.output_image_display_button = ttk.Button(self.window, text = 'Retour', command=self.window.destroy)
            self.output_image_display_button.pack()

        def open_folder(self):
            os.startfile(self.img_path)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ajouter un film")
    root.geometry("10x10")
    root.configure(bg='white')
    app = ResultsWindow(root, 'db2.json')
    root.mainloop()