import numpy as np
from PIL import Image
import cv2

def process_image(image: Image.Image) -> np.ndarray:
    
    #Process uploaded image for model inference
    # Convert PIL image to numpy array
    image_array = np.array(image)
    
    # Convert RGB to BGR if needed (for OpenCV compatibility)
    if len(image_array.shape) == 3 and image_array.shape[2] == 3:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Resize image to standard size 
    target_size = (640, 640)  # Common YOLO input size
    processed_image = cv2.resize(image_array, target_size)
    
    return processed_image

def normalize_image(image: np.ndarray) -> np.ndarray:

    #Normalize image for model input
    
    # Normalize pixel values to [0, 1]
    normalized = image.astype(np.float32) / 255.0
    return normalized

def validate_image(image: Image.Image) -> bool:
    
    # Validate uploaded image
    
    # Check image format
    if image.format not in ['JPEG', 'PNG', 'JPG']:
        return False
    
    # Check image size (not too small or too large)
    width, height = image.size
    if width < 100 or height < 100:
        return False
    
    if width > 4000 or height > 4000:
        return False
    
    return True
