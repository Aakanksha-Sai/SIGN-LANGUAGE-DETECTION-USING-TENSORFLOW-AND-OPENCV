import cv2
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Define image size and path to your dataset
img_size = 300
dataset_path = "Data"  # Path to your dataset directory

# Data Augmentation for better generalization
datagen = ImageDataGenerator(
    rescale=1./255,             # Normalize pixel values to [0, 1]
    rotation_range=20,          # Random rotations
    width_shift_range=0.2,      # Horizontal shift
    height_shift_range=0.2,     # Vertical shift
    shear_range=0.2,            # Shearing
    zoom_range=0.2,             # Zooming
    horizontal_flip=True,       # Horizontal flipping
    validation_split=0.2        # Split data into training (80%) and validation (20%)
)

# Load training data
train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=32,
    class_mode='sparse',
    subset='training'           # Use training subset
)

# Load validation data
val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=32,
    class_mode='sparse',
    subset='validation'         # Use validation subset
)

# Print the class labels (folder names)
print("Class indices:", train_data.class_indices)

# Define the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Dropout to prevent overfitting
    Dense(len(train_data.class_indices), activation='softmax')  # Output layer for classification
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Print the model summary to verify the architecture
model.summary()

# Callbacks: Save the best model and stop training early if no improvement
checkpoint = ModelCheckpoint('asl_model_best1.keras', save_best_only=True, monitor='val_loss', mode='min', verbose=1)
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)

# Train the model using the data generator
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=30,                 # Increased epochs for better learning
    callbacks=[checkpoint, early_stop]
)

# Save the final trained model
model.save("asl_model_final1.h5")
print("Model training complete and saved!")
