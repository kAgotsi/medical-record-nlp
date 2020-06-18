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
    
    data = {}
    medical_item_data ={}
    medical_data ={}
    all_medical_data =[]
    #counter for doctor and patient match
    doctor_match_counter = 0
    patient_match_conter = 0
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
        #with open('/home/kommit/Documents/cours/tx52/medical-record-nlp/ocr/output.txt', encoding="utf8") as f:
            lines = f.readlines()
            
            for line in lines:  
                #regex serch for patient and doctor
                patient_last_first_name_match = re.search ("(?P<title>(?:MR|MONSIEUR|MADEMOISELLE|MLLE|MADAME|MME) (?P<name>.*?)\s*$)", line, re.IGNORECASE)
                doctor_last_first_name_match = re.search ("(?P<title>(?:DR) (?P<name>.*?)\s*$)", line, re.IGNORECASE)
                
                if(patient_last_first_name_match):
                    print(patient_last_first_name_match.group(1).split("\n")[0])
                    #regex can match many patient and doctor so when filter then with counter and get the first
                    if patient_match_conter == 0: data['patient_name'] = patient_last_first_name_match.group(1).split("\n")[0] 
                    patient_match_conter +=1
                if(doctor_last_first_name_match):
                    print(doctor_last_first_name_match.group(1))
                    if doctor_match_counter == 0:data['doctor_name'] = doctor_last_first_name_match.group(1).split("\n")[0] 
                    doctor_match_counter +=1
                
                #regex search for medical entity 
                for pattern in patterns:
                    if re.search(pattern, line, re.I):                        
                        valeurItems = re.findall ("<?\d\d?.+[0-9]*", line)
                        print(pattern,valeurItems,"-----------------------\n")
                        str_valeur_items = list_to_str(valeurItems)
                        medical_item_data_match = re.search("^(\S+) (\S+) (\S+ \S+ \S+) ?(|(\S+))$",str_valeur_items)
                        if(medical_item_data_match):
                            group_len = len(medical_item_data_match.groups())
                            print(group_len,"************")
                            medical_item_data['code'] = pattern
                            medical_item_data['value'] = medical_item_data_match.group(1)
                            medical_item_data['unity'] = medical_item_data_match.group(2)
                            if group_len == 5 : medical_item_data['normal'] = medical_item_data_match.group(3)
                            medical_item_data['history'] = medical_item_data_match.group(4)                                
                            print('pattern',pattern) 
                            p = pattern  
                            #medical_data[pattern] = medical_item_data 
                            print("medicaldata",medical_data)  
                            all_medical_data.append(medical_item_data)
                            medical_item_data ={}
            print("all----------",all_medical_data,"all")
        data['medical_data'] = all_medical_data        
                                                
        print(data)
        return data
    except IOError: 
        print("Le fichier pas etre ouvert")          
                
    pass

def list_to_str(str_list):
   res =  ' '.join([str(elem) for elem in str_list]) 
   return res


