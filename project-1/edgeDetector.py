import cv2
import numpy as np
import matplotlib.pyplot as plt


def mask(image):
    #importo l'immagine originale
    image = image[:, :, :3]

    #rimuovo possibili rumori dell'immagine
    dst = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)


    plt.subplot(122), plt.imshow(dst)

    #definisco una regione di interesse per applicare cambiamenti che aiuteranno nella edge detection solo in quest'area
    inizio_roi = (40, 135)
    fine_roi = (631, 645)

    roi_main = dst[inizio_roi[1]:fine_roi[1], inizio_roi[0]:fine_roi[0]]

    #rendo pienamente neri i pixel della striscia nera sul cono giallo
    black_limit = 50
    almost_black_mask = np.all(roi_main < black_limit, axis=2)

    roi_main[almost_black_mask] = [0, 0, 0]


    #creo la prima maschera per rendere nere parte delle striscie bianche sui coni, utilizzo il tool git+https://github.com/alkasm/colorfilters per trovare gli i valori hsv che mi servono

    hsv = cv2.cvtColor(roi_main, cv2.COLOR_BGR2HSV)

    lower_bound1 = np.array([0, 0, 211])  
    upper_bound1 = np.array([180, 118, 255]) 

    mask1 = cv2.inRange(hsv, lower_bound1, upper_bound1)

    target_bgr = np.array([0, 0, 0])

    modified_roi = roi_main.copy()
    modified_roi[mask1 != 0] = target_bgr

    #creo la seconda maschera per rendere neri i coni colorati, usando lo stesso metodo di prima ma valori hsv diversi
    lower_bound2 = np.array([0, 0, 0])  
    upper_bound2 = np.array([180, 118, 255])  


    mask2 = cv2.inRange(hsv, lower_bound2, upper_bound2)

    result = cv2.bitwise_and(modified_roi, modified_roi, mask=mask2)

    #creo altre due aree di interesse per rimuovere dal 'result' le rotelle delle sedie che creano rumore nell'immagine 

    inizio_roi1 = (0, 0)
    fine_roi1 = (501, 13)
    result[inizio_roi1[1]:fine_roi1[1], inizio_roi1[0]:fine_roi1[0]] = [255, 255, 255]
    result[:, 0] = [255, 255, 255]

    inizio_roi2 = (0, 10)
    fine_roi2 = (375, 28)
    result[inizio_roi2[1]:fine_roi2[1], inizio_roi2[0]:fine_roi2[0]] = [255, 255, 255]
    result[:, 0] = [255, 255, 255]

    #riporto l'roi modificata nell'immagine originale
    dst[inizio_roi[1]:fine_roi[1], inizio_roi[0]:fine_roi[0]] = result
    return dst



def find_contours(dst, image):
    #modifico l'immagine in gray scale e applico treshold binario e otsu
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #trovo i contorni dei coni
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #definisco dei parametri utili ad escludere alcune aree che creano rumore
    min_contour_area = 1000
    height, width = image.shape[:2]

    #creo il file sui quali saranno salvate le coordinate delle bounding boxes
    file_path = "C:\\Users\\matte\\OneDrive\\Desktop\\project-1\\bounding_boxes"
    cone_color = "blue"

    for contour in contours:
        area = cv2.contourArea(contour)
        
        #definisco un area minima necessaria
        if area > min_contour_area:

            x, y, w, h = cv2.boundingRect(contour)
            
            #elimino i contorni del bordo dell'immagine
            if x == 0 or y == 0 or x + w == width or y + h == height:

                continue
            
            #disegno i contorni
            cv2.drawContours(dst, [contour], -1, (0, 255, 0), 2)

            #disegno il rettangolo
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

            #segno le coordinate
            with open(file_path, 'a') as file:
                file.write(f"{cone_color}: ({x}, {y}, {x + w}, {y + h})\n")
                
            if cone_color == "blue":
                cone_color = "yellow" 
            else:
                cone_color = "orange"
    return file_path
        



