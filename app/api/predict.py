from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
from typing import List, Dict, Any
from app.utils.food_detection import detect_food
from app.utils.calorie_calculator import calculate_calories, get_nutrition_for_food
from app.utils.image_processor import process_image, validate_image
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    """
    Main prediction endpoint that processes uploaded image and returns food detection results
    
    Returns:
    - success: Boolean indicating success
    - total_calories: Total calories for all detected foods
    - total_macros: Total protein, carbs, fat
    - detected_foods: List of detected food items with details
    - image_info: Image metadata
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image (JPEG, PNG, JPG)")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Validate image
        if not validate_image(image):
            raise HTTPException(
                status_code=400, 
                detail="Invalid image: must be JPEG/PNG, between 100x100 and 4000x4000 pixels"
            )
        
        logger.info(f"Processing image: {image.size}, format: {image.format}")
        
        # Process image for model
        processed_image = process_image(image)
        
        # Detect food items using YOLO
        detections = detect_food(processed_image)
        logger.info(f"Detected {len(detections)} food items")
        
        # Calculate calories and macros
        results = calculate_calories(detections)
        
        # Prepare response consistent with nutrition dashboard format
        simplified_items = []
        for item in results["food_items"]:
            simplified_items.append({
                "food_name": item["food_name"],
                "portion_grams": item["portion_grams"],
                "calories": item["calories"],
                "protein": item["protein"],
                "carbs": item["carbs"],
                "fat": item["fat"],
                "confidence": item["confidence"]
            })

        response_data = {
            "total_calories": results["total_calories"],
            "total_macros": results["total_macros"],
            "food_items": simplified_items
        }
        
        logger.info(f"Prediction successful: {results['total_calories']} kcal")
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/foods")
async def get_food_list():
    """
    Get list of all foods in the nutrition database
    """
    try:
        from app.utils.calorie_calculator import NUTRITION_DB
        
        foods = []
        for food_name, nutrition in NUTRITION_DB.items():
            foods.append({
                "name": food_name,
                "calories_per_100g": nutrition["calories"],
                "protein_per_100g": nutrition["protein"],
                "carbs_per_100g": nutrition["carbs"],
                "fat_per_100g": nutrition["fat"]
            })
        
        return {
            "success": True,
            "total_foods": len(foods),
            "foods": sorted(foods, key=lambda x: x["name"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch food list: {str(e)}")