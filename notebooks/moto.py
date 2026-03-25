from tkinter.constants import NONE

import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from keras.models import Sequential
from keras.layers import Dense

from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np

class Moto:

       

    def path_fold(self):
        """ Verifies the existence of the essential folders for the Med AI system. It checks for the training, test, and production folders within the data directory. If any of these folders are missing, it prints an error message specifying which folder is not found and returns None. If all folders are found successfully, it returns a dictionary with the paths to these folders for use in other parts of the code. """
        base_path = Path("data") # Using Path from pathlib for better path handling
        
        # 2. Create the list with the specific paths for the loop to work
        path_0 = [
            base_path / "training",
            base_path / "test",
            base_path / "production"
        ]
                
        try:
            # 3. The loop lists 'path_0' 
            for p in path_0:
                if not p.exists():
                    print(f"Erro: The File {p.name} folder was not found in: {p}")
                    return None
            
            print("All folders were found successfully.")
            
            # 4. Return the paths to be used in other parts of the code
            return {
                "training": path_0[0],
                "test": path_0[1],
                "production": path_0[2]
                    }
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def generation(self):
        """ Configures the ImageDataGenerators for both training and test datasets. The training generator includes data augmentation techniques to increase the diversity of the dataset, while the test generator only normalizes the images. Returns both generators for use in loading the data. """
        try:
            # Generator for Training: Applies transformations to increase the dataset
            train_datagen = ImageDataGenerator(
                rescale=1./255,         # Normalize: from [0, 255] to [0, 1]
                shear_range=0.2,        # Light deformation
                zoom_range=0.2,         # Random zoom
                horizontal_flip=True,   # Flip the image (useful if the organ doesn't have a fixed side)
                fill_mode='nearest'     # Preenche espaços vazios após rotações
            )

            # Generator for Test: ONLY normalizes (should not invent data during testing)
            test_datagen = ImageDataGenerator(rescale=1./255)

            print("Image generators configured successfully.")
            return train_datagen, test_datagen

        except Exception as e:
            print(f"Error occurred while configuring ImageDataGenerator: {e}")
            return None, None
    
    def load_data(self):
        """ Loads the training and test data using the configured ImageDataGenerators. It creates flows from the directories specified in the path_fold method. The training data is shuffled to prevent bias, while the test data is not shuffled to ensure consistent evaluation. Returns the training and test data generators. """
        try:
            # 1. Get the validated paths
            folder_0 = self.path_fold()
            if not folder_0:
                return None
            
            # 2. Get the configured generators
            gen_training, gen_test = self.generation()
            if not gen_training:
                return None

            # 3. Create the flow for the TRAINING data
            print("Loading training data...")
            training_data = gen_training.flow_from_directory(
                directory=str(folder_0['training']), # Convert the Path to a string
                target_size=(224, 224), # Target size of the input images
                batch_size=32, # Batch size for training
                class_mode='binary',
                shuffle=True # Shuffle to prevent the AI from biasing the order
            )

            # 4. Create the flow for the TEST data (using the test generator)
            print("Loading test data...")
            test_data = gen_test.flow_from_directory(
                directory=str(folder_0['test']),
                target_size=(224, 224),
                batch_size=32,
                class_mode='binary',
                shuffle=False # No need to shuffle test data, we want to evaluate in a consistent order
            )

            return training_data, test_data

        except Exception as e:
            print(f"Error loading image flow: {e}")
            return None, None
    
    
    
    
    
    
    
   

    def get_model(self): 
        """
        Defines the CNN architecture and loads pre-trained weights if available.
        
        Returns:
            tf.keras.Model: A compiled Keras model ready for evaluation or inference.
        """  
        try:
            
            _, test_data = self.load_data()
                
            if test_data is None:
                    print("Error: Could not load test data.")
                    return None
            
            # 1. Define the architecture of the model
            model = tf.keras.models.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(512, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])

            # 2. Define the path for the weights (you can change this to your actual path)
            weights1 = os.path.join("models", "my_trained_model.weights.h5") # Change to your actual path
            weights_path = Path(weights1) # Using Path for better path handling

            # 3. Verification: If the file exists, we load the weights. If not, we start with random weights (the model will be untrained, but at least it won't crash).
            if weights_path.exists():
                print(f"Weights found! Loading: {weights_path.name}")
                model.load_weights(str(weights_path)) # Convert Path to string for load_weights
            else:
                print("No previous weights found. Initializing model with random weights.")

            # 4. Compilation (Required for training or evaluation, the model needs to be compiled to define the loss function and metrics)
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )

                # 5. Evaluation
            print("Starting accuracy evaluation...")
                # The evaluate method returns [loss, accuracy]. The index [1] is the accuracy.
            loss_,precision = model.evaluate(test_data)
            print(f"The accuracy of the model on the test data is: {precision * 100:.2f}%")
            
            return model
        
        except Exception as e:
            print(f"Error building or loading the model: {e}")
            return None

    def rayx_analysis(self,path_image):
        """
        Preprocesses an input image and performs binary classification.
        
        Args:
            path_image (str): The path to the X-ray image file.
            
        Returns:
            float: A decimal value between 0 and 1 representing the prediction confidence.
        """
        model = self.get_model()
        try:
            # 1. Load and prepare the image
            # The target_size should be the same as used in training (224, 224)
            img = load_img(path_image, target_size=(224, 224))
            img_array = img_to_array(img)
            
            # 2. Expand dimensions (the model expects a 'batch', e.g., [1, 224, 224, 3])
            img_array = np.expand_dims(img_array, axis=0)
            
            # 3. Normalization (the same as used in training: rescale=1./255)
            img_array = img_array / 255.0

            # 4. Make the prediction
            preview = model.predict(img_array)
            
            # As we used 'sigmoid', the result is a value between 0 and 1
            # Usually: close to 0 = Normal, close to 1 = Diseased (or vice-versa, depending on your folders)
            resultado_decimal = float(preview[0][0]) # Converting from array to a simple decimal number
            
            return resultado_decimal

        except Exception as e:
            print(f"Error processing image for prediction: {e}")
            return None