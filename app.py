import os
import sys 
from flask import Flask, render_template, request,jsonify
from engine import ocr,extract_medical_data
import json 
from pathlib import Path
import csv



app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/",methods=['GET', 'POST'])
def index():
    return jsonify("ok")

@app.route("/process",methods=['GET', 'POST'])
def upload():
    saved_image_name =""
    print("request",request.files)
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    print("request",request.files)

    if not os.path.isdir(target):
        os.mkdir(target)
        
    #save image
    saved_image_name = save_image(request,target)    
    print(saved_image_name)
    #ocr
    ocr_file = ocr(saved_image_name,APP_ROOT)
    
    #extract data
    data = extract_medical_data(ocr_file,APP_ROOT)
    
    target_ocr = os.path.join(APP_ROOT, 'medicaldata/')
    if not os.path.isdir(target):
        os.mkdir(target)
        pass
    
    simple_filename = Path(saved_image_name).stem
    
    ocr_path =  "/".join([target_ocr, simple_filename+".json"])
            
    file = open(ocr_path,"w")
    file.write(json.dumps(data))
    file.close()
    
    
    return jsonify(data)

"""
    save image in /image directory
    
    @return
        the file name
"""
def save_image(request,target):   
    destination=""
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return destination
   


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)