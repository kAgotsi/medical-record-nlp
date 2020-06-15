import os
from flask import Flask, render_template, request,jsonify


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/",methods=['GET', 'POST'])
def index():
    return jsonify("ok")

@app.route("/process",methods=['GET', 'POST'])
def upload():
    print("request",request.files)
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    print("request",request.files)

    if not os.path.isdir(target):
        os.mkdir(target)
    
    save_image(request)
    #ocr()
    #extract_medical_dat
    
    
    medical_data = {'patient_name': 'Alice', 'doctor_name': 'Hammed'}
    return jsonify(medical_data)

"""
    save image in /image dicectory
    
    @return
        the file name
"""
def save_image(request):   
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return destination
   
"""
    process ocr
    
    @return
        text extracted from image
"""        
def ocr(imagefile):
    pass
    
"""
    extract medical data from ocr text
    @return
        data structure of medical data
"""    
def extract_medical_dat():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)