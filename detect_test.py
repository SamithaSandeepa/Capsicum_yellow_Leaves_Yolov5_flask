import cv2
import torch
from PIL import Image
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
import numpy as np
import os
import json
import pandas as pd


# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model.pt')

# Path to the folder containing images
folder_path = 'images'
output_folder = 'output_images'

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# List to store all results in JSON format
all_results_json = []

for image_file in image_files:
    # Construct the full path to the image
    image_path = os.path.join(folder_path, image_file)

    # Read the image using OpenCV
    image = cv2.imread(image_path)[..., ::-1]  # Convert BGR to RGB

    # Inference
    results = model([Image.fromarray(image)], size=640)  # batch of images

    # Convert results to JSON format
    results_json = results.pandas().xyxy[0].to_json(orient='records')

    # Create a dictionary with image name and detection results
    image_results = {
        "image_name": image_file,
        "detection_results": json.loads(results_json)
    }

    # Append the dictionary to the list
    all_results_json.append(image_results)

    # Draw bounding boxes on the image
    img_with_boxes = results.render()[0]

    # Save the image with bounding boxes
    output_image_path = os.path.join(output_folder, f'{os.path.splitext(image_file)[0]}_with_boxes.jpg')
    cv2.imwrite(output_image_path, img_with_boxes[..., ::-1])  # Convert RGB to BGR for saving with OpenCV

    # Filter results for class 'yellow' (assuming it's a specific class in your model)
    yellow_results_df = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == 'yellow']
    print(yellow_results_df)

# Save all results as a single JSON file
output_all_json_path = os.path.join(output_folder, 'all_results.json')
with open(output_all_json_path, 'w') as json_file:
    json.dump(all_results_json, json_file, indent=2)

print(f'All results saved to {output_all_json_path}')