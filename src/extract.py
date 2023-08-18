from flask import Flask, request, jsonify, render_template
from PIL import Image
from pytesseract import pytesseract
import pandas as pd
import os
import re
import spacy
import cv2
import json
#from app import flask_app
from tabulate import tabulate


# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract =  input("Please enter the path to the 'tesseract.exe': ")

#r"C:/Users/NC67322/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
nlp = spacy.load('en_core_web_sm')


def extract_given_name(text):

    # Use a custom regular expression to search for the given name

    name_pattern = r'Name:\s*([(A-Z)(a-z) ]*)'

    name_match = re.search(name_pattern, text)

    if name_match:

        return name_match.group(1).strip()


    # If the custom pattern does not find the name, fallback to spaCy's NER

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            return ent.text.strip()


    # If no name is found, return an empty string

    return ""

def extract_informartion(document_type,image_path):
    # Opening the image & storing it in an image object
    img = Image.open(image_path)
# Providing the tesseract executable
# location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract
# Passing the image object to image_to_string() function
# This function will extract the text from the image
    text = pytesseract.image_to_string(img)
    #text = pytesseract.image_to_string(img)
    processed_dict = {}
    if document_type=="PAN":
        text = text.split("\n\n")
        print(text)
        print("\n\n")
        processed_text = []
        for line in text:
            if line.count('Permanent') or line.count('Name'):
                processed_text.append(line)
                for line in processed_text:
                    data = line.split('\n')
                    key = data[0].split('/')[1] if len(data[0].split('/'))>1 else data[0]
                    processed_dict[key]=data[1]
        print(processed_dict)
    if document_type=="Aadhar":
        print(text)
        text = text.split("\n\n")
        print(text)
        print("\n\n")
        processed_text = []
        for line in text:
            names = re.findall(r'(?<=[a-z,][ ])([A-Z][a-z]*)', line)
            numbers = re.findall(r'\b\d\d\d\d\b',line)
            if len(names)>0 and len(names[0])>3:
                processed_dict['Name'] = "".join(names)
            if len(numbers)>2:
                processed_dict['Aadhar No'] = " ".join(numbers[:3])
            if line.count('DOB'):
                dob_text = line.split(':')
                processed_dict[dob_text[0].split('/')[1]] = dob_text[1].split('\n')[0]
        print(processed_dict)

    if document_type == "Passport":
        processed_dict = {}

        passport_number_pattern = r'[A-Z]{1}[0-9]{7}'
        passport_number_match = re.search(passport_number_pattern, text)
        if passport_number_match:
            processed_dict['Passport No'] = passport_number_match.group()

 
        # Extract Holder's Name using the custom function
        holder_name = extract_given_name(text)
        if holder_name:
            processed_dict['Name'] = holder_name

 
        # Load the spaCy English language model
        nlp = spacy.load('en_core_web_sm')

 
        # Process the text with spaCy to extract other attributes
        doc = nlp(text)


        for i, ent in enumerate(doc.ents):
            if ent.label_ == "GPE" and "Nationality" not in processed_dict:
                processed_dict['Nationality'] = ent.text.strip()
            elif ent.label_ == "DATE":
                if "DOB" not in processed_dict:
                    processed_dict['DOB'] = ent.text.strip()
                elif "Issue Date" not in processed_dict and "Expiry Date" not in processed_dict:
                    # We assume that the Issue Date comes before the Expiry Date in the text
                    if i < len(doc.ents) - 1:
                        next_ent = doc.ents[i + 1]
                        if next_ent.label_ == "DATE" and next_ent.text.strip() != processed_dict.get('DOB', ''):
                            processed_dict['Issue Date'] = ent.text.strip()
                        else:
                            processed_dict['Expiry Date'] = ent.text.strip()
                    else:
                        processed_dict['Expiry Date'] = ent.text.strip()
    

    
    if document_type == "DL":

        processed_dict = {}  

        lines = text.split("\n")

        # Process each line in the text

        for i in range(len(lines)):

            try:

                line = lines[i]

                if 'DL No' in line or 'Licence No.' in line:

                    key = 'DL No'

                    value = line.split(':')[1].strip()

                    processed_dict[key] = value[:-5]


                if 'DOB' in line or 'Date of Birth' in line:

                    key = 'DOB'

                    value = line.split(':')[1].strip()

                    processed_dict[key] = value[0:11]

 
                if 'Name' in line:

                    key = 'Name'

                    value = line.split(':')[1].strip()

                    processed_dict[key] = value    


                if 'Issue Date' in line:

                    key = 'Issue Date'

                    value = line.split(':')[1].strip()

                    processed_dict[key] = value[0:11]


                if 'Validity' in line:

                    key = 'Expiry Date'

                    value = line.split(':')[1].strip()

                    processed_dict[key] = value[0:11]    

            except IndexError:

                # Handle cases where the index is out of range

                pass



    with open(f"{document_type}_output.json", "w") as json_file:

        json.dump(processed_dict, json_file, indent=4)



    return processed_dict



#C:/Users/NC67322/AppData/Local/Programs/Tesseract-OCR/tesseract.exe
    



   


 

 


