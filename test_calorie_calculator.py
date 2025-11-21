#!/usr/bin/env python3
"""
Test script for calorie calculator
"""
from app.utils.calorie_calculator import calculate_calories, get_nutrition_for_food

# Mock detection data for South Indian foods testing
test_detections = [
    {
        "class_name": "dosa",
        "confidence": 0.85,
        "bbox": [100, 100, 300, 200]
    },
    {
        "class_name": "idly",
        "confidence": 0.92,
        "bbox": [320, 120, 380, 180]
    },
    {
        "class_name": "sambar",
        "confidence": 0.78,
        "bbox": [150, 220, 250, 300]
    },
    {
        "class_name": "paneer briyani",
        "confidence": 0.88,
        "bbox": [200, 300, 400, 450]
    }
]

def test_calorie_calculation():
    """Test the calorie calculation function"""
    print("Testing calorie calculation...")
    
    # Test individual nutrition lookup
    rice_nutrition = get_nutrition_for_food("rice")
    print(f"Rice nutrition: {rice_nutrition}")
    
    # Test full calculation
    results = calculate_calories(test_detections)
    
    print("\n=== Calorie Calculation Results ===")
    print(f"Total Calories: {results['total_calories']}")
    print(f"Total Macros: {results['total_macros']}")
    print("\nDetected Foods:")
    
    for food in results['food_items']:
        print(f"- {food['food_name']}: {food['portion_grams']}g = {food['calories']} kcal")
        print(f"  Protein: {food['protein']}g, Carbs: {food['carbs']}g, Fat: {food['fat']}g")
    
    return results

if __name__ == "__main__":
    test_calorie_calculation()