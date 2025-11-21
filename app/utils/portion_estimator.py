from ultralytics import YOLO
from PIL import Image
import json
import os

# ============================================================================
# FOOD DATABASE - Average Weight (grams)
# ============================================================================

FOOD_DATABASE = {
    "appalam": 15,
    "appam": 50,
    "banana": 120,
    "boiled egg": 50,
    "butter milk": 200,
    "channa masala": 180,
    "chicken 65": 150,
    "dosa": 86,
    "gravy": 200,
    "idiyappam": 100,
    "idly": 105,
    "kaara chutney": 40,
    "kesari": 100,
    "koozh": 150,
    "kuruma": 180,
    "masiyal": 100,
    "medu vadai": 65,
    "moor kolambu": 200,
    "mushroom briyani": 280,
    "paal kolukattai": 50,
    "paneer briyani": 300,
    "paniyaram": 40,
    "parupu vadai": 60,
    "payasam": 100,
    "pickle": 30,
    "pidi kolukattai": 45,
    "podi": 20,
    "pongal": 180,
    "poori": 60,
    "poorna kolukattai": 50,
    "pulisatham": 150,
    "puthina chutney": 35,
    "raita": 100,
    "rasam": 150,
    "salad": 120,
    "sambar": 140,
    "satham": 180,
    "soup": 200,
    "tea": 150,
    "thayir": 100,
    "thengai chutney": 40,
    "thovaiyal": 80,
    "uthapam": 90,
}

# ============================================================================
# MODEL PATH HELPER
# ============================================================================

def find_model_path():
   
    # Get the directory where this script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Model should be in models/food_detection.pt
    model_path = os.path.join(script_dir, "models", "food_detection.pt")
    
    if os.path.exists(model_path):
        print(f"✓ Model found at: {model_path}")
        return model_path
    
    # Fallback: check for best.pt in models folder
    model_path_alt = os.path.join(script_dir, "models", "best.pt")
    if os.path.exists(model_path_alt):
        print(f"✓ Model found at: {model_path_alt}")
        return model_path_alt
    
    print(f"✗ Model not found at: {os.path.join(script_dir, 'models')}")
    print(f"  Please place best.pt in: {os.path.join(script_dir, 'models', 'food_detection.pt')}")
    
    return None

# ============================================================================
# GRAM CALCULATION
# ============================================================================

def calculate_grams_from_detection(food_name, confidence, bbox_area, img_width, img_height):
    """
    Convert YOLO detection to grams
    
    Args:
        food_name: Detected food name (from YOLO model)
        confidence: Detection confidence score (0-1)
        bbox_area: Bounding box area in pixels
        img_width: Image width
        img_height: Image height
        
    Returns:
        Dictionary with gram estimate
    """
    
    # Normalize area
    total_area = img_width * img_height
    normalized_area = bbox_area / total_area
    
    # Size multiplier based on normalized area
    if normalized_area < 0.10:
        multiplier = 0.6
        size = "small"
    elif normalized_area < 0.30:
        multiplier = 1.0
        size = "medium"
    else:
        multiplier = 1.4
        size = "large"
    
    # Confidence multiplier (80% to 120% based on confidence)
    conf_multiplier = 0.8 + (confidence * 0.4)
    
    # Get base weight from database
    base_weight = FOOD_DATABASE.get(food_name.lower().strip(), 100)
    
    # Calculate estimated grams
    estimated_grams = base_weight * multiplier * conf_multiplier
    
    return {
        "food_name": food_name,
        "confidence": round(confidence, 4),
        "estimated_grams": round(estimated_grams, 1),
        "size_category": size,
        "normalized_area": round(normalized_area, 4)
    }

# ============================================================================
# MAIN PIPELINE: IMAGE → DETECTIONS → GRAMS
# ============================================================================

def process_food_image(image_path, model_path=None):
    """
    Complete pipeline:
    1. Load image
    2. Run YOLO detection
    3. Convert each detection to grams
    4. Return JSON with results
    
    Args:
        image_path: Path to food image
        model_path: Path to detection.pt model (optional, will auto-find if None)
        
    Returns:
        Dictionary with all detections and grams
    """
    
    # Auto-find model if not provided
    if model_path is None:
        model_path = find_model_path()
        if model_path is None:
            raise FileNotFoundError(
                "Model file (best.pt) not found. "
                "Please place it in your project directory or provide the full path."
            )
    
    # Verify model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")
    
    print(f"Loading model from: {model_path}")
    
    # Load YOLO model
    model = YOLO(model_path)
    
    # Run detection
    print(f"Processing image: {image_path}")
    results = model.predict(source=image_path, conf=0.25, verbose=False)
    result = results[0]
    
    # Get image dimensions
    image = Image.open(image_path)
    img_width, img_height = image.size
    
    # Convert each detection to grams
    gram_results = []
    total_grams = 0
    
    for i in range(len(result.boxes)):
        detection_box = result.boxes[i]
        food_name = result.names[int(detection_box.cls.item())].lower().strip()
        confidence = detection_box.conf.item()
        
        # Get box coordinates
        x1, y1, x2, y2 = detection_box.xyxy[0]
        x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()
        
        # Calculate bounding box area
        width = x2 - x1
        height = y2 - y1
        bbox_area = width * height
        
        # Calculate grams
        gram_data = calculate_grams_from_detection(
            food_name, confidence, bbox_area, img_width, img_height
        )
        
        estimated_grams = gram_data["estimated_grams"]
        total_grams += estimated_grams
        
        gram_results.append({
            "detection_id": i + 1,
            "food_name": gram_data["food_name"],
            "confidence": gram_data["confidence"],
            "estimated_grams": gram_data["estimated_grams"],
            "size_category": gram_data["size_category"],
            "normalized_area": gram_data["normalized_area"],
            "bounding_box": {
                "x1": round(x1, 2),
                "y1": round(y1, 2),
                "x2": round(x2, 2),
                "y2": round(y2, 2),
                "width": round(width, 2),
                "height": round(height, 2)
            }
        })
    
    # Prepare output
    final_output = {
        "image_name": os.path.basename(image_path),
        "image_dimensions": {"width": img_width, "height": img_height},
        "detections_count": len(gram_results),
        "items": gram_results,
        "total_meal_grams": round(total_grams, 1),
        "status": "success"
    }
    
    return final_output

# ============================================================================
# TEST & USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage
    
    try:
        # Method 1: Auto-find model
        result = process_food_image("test_images/dosa.jpg")
        
        # Method 2: Specify model path (uncomment if auto-find fails)
        # result = process_food_image(test_image, model_path=r"C:\path\to\best.pt")
        
        # Print results
        print("\n" + "="*60)
        print("PORTION ESTIMATION RESULTS")
        print("="*60)
        print(json.dumps(result, indent=2))
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

