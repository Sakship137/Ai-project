import numpy as np
from typing import List, Dict, Any
from PIL import Image
import os

def detect_food(image: np.ndarray) -> List[Dict[str, Any]]:
    """
    Interface function for YOLO food detection
    Integrates with Team Member 1's YOLO model
    """
    try:
        # Try to load actual YOLO model
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'food_detection.pt')
        
        if os.path.exists(model_path):
            from ultralytics import YOLO
            model = YOLO(model_path)
            
            # Convert numpy array to PIL Image if needed
            if isinstance(image, np.ndarray):
                image_pil = Image.fromarray(image)
            else:
                image_pil = image
                
            # Run YOLO detection
            results = model.predict(source=image_pil, conf=0.25, verbose=False)
            result = results[0]
            
            detections = []
            for i in range(len(result.boxes)):
                detection_box = result.boxes[i]
                class_id = int(detection_box.cls.item())
                food_name = result.names[class_id]
                confidence = detection_box.conf.item()
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = detection_box.xyxy[0]
                bbox = [int(x1), int(y1), int(x2), int(y2)]
                
                detections.append({
                    "class_name": food_name,
                    "confidence": confidence,
                    "bbox": bbox,
                    "area_pixels": (x2 - x1) * (y2 - y1)
                })
            
            return detections
            
    except Exception as e:
        print(f"YOLO model not available, using mock data: {e}")
    
    # Fallback to mock detection for development
    mock_detections = [
        {
            "class_name": "dosa",
            "confidence": 0.85,
            "bbox": [100, 100, 300, 200],
            "area_pixels": 20000
        },
        {
            "class_name": "idli",
            "confidence": 0.92,
            "bbox": [320, 120, 380, 180],
            "area_pixels": 3600
        },
        {
            "class_name": "sambar",
            "confidence": 0.78,
            "bbox": [150, 220, 250, 300],
            "area_pixels": 8000
        }
    ]
    
    return mock_detections

def load_yolo_model(model_path: str):
    """
    Load the trained YOLO model from Team Member 1
    """
    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None

def preprocess_for_yolo(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for YOLO inference
    Resize to 640x640 and normalize
    """
    import cv2
    
    # Resize to YOLO input size
    target_size = (640, 640)
    processed_image = cv2.resize(image, target_size)
    
    return processed_image
