# empty tkinter window


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from RangeSlider.RangeSlider import RangeSliderH

class Fenetre() :
    def __init__(self) :
        # Initialisation de la fenêtre racine
        self.racine = Tk()

        # fond blanc
        self.racine.configure(bg='white')

        # Attributs esthétiques de la fenêtre
        self.racine.title('Menu principal')
        self.racine.geometry('720x480')

        self.highres = IntVar()
        self.highres.set(0)

        self.mode = IntVar()
        self.mode.set(1)

        self.quality = IntVar()
        self.quality.set(7)

        self.imagesperhour = IntVar()
        self.imagesperhour.set(1000)

        self.start_time = IntVar()
        self.start_time.set(0)

        self.end_time = IntVar()
        self.end_time.set(20)

        self.images_to_compute = 1500

        self.progress = IntVar()
        self.progress.set(100)

        # Styles

        self.radiostyle = ttk.Style()
        self.radiostyle.configure('white.TRadiobutton', background='white')

        self.labelstyle = ttk.Style()
        self.labelstyle.configure('white.TLabel', background='white')

        # Source images

        self.empty_preview = PhotoImage(file='empty_preview.png')
        self.handle = PhotoImage(file='handle.png')

        # Lancement des fonctions
        self.creer_widgets(self.racine)
        self.racine.mainloop()

    def creer_widgets(self, root):
        # TOP
        # Projet algo S4 (header)
        # version 1.0 (header)

        self.projectname_header = ttk.Label(root, text = 'Projet algo S4', font='Arial 13 bold', style='white.TLabel')
        self.projectname_header.place(x=304, y=10)

        self.projectversion_header = ttk.Label(root, text = 'version 1.0', font='Arial 11 italic', style='white.TLabel')
        self.projectversion_header.place(x=322, y=30)

        # MIDDLE LEFT
        # Source (header)
        # Sélectionner fichier (Entry to display filename)
        # Sélectionner fichier (Button to open file explorer)
        # Haute résolution (checkbox)
        # Haute résolution (label)
        # Explication haute résolution (label)
        # Paramètres de traitement (header)
        # Couleur moyenne par image - bandes (radio button)
        # Couleur moyenne par image - circulaire (radio button)
        # Couleurs par clusters (radio button)
        # curseur qualité (slider)
        # Qualité (label)

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

        self.meanbands_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - bandes', value=1, variable=self.mode, style='white.TRadiobutton')
        self.meanbands_radiobutton.place(x=73, y=203)

        self.meancircle_radiobutton = ttk.Radiobutton(root, text = 'Couleur moyenne par image - circulaire', value=2, variable=self.mode, style='white.TRadiobutton')
        self.meancircle_radiobutton.place(x=73, y=222)

        self.clusters_radiobutton = ttk.Radiobutton(root, text = 'Couleurs par clusters', value=3, variable=self.mode, style='white.TRadiobutton')
        self.clusters_radiobutton.place(x=73, y=241)

        self.fast_label = ttk.Label(root, text = 'Rapide', font='Arial 9 italic', style='white.TLabel')
        self.fast_label.place(x=73, y=290)

        self.quality_slider = Scale(root, from_=1, to=10, orient=HORIZONTAL, length=187, variable=self.quality, background='white')
        self.quality_slider.place(x=120, y=270)

        self.slow_label = ttk.Label(root, text = 'Lent', font='Arial 9 italic', style='white.TLabel')
        self.slow_label.place(x=315, y=290)

        self.quality_label = ttk.Label(root, text = 'Qualité', font='Arial 10', style='white.TLabel')
        self.quality_label.place(x=192, y=310)

        # MIDDLE RIGHT
        # Paramètres vidéo (header)
        # Image gauche (label)
        # Image droite (label)
        # Image gauche (image)
        # Image droite (image)
        # Temps (range slider)
        # Temps gauche (label)
        # Temps droite (label) OU utiliser les labels du range slider directement
        # Actualiser (button)
        # curseur images par heure (slider)
        # Images par heure (label)

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

        self.time_rangeslider = RangeSliderH(root, [self.start_time, self.end_time], Width=255, Height=45, padX=17, min_val=0, max_val=20, font_size=10,\
     line_s_color='black',line_color='black', bar_color_inner='white', bar_color_outer='black',  line_width=1, bar_radius=8, font_family='Arial', show_value=True,\
        valueSide='BOTTOM', digit_precision='.0f', imageL=self.handle, imageR=self.handle, auto=False)
        self.time_rangeslider.place(x=400, y=180)

        self.refresh_button = ttk.Button(root, text = 'Actualiser', width=10)
        self.refresh_button.place(x=400, y=225)

        self.large_label = ttk.Label(root, text = 'Gros', font='Arial 9 italic', style='white.TLabel')
        self.large_label.place(x=400, y=290)

        self.imagesperhour_slider = Scale(root, from_=500, to=2500, orient=HORIZONTAL, length=187, variable=self.imagesperhour, background='white')
        self.imagesperhour_slider.place(x=433, y=270)

        self.thin_label = ttk.Label(root, text = 'Fin', font='Arial 9 italic', style='white.TLabel')
        self.thin_label.place(x=628, y=290)

        self.imagesperhour_label = ttk.Label(root, text = 'Images par heure', font='Arial 10', style='white.TLabel')
        self.imagesperhour_label.place(x=480, y=310)


        # BOTTOM
        # Lancer le traitement (button)
        # Annuler (button)
        # Barre de progression (progressbar)
        # images traitées (text)

        self.begin_button = ttk.Button(root, text = 'Lancer le traitement', width=20)
        self.begin_button.place(x=300, y=350)

        self.progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=574, mode='determinate', maximum=self.images_to_compute, variable=self.progress)
        self.progressbar.place(x=73, y=390)

        self.info_text = Text(root, width=81, height=2, font='Arial 10')
        self.info_text.place(x=75, y=420)


    def load_film(self):
        self.selectfile_entry.config(state='normal')
        self.film_path = filedialog.askopenfilename(title = "Choisir un fichier", filetypes = (("Video files", "*.mp4"), ("all files", "*.*")))
        self.selectfile_entry.delete(0, END)
        self.selectfile_entry.insert(0, self.film_path)
        # check if the file is valid :

        # disable entry
        self.selectfile_entry.config(state='readonly')

        # log information in the text box
        self.info_text.insert(INSERT, 'Fichier vidéo chargé : ' + self.film_path +' \n')

    def refresh_preview(self):
        # get the first image at the start time
        # get the last image at the end time
        # update the images
        pass




app = Fenetre()