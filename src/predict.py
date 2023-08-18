import numpy as np
import tensorflow as tf
from src.model import build_model
from src.data_preprocessing import load_image

def predict_from_image(model, image_path):
    image = load_image(image_path)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    prediction = model.predict(image)
    return prediction

def main():
    # Load the trained model
    output_shape = 5  # Adjust based on the number of attributes you want to predict
    model = build_model(output_shape)
    model.load_weights("path/to/your/trained/model")

    # Make predictions on an image
    image_to_predict = "path/to/unseen/image.png"
    prediction = predict_from_image(model, image_to_predict)
    print("Prediction:", prediction)

if __name__ == "__main__":
    main()
