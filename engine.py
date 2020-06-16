import numpy as np
from PIL import Image
import tempfile
import pytesseract
import os
import sys
import re
from pathlib import Path


"""
    Extract text from image
    
    @Param
        filename : Image file name
    
    @return
        file containing extracted text
"""
def ocr(filename,APP_ROOT):
    target = os.path.join(APP_ROOT, 'ocr/')
    if not os.path.isdir(target):
        os.mkdir(target)
            
    text = str(((pytesseract.image_to_string(Image.open(filename),lang='fra')))) 
    simple_filename = Path(filename).stem
    ocr_path =  "/".join([target, simple_filename])
    file = open(ocr_path,"w")
    file.write(text)
    file.close()
    return ocr_path

"""
    extract medical data from ocr text
    
    @Param
        textFile : text file
    @return
        data structure of medical data
"""    
def extract_medical_data(textfile,APP_ROOT):
    print("app  root",APP_ROOT)
    target = os.path.join(APP_ROOT, 'medicaldata/')
    print("medical targer",target)
    if not os.path.isdir(target):
        os.mkdir(target)
        pass
        
    pattern_labels = os.path.join(APP_ROOT, 'dictionnary/medical_dict.txt')
    
    dictionnaireLines = open(pattern_labels, encoding="utf8").read()
    patterns = dictionnaireLines.split(",")
    print("text file",textfile)
    print(type(textfile))
    try:
        with open(textfile, encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:  
                print(line)
                if(re.findall ("(?<=Monsieur)\s\w+\s[a-zA-Z]+?\s[a-zA-Z]+?\s[a-zA-Z]+|(?<=Madame)\s\w+\s[a-zA-Z]+?\s[a-zA-Z]+?\s[a-zA-Z]+", line,re.IGNORECASE)):
                    nomEtPrenomPatient = re.findall ("(?<=Monsieur)\s\w+\s[a-zA-Z]+?\s[a-zA-Z]+?\s[a-zA-Z]+|(?<=Madame)\s\w+\s[a-zA-Z]+?\s[a-zA-Z]+?\s[a-zA-Z]+", line,re.IGNORECASE)
                    print(nomEtPrenomPatient,"\n")
                for pattern in patterns:
                    if (pattern in line):
                        if re.search(pattern, line, re.I):
                            valeurItems = re.findall ("<?\d\d?.+[0-9]*", line)
                            print(pattern,valeurItems,"\n")
    except IOError: 
        print("Le fichier pas etre ouvert")          
                
    pass


