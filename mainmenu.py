
import cv2 #pip install opencv-python
import os
import utils
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from RangeSlider import RangeSliderH
import numpy as np
import psutil #pip install psutil

class MenuPrincipal() :
    def __init__(self) :
        # Initialisation de la fenêtre racine
        self.root = Tk()

        # fond blanc
        self.root.configure(bg='white')

        # Attributs esthétiques de la fenêtre
        self.root.title('Menu principal')
        self.root.geometry('1280x720')

        # Film info

        self.film_path = ""
        self.n_film_frames = -1
        self.source = None

        # Processor settings

        self.output_height = IntVar(value=128)

        self.highres = IntVar(value=0)

        self.mode = IntVar(value=1)

        self.start_frame_number = IntVar(value=0)
        self.end_frame_number = IntVar(value=340000)

        self.frame_count = IntVar(value=150)

        self.progress = IntVar(value=0)

        # Styles

        self.radiostyle = ttk.Style()
        self.radiostyle.configure('white.TRadiobutton', background='white')

        self.labelstyle = ttk.Style()
        self.labelstyle.configure('white.TLabel', background='white')

        # Source images

        self.rectangle_8 = PhotoImage(file='resources/Rectangle_8.png')
        self.handle = PhotoImage(file='resources/handle.png')

        # Lancement des fonctions
        self.creer_widgets(self.root)
        self.root.mainloop()

    def creer_widgets(self, root):
        # TOP
        # Projet algo S4 (header)
        # version 1.0 (header)

        self.projectname_header = ttk.Label(root, text = 'Projet algo S4', font='Arial 28 bold', style='white.TLabel')
        self.projectname_header.place(x=541, y=4)

        self.projectversion_header = ttk.Label(root, text = 'version 1.0', font='Arial 19 italic', style='white.TLabel')
        self.projectversion_header.place(x=575, y=48)

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

        self.source_header = ttk.Label(root, text = 'Source', font='Arial 24 bold', style='white.TLabel')
        self.source_header.place(x=77, y=90)

        self.selectfile_entry = ttk.Entry(root, width = 24, font='Arial 19', background='white')
        self.selectfile_entry.place(x=77, y=150)
        self.selectfile_entry.insert(INSERT, "Sélectionner un fichier source")
        self.selectfile_entry.configure(state='readonly')

        self.selectfile_button = ttk.Button(root, text = '...', width=5, command=self.load_film)
        self.selectfile_button.place(x=430, y=155)

        self.highres_checkbox = ttk.Checkbutton(root, onvalue=1, offvalue=0, variable=self.highres)
        self.highres_checkbox.place(x=77, y=220)

        self.highres_label1 = ttk.Label(root, text = 'Haute résolution', font='Arial 20', style='white.TLabel')
        self.highres_label1.place(x=121, y=190)

        self.highres_label2 = ttk.Label(root, text = 'Sélectionner si la résolution du\n fichier source dépasse 480x360', font='Arial 19 italic', style='white.TLabel')
        self.highres_label2.place(x=116, y=230)

        self.processing_header = ttk.Label(root, text = 'Paramètres de traitement', font='Arial 22 bold', style='white.TLabel')
        self.processing_header.place(x=77, y=300)

        self.meanbands_radiobutton = Radiobutton(root, text = 'Moyenne RGB - Bandes', value=1, variable=self.mode, command=self.set_defaults, font='Arial 19')
        self.meanbands_radiobutton.place(x=77, y=345)

        self.meancircle_radiobutton = Radiobutton(root, text = 'Moyenne RGB - Cercles', value=2, variable=self.mode, command=self.set_defaults,font='Arial 19')
        self.meancircle_radiobutton.place(x=77, y=390)

        self.clusters_radiobutton = Radiobutton(root, text = 'Partitionnement', value=3, variable=self.mode, command=self.set_defaults, font='Arial 19')
        self.clusters_radiobutton.place(x=77, y=435)

        #self.fast_label = ttk.Label(root, text = 'Petite', font='Arial 9 italic', style='white.TLabel')
        #self.fast_label.place(x=73, y=290)

        self.output_height_slider = Scale(root, from_=100, to=1000, resolution=10, orient=HORIZONTAL, length=364, variable=self.output_height, background='white')
        self.output_height_slider.place(x=77, y=495)

        #self.slow_label = ttk.Label(root, text = 'Grande', font='Arial 9 italic', style='white.TLabel')
        #self.slow_label.place(x=315, y=290)

        self.quality_label = ttk.Label(root, text = 'Hauteur de l\'image', font='Arial 19', style='white.TLabel')
        self.quality_label.place(x=155, y=540)

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

        self.videosettings_header = ttk.Label(root, text = 'Paramètres vidéo', font='Arial 24 bold', style='white.TLabel')
        self.videosettings_header.place(x=940, y=90)

        self.leftimage_label = ttk.Label(root, text = 'Première image', font='Arial 19 italic', style='white.TLabel')
        self.leftimage_label.place(x=534, y=150)

        self.rightimage_label = ttk.Label(root, text = 'Dernière image', font='Arial 19 italic', style='white.TLabel')
        self.rightimage_label.place(x=877, y=150)

        self.leftimage_image = self.rectangle_8
        self.leftimage_label = ttk.Label(root, image=self.leftimage_image)
        self.leftimage_label.place(x=534, y=200)

        self.rightimage_image = self.rectangle_8
        self.rightimage_label = ttk.Label(root, image=self.rightimage_image)
        self.rightimage_label.place(x=883, y=200)

        self.time_rangeslider = RangeSliderH(root, [self.start_frame_number, self.end_frame_number], Width=596, Height=45, padX=25, min_val=0, max_val=self.end_frame_number.get(), font_size=10,\
     line_s_color='black',line_color='black', bar_color_inner='white', bar_color_outer='black',  line_width=5, bar_radius=8, font_family='Arial', show_value=True,\
        valueSide='BOTTOM', digit_precision='.0f', imageL=self.handle, imageR=self.handle, auto=False)
        self.time_rangeslider.place(x=578, y=390)

        self.refresh_button = Button(root, text = 'Actualiser', width=10, command=self.refresh_preview, font ='Arial 19')
        self.refresh_button.place(x=784, y=430)

        #self.large_label = ttk.Label(root, text = 'Gros', font='Arial 9 italic', style='white.TLabel')
        #self.large_label.place(x=400, y=290)

        self.imagecount_slider = Scale(root, from_=10, to=2500, resolution=10, orient=HORIZONTAL, length=534, variable=self.frame_count, background='white')
        self.imagecount_slider.place(x=612, y=495)

        #self.thin_label = ttk.Label(root, text = 'Fin', font='Arial 9 italic', style='white.TLabel')
        #self.thin_label.place(x=628, y=290)

        self.imagesperhour_label = ttk.Label(root, text = 'Images à traiter', font='Arial 19', style='white.TLabel')
        self.imagesperhour_label.place(x=800, y=540)


        # BOTTOM
        # Lancer le traitement (button)
        # Annuler (button)
        # Barre de progression (progressbar)
        # images traitées (text)

        self.begin_button = Button(root, text = 'Démarrer le traitement', width=30, command=self.process_film, font ='Arial 19')
        self.begin_button.place(x=422, y=580)

        self.progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=1126, mode='determinate', maximum=self.frame_count.get(), variable=self.progress)
        self.progressbar.place(x=77, y=640)

        self.info_text = Text(root, width=135, height=2, font='Arial 10', state="disabled")
        self.info_text.place(x=77, y=670)

        self.usage_text=  Text(root, width=11, height=1, font='Arial 19', state="disabled")
        self.usage_text.place(x=1045, y=670)
        self.write_info(self.usage_text, 'En attente ...') 

    def load_film(self):
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

        # update slider
        self.time_rangeslider.max_val=self.n_film_frames
        self.time_rangeslider.forceValues([0, self.n_film_frames])

        self.refresh_preview()

    def refresh_preview(self):
        if self.film_path == '':
            self.write_info(self.info_text, 'Erreur : Aucun fichier vidéo chargé\n')
            return
        
        # get the first image at the start time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get())
        print(self.start_frame_number.get())
        start_frame = self.source.read()[1]
        start_frame = cv2.resize(start_frame, (120, 60))

        # get the last image at the end time
        self.source.set(cv2.CAP_PROP_POS_FRAMES, self.end_frame_number.get()-1)
        print(self.end_frame_number.get())
        end_frame = self.source.read()[1]
        end_frame = cv2.resize(end_frame, (120, 60))

        # write images as files
        cv2.imwrite('resources/start_frame.png', start_frame)
        cv2.imwrite('resources/end_frame.png', end_frame)
        # update the images
        self.leftimage_image = PhotoImage(file='resources/start_frame.png')
        self.rightimage_image = PhotoImage(file='resources/end_frame.png')

        self.leftimage_label.config(image=self.leftimage_image)
        self.rightimage_label.config(image=self.rightimage_image)
        
    def set_defaults(self):
        # default values for each mode

        # Mode 1 : meanbands
        # Output height = 1024
        # Frame count = 1500

        # Mode 2 : meancircles
        # Output height = 512
        # Frame count = 350

        # Mode 3 : clusters
        # Output height = 1024
        # Frame count = 1500

        def1 = [300, 1500]
        def2 = [1024, 350]
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
        subject.config(state='normal')
        subject.insert(INSERT, text)
        subject.config(state='disabled')

    def delete_all_info(self, subject):
        subject.config(state='normal')
        subject.delete(1.0, END)
        subject.config(state='disabled')

    def process_avg(self, circle=False):
        height = self.output_height.get()
        frame_count = self.frame_count.get()

        if not circle:
            output_image = np.zeros((height, frame_count, 3), np.uint8)

            for i in range(frame_count):
                frame_start_time = time.time()

                self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
                frame = self.source.read()[1]

                if bool(self.highres.get()):
                    frame = cv2.resize(frame, (240, 180))

                output_image[:, i] = utils.avg_strip_RGB(frame)  #average_frame_color_HSV(frame)

                self.log_progress(i, frame_start_time)
        else:
            
            # fix aspect ratio to 16/9
            aspect = 1.7777777777777777    

            output_width = int(height / aspect)   

            diagonal = np.sqrt(height**2 + output_width**2)      # max number of 1px circles
            circle_width = int(diagonal / frame_count)                  
            
            output_image = np.zeros((height, output_width, 3), np.uint8)

            colors = []

            # get color list
            for i in range(frame_count):
                frame_start_time = time.time()

                self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
                frame = self.source.read()[1]

                frame = cv2.resize(frame, (240, 180))

                colors.append(utils.avg_strip_RGB(frame))  #average_frame_color_HSV(frame)
            
                self.log_progress(i, frame_start_time)

            # create circles for every color
            for i in reversed(range(frame_count)):
                cv2.circle(output_image, (0,0), i*circle_width, (colors[i].tolist()), -1) # color is BGR

        return output_image

    def process_kmeans(self):
        height = self.output_height.get()
        frame_count = self.frame_count.get()
        output_image = np.zeros((height+4, frame_count, 3), np.uint8)

        for i in range(frame_count):
            frame_start_time = time.time()

            self.source.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame_number.get() + (i*self.frame_step) )
            frame = self.source.read()[1]
            output_image[:, i] = utils.kmeans_strip(image=frame, color_count=7, strip_height=height+4, compress=bool(self.highres.get()))[:, 0]

            self.log_progress(i, frame_start_time)

        output_image = output_image[4:, :, :]

        return output_image
    
    def process_film(self):
        if self.film_path == "":
            self.write_info(self.info_text, "Erreur : Aucun fichier vidéo chargé\n")
            return

        out_path = filedialog.askdirectory(title = "Choisir un dossier de destination", mustexist=True, initialdir=os.path.expanduser('~\Videos'))

        if out_path == "":
            self.write_info(self.info_text, "Erreur : Aucun dossier de destination sélectionné\n")
            return
        
        self.disable_all()

        os.chdir(out_path)

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


        cv2.imwrite(f"output_image.jpg", output_image)

        self.delete_all_info(self.info_text)
        self.write_info(self.info_text, f"Image enregistrée dans {out_path}\n")
        self.write_info(self.info_text, f"Temps de traitement : {time.time()-start_time:.1f}s\n")

        # display image
        cv2.imshow("output", output_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        self.enable_all()
        self.reset_vars()     

    def disable_all(self):
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
        # reset variables
        # dunno what to add there
        self.progress.set(0)

    def log_progress(self, i, start_time):
            # notify progress
            self.progress.set(i+1)
            self.delete_all_info(self.info_text)
            self.delete_all_info(self.usage_text)

            self.write_info(self.info_text, f"Image {i+1}/{self.frame_count.get()} traitée\n")
            #self.write_info(self.info_text, f"FPS: {1/(time.time()-start_time):.1f}\n")

            self.write_info(self.usage_text, f"RAM: {psutil.virtual_memory()[2]}%\n")
            #self.write_info(self.usage_text, f"CPU: {cpu_usage}%\n")

            self.progressbar.update()
            self.info_text.update()
            self.usage_text.update()
    
<<<<<<< HEAD
    def open_info_window(self) :
        self.fen_info = ttk.Fen_info()
        self.fen_infos.creer_widgets(MenuPrincipal())
        self.titre = self.fen_infos.creer_liste_infos()[0]
=======
>>>>>>> 747d208e52291560020bc9fdfedb38f274013d19

    

app = MenuPrincipal()