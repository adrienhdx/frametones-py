
import cv2 #pip install opencv-python
import os
import utils
import time
from windows import InfoWindow, ResultsWindow
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from RangeSlider import RangeSliderH
import numpy as np
import psutil #pip install psutil
from PIL import Image, ImageTk #pip install pillow

#Description document : 
#Ce document comporte la classe définissant la fenêtre racine (menu principal) ainsi que toutes les options associées
#(activation des fonctions via l'interaction de l'utilisateur avec les widgets du menu principal)
#Les fonctions codées correspondent au code principal (main) du traitement du film, des options liées aux widgets
#et du lancement des fenêtres secondaires (dont les classes sont définies dans un document à part). 
#Certaines fonctions appelées lors du traitement technique sont définies à part, dans le document "utils"


class MenuPrincipal() :
    def __init__(self) :
        """Initialisation de la fenêtre racine (paramètres principaux, attributs, lancement du gestionnaore 
        d'évènements et lancement de la création des wigets)
        """
        # Initialisation de la fenêtre racine
        self.root = Tk()
        self.resultsWindow = None
        self.infoWindow = None
        self.folder_path = os.getcwd()

        # fond blanc
        self.root.configure(bg='white')

        # Attributs esthétiques de la fenêtre
        self.root.title('Menu principal')
        self.root.geometry('720x480')

        # Film info

        self.film_path = ""
        self.out_path = ""
        self.n_film_frames = -1
        self.source = None

        # Processor settings

        self.output_height = IntVar(value=300)
        self.frame_count = IntVar(value=1500)

        self.highres = IntVar(value=0)

        self.mode = IntVar(value=1)

        self.start_frame_number = IntVar(value=0)
        self.end_frame_number = IntVar(value=340000)

        self.progress = IntVar(value=0)

        # Styles

        self.radiostyle = ttk.Style()
        self.radiostyle.configure('white.TRadiobutton', background='white')

        self.labelstyle = ttk.Style()
        self.labelstyle.configure('white.TLabel', background='white')

        # Source images

        self.empty_preview = PhotoImage(file='resources/empty_preview.png')
        self.handle = PhotoImage(file='resources/handle.png')

        # Lancement des fonctions
        self.creer_widgets(self.root)
        self.root.mainloop()

    def creer_widgets(self, root):
        """Mise en place des widgets de la fenêtre : 
        à gauche, options permettant de sélectionner un fichier video, les paramètres de traitement et le mode de traitement de la colorimétrie du fichier,
        de préciser si la fichier source est de haute résolution et d'indiquer la qualité souhaitée (slider),  ;
        à droite, affichage de l'image de début et de l'image de fin, bouton actualiser, slider nombre d'images par heures ;
        en bas, bouton de lancement du traitement et barre de progression du traitement 
        Parameters
        ----------
        root : _type : Tk_
            _fenetre racine_
        """
        # TOP

        self.projectname_header = ttk.Label(root, text = 'Projet algo S4', font='Arial 13 bold', style='white.TLabel')
        self.projectname_header.place(x=304, y=10)

        self.projectversion_header = ttk.Label(root, text = 'version 1.0', font='Arial 11 italic', style='white.TLabel')
        self.projectversion_header.place(x=322, y=30)

        # MIDDLE LEFT

        self.source_header = ttk.Label(root, text = 'Source', font='Arial 11 bold', style='white.TLabel')
        self.source_header.place(x=73, y=70)

        self.selectfile_entry = ttk.Entry(root, width = 29, font='Arial 10', background='white')
        self.selectfile_entry.place(x=73, y=94)
        self.selectfile_entry.insert(INSERT, "Sélectionner un fichier source")
        self.selectfile_entry.configure(state='readonly')

        self.selectfile_button = ttk.Button(root, text = '...', width=3, command=self.load_film)
        self.selectfile_button.place(x=282, y=94)

        self.highres_checkbox = ttk.Checkbutton(root, onvalue=1, offvalue=0, variable=self.highres)
        self.highres_checkbox.place(x=73, y=135)

        self.highres_label1 = ttk.Label(root, text = 'Haute résolution', font='Arial 10', style='white.TLabel')
        self.highres_label1.place(x=95, y=122)

        self.highres_label2 = ttk.Label(root, text = 'Sélectionner si la résolution du fichier source\ndépasse 480x360', font='Arial 9 italic', style='white.TLabel')
        self.highres_label2.place(x=95, y=141)

        self.processing_header = ttk.Label(root, text = 'Paramètres de traitement', font='Arial 11 bold', style='white.TLabel')
        self.processing_header.place(x=73, y=180)

        self.meanbands_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - bandes', value=1, variable=self.mode, style='white.TRadiobutton', command=self.set_defaults)
        self.meanbands_radiobutton.place(x=73, y=203)

        self.meancircle_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - circulaire', value=2, variable=self.mode, style='white.TRadiobutton', command=self.set_defaults)
        self.meancircle_radiobutton.place(x=73, y=222)

        self.clusters_radiobutton = ttk.Radiobutton(root, text = 'Couleurs par clusters', value=3, variable=self.mode, style='white.TRadiobutton', command=self.set_defaults)
        self.clusters_radiobutton.place(x=73, y=241)

        self.output_height_slider = Scale(root, from_=100, to=1000, resolution=10, background='white', variable=self.output_height, orient=HORIZONTAL, length=250)
        self.output_height_slider.place(x=73, y=270)

        self.quality_label = ttk.Label(root, text = 'Hauteur de l\'image', font='Arial 10', style='white.TLabel')
        self.quality_label.place(x=150, y=310)

        # MIDDLE RIGHT

        self.videosettings_header = ttk.Label(root, text = 'Paramètres vidéo', font='Arial 11 bold', style='white.TLabel')
        self.videosettings_header.place(x=400, y=70)

        self.leftimage_label = ttk.Label(root, text = 'première image', font='Arial 10 italic', style='white.TLabel')
        self.leftimage_label.place(x=400, y=94)

        self.rightimage_label = ttk.Label(root, text = 'dernière image', font='Arial 10 italic', style='white.TLabel')
        self.rightimage_label.place(x=530, y=94)

        self.leftimage_image = self.empty_preview
        self.leftimage_label = ttk.Label(root, image=self.leftimage_image)
        self.leftimage_label.place(x=400, y=114)

        self.rightimage_image = self.empty_preview
        self.rightimage_label = ttk.Label(root, image=self.rightimage_image)
        self.rightimage_label.place(x=530, y=114)

        self.time_rangeslider = RangeSliderH(root, [self.start_frame_number, self.end_frame_number], Width=255, Height=45, padX=25, min_val=0, max_val=self.end_frame_number.get(), font_size=10,\
     line_s_color='black',line_color='black', bar_color_inner='white', bar_color_outer='black',  line_width=1, bar_radius=8, font_family='Arial', show_value=True,\
        valueSide='BOTTOM', digit_precision='.0f', imageL=self.handle, imageR=self.handle, auto=False)
        self.time_rangeslider.place(x=400, y=180)

        self.refresh_button = ttk.Button(root, text = 'Actualiser', width=10, command=self.refresh_preview)
        self.refresh_button.place(x=400, y=225)

        self.imagecount_slider = Scale(root, from_=100, to=2500, resolution=10, orient=HORIZONTAL, length=250, variable=self.frame_count, background='white')
        self.imagecount_slider.place(x=400, y=270)

        self.imagesperhour_label = ttk.Label(root, text = 'Images à traiter', font='Arial 10', style='white.TLabel')
        self.imagesperhour_label.place(x=480, y=310)


        # BOTTOM

        self.begin_button = ttk.Button(root, text = 'Lancer le traitement', width=20, command=self.begin)
        self.begin_button.place(x=300, y=350)

        self.progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=574, mode='determinate', maximum=self.frame_count.get(), variable=self.progress)
        self.progressbar.place(x=73, y=391)

        self.info_text = Text(root, width=69, height=2, font='Arial 10', state="disabled")
        self.info_text.place(x=73, y=420)

        self.usage_text=  Text(root, width=11, height=2, font='Arial 10', state="disabled")
        self.usage_text.place(x=566, y=420)
        self.write_info(self.usage_text, 'En attente\n')
        self.write_info(self.usage_text, '...\n') 

    def load_film(self):
        """Chargement du fichier video : l'utilisateur clique sur un ficier dont on récupère le chemin, qu'on insère dans la zone d'entrée
        (vidée au préalable). Affichage d'un message d'information indiquant que le fichier a été chargé et son chemin.
        On récupère le fichier video avec cv2 et son nombre d'image.
        Mise à jour de la longueur du slider de temps (adaptation à la longueur du fichier en fonction du nombre d'images)
        """
        self.film_path = filedialog.askopenfilename(title = "Choisir un fichier", filetypes = (("Video files", "*.mp4"), ("all files", "*.*")), initialdir=os.path.expanduser('~\Videos'))

        if self.film_path == '':
            return

        self.selectfile_entry.config(state='normal')
        self.selectfile_entry.delete(0, END)
        self.selectfile_entry.insert(0, self.film_path)
        self.selectfile_entry.config(state='disabled')

        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, 'Fichier vidéo chargé : ' + self.film_path + '\n')
        

        # get relevant file info
        self.source = cv2.VideoCapture(self.film_path)
        self.n_film_frames = int(self.source.get(cv2.CAP_PROP_FRAME_COUNT))
        film_resolution = (int(self.source.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.source.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.write_info(self.info_text, f"Résolution : {film_resolution[0]}x{film_resolution[1]}\n")

        # update slider
        self.time_rangeslider.max_val=self.n_film_frames
        self.time_rangeslider.forceValues([0, self.n_film_frames])

        self.refresh_preview()

    def refresh_preview(self):
        """Récupère la première et la dernière image du film et les affiche dans les cadres "1ère image" et "dernière image"
        (les images sont récupérées et redimensionnées avec cv2 puis écrites sous forme de fichiers png,
        elles sont ensuite mises à jour avec PhotoImage  afin d'être compatibles avec tkinter pour être collées dans les cadres de droite)
        Si le chemin de fichier entré est vide, la fonction affiche un message d'erreur. 
        """
        if self.film_path == '':
            self.write_info(self.info_text, 'Erreur : Aucun fichier vidéo chargé\n')
            return
        
        # get the first image at the start time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get())
        start_frame = self.source.read()[1]
        start_frame = cv2.resize(start_frame, (120, 60))

        # get the last image at the end time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.end_frame_number.get()-1)
        end_frame = self.source.read()[1]
        end_frame = cv2.resize(end_frame, (120, 60))

        # write images as files
        # TODO : fix "no such file or directory" error
        os.chdir(self.folder_path)
        cv2.imwrite('resources/start_frame.png', start_frame)
        cv2.imwrite('resources/end_frame.png', end_frame)
        # update the images
        self.leftimage_image = PhotoImage(file='resources/start_frame.png')
        self.rightimage_image = PhotoImage(file='resources/end_frame.png')

        self.leftimage_label.config(image=self.leftimage_image)
        self.rightimage_label.config(image=self.rightimage_image)
        
    def set_defaults(self):
        """Affecte des valeurs par défaut aux attributs self.frame_count et self.output_height
         pour les différents modes de traitement (meanbands, meancircles and cluster) ;
         met à jour les deux sliders (images par heure et qualité de résolution)
        """
        # default values for each mode

        # Mode 1 : meanbands
        # Output height = 300
        # Frame count = 1500

        # Mode 2 : meancircles
        # Output height = 1000
        # Frame count = 250

        # Mode 3 : clusters
        # Output height = 300
        # Frame count = 1500

        def1 = [300, 1500]
        def2 = [1000, 250]
        def3 = [300, 1500]

        match self.mode.get():
            case 1:
                self.output_height.set(def1[0])
                self.frame_count.set(def1[1])
            case 2:
                self.output_height.set(def2[0])
                self.frame_count.set(def2[1])
            case 3:
                self.output_height.set(def3[0])
                self.frame_count.set(def3[1])
        
        self.imagecount_slider.update()
        self.output_height_slider.update()

    def write_info(self, subject, text):
        """Entrer les informations à écrire et afficher dans un objet de type Text

        Parameters
        ----------
        subject : _type : objet de la classe Text_
            _sert à afficher un text (sur lequel on peut effectuer des modifications) sur la fenêtre_
        text : _type : string_
            _chaine de caractères à insérer_
        """
        subject.config(state='normal')
        subject.insert(INSERT, text)
        subject.config(state='disabled')

    def delete_all_info(self, subject):
        """Supprimer les informations écrites dans l'objet Text (réinitialisation de l'objet)

        Parameters
        ----------
        subject : _type : objet de la classe Text_
            _permet d'afficher un texte modifiable sur la fenêtre graphique_
        """
        subject.config(state='normal')
        subject.delete(1.0, END)
        subject.config(state='disabled')

    def process_avg(self, circle=False):
        """Si le mode "bandes" a été selectionné : calcul de la moyenne de couleurs et ajout d'une bande de taille normalisée de la couleur moyenne correspondant à cette image.
        Si le mode "cercles" a été selectionné : fixation des dimensions des cercles pour chaque image (selon le pas de traitement), 
        création d'une liste des couleurs moyennes pour l'ensemble des images traitées, insertion des cercles sur l'image (en partant de 
        la fin de la liste donc du cercle de plus grand diamètre)

        Parameters
        ----------
        circle : _type = bool
            indique si le mode cercle a été choisi ou non dans le cas où on choisit la couleur par moyennes
            vaut False par défaut

        Returns
        -------
        output_image : _type = ndarray
            image par bandes / par cercles représentative de la colorimétrie du film ( ndarray de taille (hauteur, largeur, 3) )
        """
        height = self.output_height.get()
        frame_count = self.frame_count.get()

        if not circle:
            output_image = np.zeros((height, frame_count, 3), np.uint8)

            for i in range(frame_count):

                self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
                frame = self.source.read()[1]

                if bool(self.highres.get()):
                    frame = cv2.resize(frame, (240, 180))

                output_image[:, i] = utils.avg_strip_RGB(frame)  #average_frame_color_HSV(frame)

                self.log_progress(i)
        else:
            
            # fix aspect ratio to sqrt(2)
            aspect = 2**0.5    

            output_width = int(height / aspect)   

            diagonal = np.sqrt(height**2 + output_width**2)      # max number of 1px circles
            circle_width = int(diagonal / frame_count)                  
            
            output_image = np.zeros((height, output_width, 3), np.uint8)

            colors = []

            # get color list
            for i in range(frame_count):

                self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
                frame = self.source.read()[1]

                frame = cv2.resize(frame, (240, 180))

                colors.append(utils.avg_strip_RGB(frame))  #average_strip_HSV(frame)
            
                self.log_progress(i)

            # create circles for every color
            for i in reversed(range(frame_count)):
                cv2.circle(output_image, (0,0), i*circle_width, (colors[i].tolist()), -1) # color is BGR

        return output_image

    def process_kmeans(self):
        """Initialisation de l'image (et de ses dimensions) et du timer de création de l'image finale, 
        pour chaque image traitée (selon le pas de traitement) : calcul des 7 couleurs prédominantes puis insertion sur l'image d'une bande tenant compte de ce calcul 
        dans l'ordre chronologique du film

        Returns
        -------
        output_image : _type : image_
            _image représentative de la colorimétrie chronologique du film obtenue par un processus de clustering (accès avec cv2)_
        """
        height = self.output_height.get()
        frame_count = self.frame_count.get()
        output_image = np.zeros((height+4, frame_count, 3), np.uint8)

        for i in range(frame_count):

            self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
            frame = self.source.read()[1]
            output_image[:, i] = utils.kmeans_strip(image=frame, color_count=7, strip_height=height+4, compress=bool(self.highres.get()))[:, 0]

            self.log_progress(i)

        output_image = output_image[4:, :, :]

        return output_image
    
    def begin(self):
        """Choix d'un dossier de destination pour l'image par l'utilisateur. 
        Si aucun fichier n'est chargé ou aucun dossier de destination n'est sélectionné, un message d'erreur est affiché.
        Lancement du traitement du film et de la fenêtre d'informations à remplir par l'utilisateur
        """
        if self.film_path == "":
            self.write_info(self.info_text, "Erreur : Aucun fichier vidéo chargé\n")
            return
    
        self.out_path = filedialog.askdirectory(title = "Choisir un dossier de destination", mustexist=True, initialdir=os.path.expanduser('~\Videos'))

        if self.out_path == "":
            self.write_info(self.info_text, "Erreur : Aucun dossier de destination sélectionné\n")
            return

        self.process_film()
        self.open_info_window()

    def open_info_window(self):
        """Instanciation d'un objet fenêtre de la  classe InfoWindow, lancée pour récupérer les informations du film.
        """
        self.infoWindow = InfoWindow(self.root, self.out_path)
        
    def process_film(self):
        """Calcul du pas de traitement des images. Lancement d'un timer de traitement. Lancement de l'analyse colorimétrique et
        de la production d'une image représentative de la colorimétrie du fichier vidéo en fonction du mode choisi.
        L'image produite est récupérée et stockée dans le dossier choisi au départ par l'utilisateur.
        ((Le répertoire d'études est redirigé à l'endroit où l'on stocke les images))
        Affichage de messages d'information (image chargée, temps de traitement)
        Affichage de l'image résultat.
        Au cours du traitement, l'utilisation des différents widgets est blockée afin d'éviter toute erreur, elle est à nouveau disponible à la fin du traitement.
        On réinitialise les variables utiles afin de pouvoir lancer un nouveau traitement
        """
        self.disable_all()

        os.chdir(self.out_path)

        self.frame_step = (self.end_frame_number.get() - self.start_frame_number.get()) // self.frame_count.get()
        self.progressbar.config(maximum=self.frame_count.get())

        start_time = time.time()

        match self.mode.get():
            case 1: # Bands
                output_image = self.process_avg(circle=False)
            case 2: # Circles
                # check if image count is greater than output height
                if self.frame_count.get() > self.output_height.get():
                    self.delete_all_info(self.info_text)
                    self.write_info(self.info_text, "Attention : Le nombre de cercles est supérieur à la hauteur de l'image\n")
                    self.enable_all()
                    return

                output_image = self.process_avg(circle=True)
            case 3: # KMeans
                # paramètres bancals
                output_image = self.process_kmeans()

        cv2.imwrite(f"output_image.png", output_image)

        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, f"Image enregistrée dans {self.out_path}\n")
        self.write_info(self.info_text, f"Temps de traitement : {time.time()-start_time:.1f}s\n")
        
        self.enable_all()
        self.reset_vars()     

    def disable_all(self):
        """Désactivation des fonctionnalités des widgets : l'utilisateur ne peut plus les activer
        """
        # disable everything while processing
        self.begin_button.config(state='disabled')
        self.selectfile_button.config(state='disabled')
        self.meanbands_radiobutton.config(state='disabled')
        self.meancircle_radiobutton.config(state='disabled')
        self.clusters_radiobutton.config(state='disabled')
        self.highres_checkbox.config(state='disabled')
        self.refresh_button.config(state='disabled')
        self.output_height_slider.config(state='disabled')
        self.imagecount_slider.config(state='disabled')

    def enable_all(self):
        """Activation des fonctionnalités des widgets cités ci-dessous
        """
        # enable everything after processing
        self.begin_button.config(state='normal')
        self.selectfile_button.config(state='normal')
        self.meanbands_radiobutton.config(state='normal')
        self.meancircle_radiobutton.config(state='normal')
        self.clusters_radiobutton.config(state='normal')
        self.highres_checkbox.config(state='normal')
        self.refresh_button.config(state='normal')
        self.output_height_slider.config(state='normal')
        self.imagecount_slider.config(state='normal')

    def reset_vars(self):
        """ Réinitialisation de la variable de progression de chargement et redéfinition du répertoire d'études 
        à l'endroit où l'image a été stockée 
        """
        # reset variables
        # dunno what to add there
        self.progress.set(0)
        self.delete_all_info(self.usage_text)
        self.write_info(self.usage_text, 'En attente\n')
        self.write_info(self.usage_text, '...\n') 

    def log_progress(self, frame):
        """Détermination du la progression du traitement par rapport à la longueur totale du fichier à traiter 
        et affichage de cette progression à l'aide d'un texte qui indique le temps écoulé depuis le lancement du traitement
        et de la progressbar (évolution de l'affichage dans le temps : texte et progressbar actualisés continuellement jusqu'à la fin du traitement)

        Parameters
        ----------
        frame : _type : int
            numéro de l'image en traitement

        """
        # notify progress
        self.progress.set(frame+1)
        self.delete_all_info(self.info_text)
        self.delete_all_info(self.usage_text)

        self.write_info(self.info_text, f"Image {frame+1}/{self.frame_count.get()} traitée\n")
        self.write_info(self.usage_text, f"RAM: {psutil.virtual_memory()[2]}%\n")

        self.progressbar.update()
        self.info_text.update()
        self.usage_text.update()
    
    
app = MenuPrincipal()