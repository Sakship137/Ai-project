import csv
import os
from typing import List, Dict, Any

# Nutrition database (calories per 100g)
NUTRITION_DB = {
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "paneer": {"calories": 265, "protein": 18, "carbs": 1.2, "fat": 20},
    "dal": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4},
    "roti": {"calories": 297, "protein": 11, "carbs": 61, "fat": 3.7},
    "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "vegetables": {"calories": 25, "protein": 1.5, "carbs": 5, "fat": 0.2}
}

def estimate_portion_from_bbox(bbox: List[int], food_class: str) -> float:
    
   # Estimate portion size in grams 
    x1, y1, x2, y2 = bbox
    area_pixels = (x2 - x1) * (y2 - y1)
    
    # Basic portion estimation based on food type and pixel area
    
    portion_multipliers = {
        "rice": 0.02,     
        "paneer": 0.015,   
        "dal": 0.018,      
        "roti": 0.012,     
        "chicken": 0.014,  
        "vegetables": 0.016 
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
        
        # nutrition info
        nutrition = NUTRITION_DB.get(food_class, NUTRITION_DB["vegetables"])
        
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

def load_nutrition_database(csv_path: str) -> Dict[str, Dict[str, float]]:
    """
  #  Load nutrition database from CSV file
   
   nutrition_db = {}
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nutrition_db[row['food_name']] = {
                    'calories': float(row['calories_per_100g']),
                    'protein': float(row['protein_per_100g']),
                    'carbs': float(row['carbs_per_100g']),
                    'fat': float(row['fat_per_100g'])
                }
    except FileNotFoundError:
        print(f"Nutrition database file not found: {csv_path}")
        return NUTRITION_DB
    
    return nutrition_db
