import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Define image size and data path
data_path = 'Data'  # Root folder where gesture folders are
img_size = 300

# Initialize lists to hold images and labels
images = []
labels = []

# Loop through each folder in the dataset (e.g., "Thank_you", "Hello", etc.)
for class_folder in os.listdir(r"C:\Users\dasar\OneDrive\Desktop\asl\Data"):
    class_path = os.path.join(r"C:\Users\dasar\OneDrive\Desktop\asl\Data", class_folder)
    if os.path.isdir(class_path):
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)  # Read the image
            img = cv2.resize(img, (img_size, img_size))  # Resize the image
            img = img / 255.0  # Normalize to [0, 1]

            images.append(img)  # Append image to the list
            labels.append(class_folder)  # Append label based on the folder name

# Convert lists to numpy arrays
images = np.array(images)
labels = np.array(labels)

# Encode the labels (e.g., "Thank_you" -> 0, "Hello" -> 1, etc.)
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]}, Validation set size: {X_val.shape[0]}")
