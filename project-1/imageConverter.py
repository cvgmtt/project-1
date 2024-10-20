import cv2
import numpy as np

image = cv2.imread("C:\\Users\\matte\\OneDrive\\Desktop\\project-1\\corrupted.image.png")

inizio_area_superiore = (0, 0)
fine_area_superiore = (713, 480)
inizio_area_inferiore = (0, 480)
fine_area_inferiore = (713, 960)

def correct_rolling_shift(image, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore):
    #individuo l'area superiore

    area_superiore = image[inizio_area_superiore[1]:fine_area_superiore[1], inizio_area_superiore[0]:fine_area_superiore[0]]

    #individuo l'area inferiore e la salvo 

    area_inferiore = image[inizio_area_inferiore[1]:fine_area_inferiore[1], inizio_area_inferiore[0]:fine_area_inferiore[0]].copy()

    #sposto verso il basso l'area superiore

    image[inizio_area_superiore[1]+480:fine_area_superiore[1]+480, inizio_area_superiore[0]:fine_area_superiore[0]] = area_superiore 

    #rendo nera la sezione superiore

    image[inizio_area_superiore[1]:fine_area_superiore[1], inizio_area_superiore[0]:fine_area_superiore[0]] = 0

    #reinserisco l'area ineferiore in posizione superiore

    image[0:0+(fine_area_inferiore[1]-inizio_area_inferiore[1]), 0:0+(fine_area_inferiore[0]-inizio_area_inferiore[0])] = area_inferiore


    return image

def correct_chromatic_aberration(image, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore):

    #controllo i valori attuali dei pixel forniti
    bgr_value1 = image[541, 128]
    bgr_value2 = image[267, 564]


    #riinizializziamo le variabili area_superiore e area inferiore
    area_superiore = image[inizio_area_superiore[1]:fine_area_superiore[1], inizio_area_superiore[0]:fine_area_superiore[0]]
    area_inferiore= image[inizio_area_inferiore[1]:fine_area_inferiore[1], inizio_area_inferiore[0]:fine_area_inferiore[0]]

    #modifichiamo la ''tonalità'' delle due aree

    #area inferiore: prendo il pixel nell'area inferiore, applico la formula minmax per trovare il valore del pixel in range 50-200 (197, 143,  52)
    #aggiungo la tonalità per arrivare al valore del pixel fornito in range 50-200

    tonalità = np.zeros_like(area_inferiore)
    tonalità[:,:] = [20, 0, 0]

    #aggiungo blu

    area_inferiore = cv2.add(area_inferiore, tonalità)

    #considero il rosso a parte perchè devo sottrarre
    red =  np.zeros_like(area_inferiore)
    red[:,:] = [0, 0, 35]
    area_inferiore = cv2.subtract(area_inferiore, red)

    #applico alla parte inferiore
    image[inizio_area_inferiore[1]:fine_area_inferiore[1], inizio_area_inferiore[0]:fine_area_inferiore[0]] = area_inferiore

    #ora stessa cosa per area superiore

    #valore del pixel in range 50-200 (74, 165, 191)

    tonalità = np.zeros_like(area_superiore)
    tonalità[:,:] = [0, 15, 0]

    #aggiungo verde

    area_superiore = cv2.add(area_superiore, tonalità)


    #considero il rosso il blu e il rosso a parte perchè devo sottrarre
    red_blue =  np.zeros_like(area_superiore)
    red_blue[:,:] = [12, 0, 40]
    area_superiore = cv2.subtract(area_superiore, red_blue)

    image[inizio_area_superiore[1]:fine_area_superiore[1], inizio_area_superiore[0]:fine_area_superiore[0]] = area_superiore

    #controllo ora il valore dei pixel

    bgr_value1 = image[541, 128]
    bgr_value2 = image[267, 564]

    #applico l'inverso  dell'algoritmo minmax per tornare ai valori di pixel dell'immagine originale

    image[:, :, 0] = np.clip(np.round((image[:, :, 0] - 50) * 1.7), 0, 255).astype(np.uint8)  
    image[:, :, 1] = np.clip((image[:, :, 1] -50) * 1.7, 0, 255)  
    image[:, :, 2] = np.clip(np.round((image[:, :, 2] - 50) * 1.7), 0, 255).astype(np.uint8)

    #controllo il valore dei pixel

    bgr_value1 = image[541, 128]
    bgr_value2 = image[267, 564]

    print('valori dei pixel riportati alla tonalità originale per valori 0-255:')
    print(bgr_value1)
    print(bgr_value2) 


    cv2.imwrite("C:\\Users\\matte\\OneDrive\\Desktop\\project-1\\original_image.png", image)

    return image


