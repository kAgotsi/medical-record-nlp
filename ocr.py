import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import cv2
import numpy as np
import tempfile
import sys 
from pdf2image import convert_from_path 
import re
import os.path

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def process_image(url):
    #Recuperation de l'image
    image = _get_image(url)
    #Pretraitement de l'image
    image = process_image_for_ocr(image)
    #Creation d'un fichier temporaire et stockage du texte apres pretraitement
    fp = tempfile.TemporaryFile()
    fp.write(pytesseract.image_to_string(image))
    fp.close()    
    #return pytesseract.image_to_string(image)

def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))

    #Fonctions de Pretraitement d'images
def process_image_for_ocr(url):
    # TODO : Implement using opencv
    url = set_image_dpi(url)
    im_new = remove_noise_and_smooth(url)
    return im_new

def set_image_dpi(url):
    im = Image.open(url)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(url):
    img = cv2.imread(url, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image    
    
    
