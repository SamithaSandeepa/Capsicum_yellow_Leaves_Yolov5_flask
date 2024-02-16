import cv2
import torch
from PIL import Image
import numpy as np
import os
import json
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model.pt')

def detect(image, image_name):
    try:

        print(f"Processing image: {image_name}")
        # Read the image using OpenCV
        image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)[..., ::-1]  # Convert BGR to RGB

        # Inference
        results = model([Image.fromarray(image)], size=640)  # batch of images

        # results.show()  # display results
        # Convert results to JSON format
        results_json = results.pandas().xyxy[0].to_json(orient='records')

        # Create a dictionary with image name, detection results, and image save path
        output_image_path = f'output_images/{os.path.splitext(image_name)[0]}_with_boxes.jpg'

        # Create a dictionary with image name and detection results
        image_results = {
            "image_name": image_name,  # You might want to replace this with the actual image name
            "detection_results": json.loads(results_json),
            "image_save_path": output_image_path  # Include image save path
        }

        # Draw bounding boxes on the image
        img_with_boxes = results.render()[0]

        # Save the image with bounding boxes
        output_image_path = f'output_images/{os.path.splitext(image_name)[0]}_with_boxes.jpg'
        cv2.imwrite(output_image_path, img_with_boxes[..., ::-1])  # Convert RGB to BGR for saving with OpenCV
        print(f"Image with bounding boxes saved to {output_image_path}")


        return image_results
    except Exception as e:
        return {"error": str(e)}
