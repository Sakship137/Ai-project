#!/usr/bin/env python3
"""
Comprehensive test script for Smart Diet Recommender Backend
Tests all core functionality without database dependencies
"""
import requests
import json
import sys
import os
from PIL import Image
import io
import numpy as np

# API base URL
BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image"""
    # Create a 640x640 RGB image with random colors
    img = Image.new('RGB', (640, 640), color=(200, 150, 100))
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Health check PASSED")
            return True
        else:
            print("❌ Health check FAILED")
            return False
    except Exception as e:
        print(f"❌ Health check ERROR: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Root Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Root endpoint PASSED")
            return True
        else:
            print("❌ Root endpoint FAILED")
            return False
    except Exception as e:
        print(f"❌ Root endpoint ERROR: {e}")
        return False

def test_food_list_endpoint():
    """Test the food list endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Food List Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/foods")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Foods: {data['total_foods']}")
            print(f"Sample Foods (first 5):")
            for food in data['foods'][:5]:
                print(f"  - {food['name']}: {food['calories_per_100g']} kcal/100g")
            print("✅ Food list endpoint PASSED")
            return True
        else:
            print(f"❌ Food list endpoint FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Food list endpoint ERROR: {e}")
        return False

def test_predict_endpoint():
    """Test the prediction endpoint with a test image"""
    print("\n" + "="*60)
    print("TEST 4: Prediction Endpoint")
    print("="*60)
    
    try:
        # Create test image
        test_img = create_test_image()
        
        # Prepare file upload
        files = {'file': ('test_food.jpg', test_img, 'image/jpeg')}
        
        # Make request
        response = requests.post(f"{BASE_URL}/api/predict", files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Prediction SUCCESSFUL")
            print(f"\nResults:")
            print(f"  Total Calories: {data['total_calories']} kcal")
            print(f"  Total Protein: {data['total_macros']['protein']}g")
            print(f"  Total Carbs: {data['total_macros']['carbs']}g")
            print(f"  Total Fat: {data['total_macros']['fat']}g")
            print(f"  Detected Foods: {data['detection_count']}")
            
            print(f"\n  Food Items:")
            for food in data['detected_foods']:
                print(f"    - {food['food_name']}: {food['portion_grams']}g = {food['calories']} kcal")
                print(f"      Confidence: {food['confidence']:.2f}")
            
            print("\n✅ Prediction endpoint PASSED")
            return True
        else:
            print(f"❌ Prediction endpoint FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction endpoint ERROR: {e}")
        return False

def test_invalid_file():
    """Test prediction with invalid file type"""
    print("\n" + "="*60)
    print("TEST 5: Invalid File Type (Error Handling)")
    print("="*60)
    
    try:
        # Create a text file instead of an image
        files = {'file': ('test.txt', b'This is not an image', 'text/plain')}
        
        response = requests.post(f"{BASE_URL}/api/predict", files=files)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print(f"Error Message: {response.json()['detail']}")
            print("✅ Error handling PASSED (correctly rejected non-image)")
            return True
        else:
            print("❌ Error handling FAILED (should reject non-image files)")
            return False
    except Exception as e:
        print(f"❌ Error handling test ERROR: {e}")
        return False

def test_nutrition_calculation():
    """Test the nutrition calculation module directly"""
    print("\n" + "="*60)
    print("TEST 6: Nutrition Calculation Module")
    print("="*60)
    
    try:
        from app.utils.calorie_calculator import calculate_calories, get_nutrition_for_food
        
        # Test nutrition lookup
        dosa_nutrition = get_nutrition_for_food("dosa")
        print(f"Dosa nutrition (per 100g):")
        print(f"  Calories: {dosa_nutrition['calories']} kcal")
        print(f"  Protein: {dosa_nutrition['protein']}g")
        print(f"  Carbs: {dosa_nutrition['carbs']}g")
        print(f"  Fat: {dosa_nutrition['fat']}g")
        
        # Test calorie calculation
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
            }
        ]
        
        results = calculate_calories(test_detections)
        print(f"\nTest meal calculation:")
        print(f"  Total Calories: {results['total_calories']} kcal")
        print(f"  Food Items: {len(results['food_items'])}")
        
        print("\n✅ Nutrition calculation PASSED")
        return True
    except Exception as e:
        print(f"❌ Nutrition calculation ERROR: {e}")
        return False

def test_portion_estimator():
    """Test the portion estimation module"""
    print("\n" + "="*60)
    print("TEST 7: Portion Estimation Module")
    print("="*60)
    
    try:
        from app.utils.portion_estimator import calculate_grams_from_detection, FOOD_DATABASE
        
        # Test portion calculation
        result = calculate_grams_from_detection(
            food_name="dosa",
            confidence=0.85,
            bbox_area=20000,
            img_width=640,
            img_height=640
        )
        
        print(f"Portion estimation for dosa:")
        print(f"  Estimated grams: {result['estimated_grams']}g")
        print(f"  Size category: {result['size_category']}")
        print(f"  Confidence: {result['confidence']}")
        
        print(f"\nFood database entries: {len(FOOD_DATABASE)}")
        print(f"Sample entries:")
        for food in list(FOOD_DATABASE.keys())[:5]:
            print(f"  - {food}: {FOOD_DATABASE[food]}g (average)")
        
        print("\n✅ Portion estimation PASSED")
        return True
    except Exception as e:
        print(f"❌ Portion estimation ERROR: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*70)
    print("🥗 SMART DIET RECOMMENDER - BACKEND TEST SUITE")
    print("="*70)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Food List", test_food_list_endpoint),
        ("Prediction Endpoint", test_predict_endpoint),
        ("Invalid File Handling", test_invalid_file),
        ("Nutrition Calculation", test_nutrition_calculation),
        ("Portion Estimation", test_portion_estimator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

