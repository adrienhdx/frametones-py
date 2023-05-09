
import tkinter as tk
from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
import os
import json


class InfoWindow() :
    def __init__(self, master, out_path) :
        #Initialisation de la fenêtre
        self.window = Toplevel(master)
        # Attributs esthétiques
        self.window.title('Informations du fichier chargé')
        self.window.geometry('235x290')
        self.window.configure(bg = 'white')
        # Lancement du gestionnaire d'évènement 
        self.creer_widgets(self.window)
        self.window.mainloop()
        self.db_path = ""
        self.out_path = out_path

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
                proceed = True
                if not proceed : return
                print("ERROR FILM IN DB")
                return
            
        #   ajouter le film à la base de données
        
        film_object = {
            "title": self.var_titre.get(),
            "year": self.var_annee.get(),
            "director": self.var_real.get()
        }

        db.append(film_object)

        new_db = json.dumps(db, indent=4)

        with open(self.db_path, 'w') as f:
            f.write(new_db)

        self.window.destroy()

        
# TODO : load info from json

class ResultsWindow():
        """
        blue,green,red = cv2.split(img)
        img = cv2.merge((red,green,blue))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        """ 
        def __init__(self, master) -> None:
            # path is json database where info was written

            self.window = Toplevel(master)
            self.window.configure(bg='white')
            self.window.title("Résultats")
            self.window.geometry(f"720x480")
            """self.img = PhotoImage(file=f'{path}/output_image.png')
            # Resize image width to maximum 720px
            self.img = self.img.zoom(480//self.img.height())
            #self.img = cv2.resize(self.img, (720, 480))"""
            self.create_widgets()
        
        def create_widgets(self):
            self.output_image_title = ttk.Label(self.window, text = 'Résultats', font='Arial 13 bold', style='white.TLabel')
            self.output_image_title.pack()

            # titre du film
            film_name = ""#os.path.split(self.film_path)[1].split('.')[0]
            self.output_image_film_title = ttk.Label(self.window, text = f'Film : {film_name}', font='Arial 10 bold', style='white.TLabel')
            self.output_image_film_title.pack()

            # Réalisateur
            self.output_image_director = ttk.Label(self.window, text = f'Réalisateur : Youssef Guermazi', font='Arial 10 bold', style='white.TLabel')
            self.output_image_director.pack()

            # Année
            self.output_image_year = ttk.Label(self.window, text = f'Année : 2023', font='Arial 10 bold', style='white.TLabel')
            self.output_image_year.pack()

            # Image
            """self.output_image_display = Label(self.window, image=self.img)
            self.output_image_display.pack()"""
            
         
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Informations du fichier chargé')
    root.geometry('10x10')
    root.configure(bg = 'white')
    ResultsWindow(root)
    root.mainloop()