import os
import cv2
import json 
import numpy as np

def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    image = cv2.resize(image, (224, 224))  # Resize to a common size
    image = image.astype(np.float32) / 255.0  # Normalize pixel values
    return image

def load_annotations(annotation_path):
    with open(annotation_path, 'r') as f:
        annotations = json.load(f)
    return annotations

def preprocess_dataset(dataset_folder):
    images = []
    labels = []

    for doc_type in os.listdir(dataset_folder):
        doc_type_folder = os.path.join(dataset_folder, doc_type)
        for image_name in os.listdir(doc_type_folder):
            image_path = os.path.join(doc_type_folder, image_name)
            annotation_path = os.path.splitext(image_path)[0] + '.json'
            
            if os.path.isfile(annotation_path):
                image = load_image(image_path)
                annotations = load_annotations(annotation_path)
                
                images.append(image)
                labels.append(annotations)
    
    return np.array(images), labels
