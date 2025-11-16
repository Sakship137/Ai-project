from datetime import datetime
from typing import Dict, Any, List, Optional
from app.database.connection import get_database
import uuid

async def save_prediction_result(prediction_data: Dict[str, Any]) -> str:
    """
    Save prediction result to database
    """
    try:
        db = await get_database()
        if db is None:
            print("Database not available, skipping save")
            return "no-db"
        
        # Add metadata
        document = {
            "prediction_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow(),
            "prediction_data": prediction_data,
            "user_id": "anonymous"  # TODO: Add user authentication
        }
        
        # Insert into predictions collection
        result = await db.predictions.insert_one(document)
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"Failed to save prediction: {e}")
        return "error"

async def get_user_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get user's prediction history
    """
    try:
        db = await get_database()
        if db is None:
            return []
        
        cursor = db.predictions.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)
        
        history = []
        async for document in cursor:
            history.append({
                "prediction_id": document["prediction_id"],
                "timestamp": document["timestamp"],
                "total_calories": document["prediction_data"]["total_calories"],
                "food_count": len(document["prediction_data"]["detected_foods"])
            })
        
        return history
        
    except Exception as e:
        print(f"Failed to fetch history: {e}")
        return []

async def get_prediction_details(prediction_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed prediction data by ID
    """
    try:
        db = await get_database()
        if db is None:
            return None
        
        document = await db.predictions.find_one({"prediction_id": prediction_id})
        return document["prediction_data"] if document else None
        
    except Exception as e:
        print(f"Failed to fetch prediction details: {e}")
        return None