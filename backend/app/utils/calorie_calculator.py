import csv
import os
from typing import List, Dict, Any

def load_nutrition_database(csv_path: str) -> Dict[str, Dict[str, float]]:
    """
    Load nutrition database from CSV file
    """
    nutrition_db = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_name = row['food_name'].lower().strip()
                nutrition_db[food_name] = {
                    'calories': float(row['calories_per_100g']),
                    'protein': float(row['protein_per_100g']),
                    'carbs': float(row['carbs_per_100g']),
                    'fat': float(row['fat_per_100g'])
                }
        print(f"Loaded {len(nutrition_db)} foods from nutrition database")
        return nutrition_db
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"Error loading nutrition database: {e}")
        return get_default_nutrition_db()

def get_default_nutrition_db() -> Dict[str, Dict[str, float]]:
    """Fallback nutrition database with all 43 South Indian foods"""
    return {
        "appalam": {"calories": 372, "protein": 14.1, "carbs": 58.4, "fat": 11.8},
        "appam": {"calories": 105, "protein": 2.1, "carbs": 20, "fat": 1.8},
        "banana": {"calories": 89, "protein": 1.1, "carbs": 22.8, "fat": 0.3},
        "boiled egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
        "butter milk": {"calories": 40, "protein": 3.1, "carbs": 4.6, "fat": 0.9},
        "channa masala": {"calories": 164, "protein": 8.9, "carbs": 27.4, "fat": 2.8},
        "chicken 65": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        "dosa": {"calories": 133, "protein": 4.5, "carbs": 18, "fat": 4.5},
        "gravy": {"calories": 150, "protein": 8, "carbs": 12, "fat": 8},
        "idiyappam": {"calories": 349, "protein": 8.5, "carbs": 78.2, "fat": 0.6},
        "idly": {"calories": 58, "protein": 2.8, "carbs": 8.9, "fat": 0.39},
        "kaara chutney": {"calories": 165, "protein": 2.5, "carbs": 6, "fat": 16},
        "kesari": {"calories": 320, "protein": 4.5, "carbs": 65, "fat": 6.8},
        "koozh": {"calories": 76, "protein": 2.1, "carbs": 13, "fat": 1.8},
        "kuruma": {"calories": 180, "protein": 8, "carbs": 12, "fat": 8},
        "masiyal": {"calories": 100, "protein": 3, "carbs": 15, "fat": 2},
        "medu vadai": {"calories": 245, "protein": 8, "carbs": 25, "fat": 14},
        "moor kolambu": {"calories": 85, "protein": 4.2, "carbs": 12, "fat": 2.8},
        "mushroom briyani": {"calories": 200, "protein": 6, "carbs": 35, "fat": 4},
        "paal kolukattai": {"calories": 98, "protein": 1.8, "carbs": 20, "fat": 1.2},
        "paneer briyani": {"calories": 300, "protein": 18, "carbs": 35, "fat": 12},
        "paniyaram": {"calories": 120, "protein": 4, "carbs": 16, "fat": 4},
        "parupu vadai": {"calories": 245, "protein": 8, "carbs": 25, "fat": 14},
        "payasam": {"calories": 180, "protein": 4.2, "carbs": 35, "fat": 3.8},
        "pickle": {"calories": 216, "protein": 2.6, "carbs": 23.4, "fat": 13.1},
        "pidi kolukattai": {"calories": 98, "protein": 1.8, "carbs": 20, "fat": 1.2},
        "podi": {"calories": 508, "protein": 26.1, "carbs": 28.1, "fat": 36.2},
        "pongal": {"calories": 156, "protein": 4.2, "carbs": 24, "fat": 5.1},
        "poori": {"calories": 297, "protein": 11, "carbs": 61, "fat": 3.7},
        "poorna kolukattai": {"calories": 98, "protein": 1.8, "carbs": 20, "fat": 1.2},
        "pulisatham": {"calories": 165, "protein": 3.8, "carbs": 32, "fat": 2.1},
        "puthina chutney": {"calories": 165, "protein": 2.5, "carbs": 6, "fat": 16},
        "raita": {"calories": 100, "protein": 3.1, "carbs": 14, "fat": 2.3},
        "rasam": {"calories": 45, "protein": 2.1, "carbs": 8, "fat": 0.8},
        "salad": {"calories": 25, "protein": 1.5, "carbs": 5, "fat": 0.2},
        "sambar": {"calories": 85, "protein": 4.2, "carbs": 12, "fat": 2.8},
        "satham": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
        "soup": {"calories": 45, "protein": 2.1, "carbs": 8, "fat": 0.8},
        "tea": {"calories": 1, "protein": 0.1, "carbs": 0.2, "fat": 0},
        "thayir": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        "thengai chutney": {"calories": 165, "protein": 2.5, "carbs": 6, "fat": 16},
        "thovaiyal": {"calories": 80, "protein": 3, "carbs": 15, "fat": 2},
        "uthapam": {"calories": 120, "protein": 4, "carbs": 16, "fat": 4}
    }

# Load nutrition database
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'nutrition_db.csv')
NUTRITION_DB = load_nutrition_database(CSV_PATH)

def estimate_portion_from_bbox(bbox: List[int], food_class: str, img_width: int = 640, img_height: int = 640) -> float:
    """
    Estimate portion size using Team Member 2's portion estimation logic
    Integrates with their FOOD_DATABASE and calculation methods
    """
    try:
        # Try to use Team Member 2's portion estimator
        from app.utils.portion_estimator import calculate_grams_from_detection
        
        x1, y1, x2, y2 = bbox
        bbox_area = (x2 - x1) * (y2 - y1)
        
        # Use Team Member 2's calculation method
        result = calculate_grams_from_detection(
            food_name=food_class,
            confidence=0.8,  # Default confidence
            bbox_area=bbox_area,
            img_width=img_width,
            img_height=img_height
        )
        
        return result["estimated_grams"]
        
    except Exception as e:
        print(f"Team Member 2's portion estimator not available, using fallback: {e}")
        
        # Fallback portion estimation
        x1, y1, x2, y2 = bbox
        area_pixels = (x2 - x1) * (y2 - y1)
        
        # Team Member 2's portion multipliers for all 43 foods
        portion_multipliers = {
            "appalam": 0.010,
            "appam": 0.015,
            "banana": 0.008,
            "boiled egg": 0.012,
            "butter milk": 0.025,
            "channa masala": 0.020,
            "chicken 65": 0.018,
            "dosa": 0.025,
            "gravy": 0.020,
            "idiyappam": 0.016,
            "idly": 0.008,
            "kaara chutney": 0.015,
            "kesari": 0.018,
            "koozh": 0.020,
            "kuruma": 0.020,
            "masiyal": 0.018,
            "medu vadai": 0.012,
            "moor kolambu": 0.020,
            "mushroom briyani": 0.030,
            "paal kolukattai": 0.012,
            "paneer briyani": 0.030,
            "paniyaram": 0.015,
            "parupu vadai": 0.012,
            "payasam": 0.018,
            "pickle": 0.008,
            "pidi kolukattai": 0.012,
            "podi": 0.005,
            "pongal": 0.020,
            "poori": 0.015,
            "poorna kolukattai": 0.012,
            "pulisatham": 0.020,
            "puthina chutney": 0.015,
            "raita": 0.018,
            "rasam": 0.022,
            "salad": 0.020,
            "sambar": 0.020,
            "satham": 0.020,
            "soup": 0.025,
            "tea": 0.030,
            "thayir": 0.018,
            "thengai chutney": 0.015,
            "thovaiyal": 0.015,
            "uthapam": 0.020
        }
        
        multiplier = portion_multipliers.get(food_class.lower(), 0.015)
        estimated_grams = area_pixels * multiplier
        
        # Reasonable bounds
        return max(10, min(estimated_grams, 500))

def calculate_calories(detections: List[Dict[str, Any]]) -> Dict[str, Any]:

   # Calculating total calories and macros from detected foods
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    food_items = []
    
    for detection in detections:
        food_class = detection["class_name"]
        bbox = detection["bbox"]
        confidence = detection["confidence"]
        
        # This line is now handled above
        # portion_grams already calculated
        
        # Estimate portion size with image dimensions
        portion_grams = estimate_portion_from_bbox(bbox, food_class, 640, 640)
        
        # Get nutrition info
        nutrition = get_nutrition_for_food(food_class)
        
        # Calculate calories and macros for this portion
        calories = (nutrition["calories"] * portion_grams) / 100
        protein = (nutrition["protein"] * portion_grams) / 100
        carbs = (nutrition["carbs"] * portion_grams) / 100
        fat = (nutrition["fat"] * portion_grams) / 100
        
        # Add to totals
        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat
        
        # Store individual food item data
        food_items.append({
            "food_name": food_class,
            "portion_grams": round(portion_grams, 1),
            "calories": round(calories, 1),
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1),
            "confidence": round(confidence, 2),
            "bbox": bbox
        })
    
    return {
        "total_calories": round(total_calories, 1),
        "total_macros": {
            "protein": round(total_protein, 1),
            "carbs": round(total_carbs, 1),
            "fat": round(total_fat, 1)
        },
        "food_items": food_items
    }

def get_nutrition_for_food(food_name: str) -> Dict[str, float]:
    """
    Get nutrition information for a specific food item
    """
    food_key = food_name.lower().strip()
    return NUTRITION_DB.get(food_key, NUTRITION_DB.get("rice", {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3}))

def update_nutrition_database(new_data: Dict[str, Dict[str, float]]) -> None:
    """
    Update nutrition database with new food items
    """
    global NUTRITION_DB
    NUTRITION_DB.update(new_data)
    print(f"Updated nutrition database with {len(new_data)} new items")
