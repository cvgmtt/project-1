import cv2
import numpy as np
from imageConverter import correct_rolling_shift, correct_chromatic_aberration
from edgeDetector import mask, find_contours

image = cv2.imread("C:\\Users\\matte\\OneDrive\\Desktop\\project-1\\corrupted.image.png")

inizio_area_superiore = (0, 0)
fine_area_superiore = (713, 480)
inizio_area_inferiore = (0, 480)
fine_area_inferiore = (713, 960)

def restore_original(image, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore):
    roll_shift_correction = correct_rolling_shift(image, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore)
    original_image = correct_chromatic_aberration(roll_shift_correction, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore)
    return original_image

def edge_detector(image):
    masked_imaged = mask(image)
    bounding_boxes = find_contours(masked_imaged, image)
    return bounding_boxes

def bounding_boxes_finder():
    restore_original(image, inizio_area_superiore, fine_area_superiore, inizio_area_inferiore, fine_area_inferiore)
    edge_detector(image)

bounding_boxes_finder()

