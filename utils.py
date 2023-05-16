import numpy as np
import cv2 #pip install opencv-python
import colorsys
import time

#Description du document : 
#Code des fonctions (appelées dans le main) qui réalisent l'analyse colorimétrique du film
# et la création de l'image finale  

def avg_strip_HSV(img):
    """Récupère la teinte de couleur moyenne de l'image (accès par cv2) dans le système de couleur hsv 
    (en récupérant d'abord séparément la teinte moyenne en h, en s et en v) puis convertit l'identité 
    de la couleur dans le système RGB (avec la fonction cvtColor)

    Parameters
    ----------
    img : _type : ndarray
        une image du film en traitement

    Returns
    -------
    _avg_color_rgb_[0][0] : _type = (int, int, int)

        
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    avg_h = np.average(h)
    avg_s = np.average(s)
    avg_v = np.average(v)
    _avg_color_hsv = np.uint8([[[avg_h, avg_s, avg_v]]])
    _avg_color_rgb = cv2.cvtColor(_avg_color_hsv, cv2.COLOR_HSV2BGR)
    return _avg_color_rgb[0][0]

def avg_strip_RGB(img):
    """Retourne directement la valeur dans le système RGB de la couleur moyenne de l'image traitée

    Parameters
    ----------
    img : _type : ndarray
        une image du film en traitement

    Returns
    -------
    np.average(img, axis=(0,1)) : _type = (int, int, int)
        la couleur moyenne de l'image
    """
    return np.average(img, axis=(0,1))

def kmeans_strip(image, color_count=7, strip_height=100, compress=False):
    """Définiton du critère de clustering, calcul des couleurs prédominantes, création de la bande
    correspondant à la colorimétrie de l'image et ajout de la bande à l'image finale en cours de création.

    Parameters
    ----------
    image : _type : ndarray
        une image en traitement dans le film
    color_count : int, optional
        nombre de couleurs prédominantes souhaitées pour le calcul par clusters, par défaut 7
    strip_height : int, optional
        hauteur de la bande de l'image crée, par défaut 100
    compress : bool, optional
        permet éventuellement de redimensionner l'image, par défaut False

    Returns
    -------
    output_image : _type : ndarray (strip_height x 1 x 3)
        bande verticale
    """
    if compress : 
        image = cv2.resize(image, (240, 180))
    
    Z = image.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = color_count
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)

    labels, counts = np.unique(label, return_counts=True)

    total_pixels = image.shape[0] * image.shape[1]
    heights = np.uint8(counts * strip_height / total_pixels)

    # make strip
    output_image = np.zeros((strip_height, 1, 3), np.uint8) # hauteur x largeur x 3 (BGR)

    mt = []
    for i in range(K):
        mt.append(  ((center[i][0], center[i][1], center[i][2]), heights[i])    )

    # sort mt by hue
    mt = sorted(mt, key=lambda x: colorsys.rgb_to_hsv(x[0][0], x[0][1], x[0][2])[2], reverse=True)

    last_height = 0
    for i in range(K):
        height = mt[i][1]
        output_image[last_height:last_height+height, 0] = (mt[i][0][0], mt[i][0][1], mt[i][0][2])
        last_height+=height

    output_image = cv2.flip(output_image, 0)
    
    return output_image

# duplicate of mainmenu.py, used in archive files

def process_kmeans(source, frame_count, output_height, logging=True, color_count=7, high_res=False, end_credits=7200):
    """
        Crée une image représentative de la colorimétrie chronologique du film obtenue par un processus de clustering

        Returns
        -------
        output_image : _type : ndarray
            image représentative de la colorimétrie chronologique du film obtenue par un processus de clustering (accès avec cv2)
            (ndarray de taille (hauteur, largeur, 3)
    """
    source_frame_count = int(source.get(cv2.CAP_PROP_FRAME_COUNT)) - end_credits
    frame_step = source_frame_count // frame_count
    
    output_image = np.zeros((output_height+4, frame_count, 3), np.uint8)

    for i in range(frame_count):
        frame_time_start = time.time()

        source.set(cv2.CAP_PROP_POS_FRAMES, frame_step * i)
        ret, frame = source.read()
        output_image[:, i] = kmeans_strip(image=frame, color_count=color_count, strip_height=output_height+4, compress=high_res)[:, 0]
        if logging:
            print(f"Frame {i+1}/{frame_count} done")
            print(f"FPS: {1/(time.time()-frame_time_start):.2f}")
    
    output_image = output_image[4:, :, :]

    return output_image

def process_avg(source, frame_count, output_height, logging=True, high_res=False, circle=False, end_credits=7200):

    """
    Crée une image représentative de la colorimétrie chronologique du film obtenue par un processus de moyenne
    
    Args:
        source (cv2.VideoCapture): source du film
        frame_count (int): nombre de frames à traiter
        output_height (int): hauteur de l'image de sortie
        logging (bool, optional): utilisé pour le debug. Defaults to True.
        high_res (bool, optional): compression de l'image pour améliorer les performances. Defaults to False.
        circle (bool, optional): image de sortie sous forme de cercles. Defaults to False.
        end_credits (int, optional): suppression des crédits (en images, à raison de 24/s). Defaults to 7200.

    Returns:
        _type_: ndarray (output_height x frame_count x 3)
            Image finale
    """

    source_frame_count = int(source.get(cv2.CAP_PROP_FRAME_COUNT)) - end_credits # remove end credits
    frame_step = source_frame_count // frame_count
    
    if not circle:
        output_image = np.zeros((output_height, frame_count, 3), np.uint8)

        for i in range(frame_count):
            source.set(cv2.CAP_PROP_POS_FRAMES, frame_step * i)
            frame = source.read()[1]

            if high_res:
                frame = cv2.resize(frame, (240, 180))

            output_image[:, i] = avg_strip_RGB(frame)  #average_frame_color_HSV(frame)

            if logging:
                print(f"Frame {i+1}/{frame_count} done")
    else:
        
        # fix aspect ratio to 4:3
        aspect = 1.333

        start_time = time.time()

        output_width = int(output_height / aspect)   

        diagonal = np.sqrt(output_height**2 + output_width**2)      # max number of 1px circles
        circle_width = int(diagonal / frame_count)                  
        
        output_image = np.zeros((output_height, output_width, 3), np.uint8)

        colors = []

        # get color list
        for i in range(frame_count):
            source.set(cv2.CAP_PROP_POS_FRAMES, frame_step * i)
            frame = source.read()[1]

            frame = cv2.resize(frame, (240, 120))

            colors.append(avg_strip_RGB(frame))  #average_frame_color_HSV(frame)
            if logging:
                print(f"Frame {i+1}/{frame_count} processed")

        print(f"    Colors computed in {time.time() - start_time}")

        # create circles for every color
        for i in reversed(range(frame_count)):
            cv2.circle(output_image, (0,0), i*circle_width, (colors[i].tolist()), -1) # color is BGR


    return output_image