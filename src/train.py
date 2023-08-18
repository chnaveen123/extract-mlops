import os
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from src.model import build_model
from src.data_preprocessing import preprocess_dataset

def train(dataset_folder):
    # Load and preprocess the dataset
    images, labels = preprocess_dataset(dataset_folder)

    # Split the dataset into training and validation sets
    train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.15, random_state=42)

    # Build and compile the model
    output_shape = 5  # Adjust based on the number of attributes you want to predict
    model = build_model(output_shape)
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    # Train the model
    model.fit(train_images, train_labels, validation_data=(val_images, val_labels), epochs=10)

    return model

if __name__ == "__main__":
    trained_model = train("data")  # Pass your dataset folder here
    trained_model.save_weights("path/to/your/trained/model")
    print("Model trained and saved.")
