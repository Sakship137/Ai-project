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
    """Fallback nutrition database for South Indian foods"""
    return {
        "dosa": {"calories": 133, "protein": 4.5, "carbs": 18, "fat": 4.5},
        "idli": {"calories": 58, "protein": 2.8, "carbs": 8.9, "fat": 0.39},
        "vada": {"calories": 245, "protein": 8, "carbs": 25, "fat": 14},
        "sambar": {"calories": 85, "protein": 4.2, "carbs": 12, "fat": 2.8},
        "rasam": {"calories": 45, "protein": 2.1, "carbs": 8, "fat": 0.8},
        "coconut_chutney": {"calories": 165, "protein": 2.5, "carbs": 6, "fat": 16},
        "upma": {"calories": 76, "protein": 2.1, "carbs": 13, "fat": 1.8},
        "uttapam": {"calories": 120, "protein": 4, "carbs": 16, "fat": 4},
        "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3}
    }

# Load nutrition database
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'nutrition_db.csv')
NUTRITION_DB = load_nutrition_database(CSV_PATH)

def estimate_portion_from_bbox(bbox: List[int], food_class: str) -> float:
    
   # Estimate portion size in grams 
    x1, y1, x2, y2 = bbox
    area_pixels = (x2 - x1) * (y2 - y1)
    
    # Basic portion estimation based on food type and pixel area
    
    portion_multipliers = {
        "dosa": 0.025,
        "idli": 0.008,
        "vada": 0.012,
        "sambar": 0.020,
        "rasam": 0.022,
        "coconut_chutney": 0.015,
        "upma": 0.018,
        "uttapam": 0.020,
        "rice": 0.020,
        "appam": 0.015,
        "puttu": 0.016,
        "payasam": 0.018
    }
    
    multiplier = portion_multipliers.get(food_class, 0.015)
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
        
        # Estimate portion size
        portion_grams = estimate_portion_from_bbox(bbox, food_class)
        
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
