from flask import Flask, render_template, request
from src import extract
import pandas as pd
import os
app = Flask(__name__)
cwd = os.getcwd()
# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['document']
    document_type = request.form.get('document_type')
    if file:
        allowed_types = {'image/jpeg', 'image/png','images/jpg'}
        if file.content_type in allowed_types:
            file.save(os.path.join('static','images',file.filename)) # Save the uploaded file to a specific location
            img_path = os.path.join(cwd,'static','images',file.filename)
            result = extract.extract_informartion(document_type,img_path)
            #return 'Document uploaded successfully!'
            return render_template('result.html',result = result,document_type=document_type,filename=file.filename)
        
        
        
        
        else:
            return 'Please upload a valid image file (JPEG or PNG).'
    else:
        return 'No document uploaded.'

if __name__ == '__main__':
    app.run(debug=True)




   # "C:\Users\NC67322\Downloads\tesseract-ocr-w64-setup-5.3.1.20230401.exe"