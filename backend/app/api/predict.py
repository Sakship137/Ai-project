from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
from typing import List, Dict, Any
from app.utils.food_detection import detect_food
from app.utils.calorie_calculator import calculate_calories
from app.utils.image_processor import process_image
from app.database.storage import save_prediction_result

router = APIRouter()

@router.post("/predict")
async def predict_food(file: UploadFile = File(...)):
    """
    Main prediction endpoint that processes uploaded image and returns food detection results
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        processed_image = process_image(image)
        
        # Detect food items using YOLO
        detections = detect_food(processed_image)
        
        # Calculate calories and macros
        results = calculate_calories(detections)
        
        # Prepare response
        response_data = {
            "success": True,
            "total_calories": results["total_calories"],
            "total_macros": results["total_macros"],
            "detected_foods": results["food_items"],
            "image_info": {
                "width": image.width,
                "height": image.height,
                "format": image.format
            }
        }
        
        # Save to database
        await save_prediction_result(response_data)
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/history")
async def get_prediction_history():
    """
    Get user's prediction history
    """
    try:
        # This would fetch from database
        return {"message": "History endpoint - to be implemented with user authentication"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")