from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class FoodItem(BaseModel):
    food_name: str
    portion_grams: float
    calories: float
    protein: float
    carbs: float
    fat: float
    confidence: float
    bbox: List[int]

class MacroNutrients(BaseModel):
    protein: float
    carbs: float
    fat: float

class PredictionResponse(BaseModel):
    success: bool
    total_calories: float
    total_macros: MacroNutrients
    detected_foods: List[FoodItem]
    image_info: Dict[str, Any]

class PredictionHistory(BaseModel):
    prediction_id: str
    timestamp: datetime
    total_calories: float
    food_count: int

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None