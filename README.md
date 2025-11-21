# Smart Diet Recommender - Backend API

This is the FastAPI backend that connects the ML model with the frontend, handling image uploads, food detection, calorie calculation, and data storage.

## Features

- **Image Upload & Processing**: Handle image uploads and preprocessing
- **YOLO Integration**: Interface with Team Member 1's food detection model
- **Calorie Calculation**: Calculate calories and macros from detected foods
- **Database Storage**: Store prediction results in MongoDB
- **RESTful API**: Clean JSON API for frontend integration

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── predict.py          # Main prediction endpoint
│   ├── database/
│   │   ├── connection.py       # Database connection setup
│   │   └── storage.py          # Database operations
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── utils/
│   │   ├── calorie_calculator.py   # Calorie calculation logic
│   │   ├── food_detection.py       # YOLO interface
│   │   └── image_processor.py      # Image preprocessing
│   └── main.py                 # FastAPI application
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   ```bash
   copy .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run the Server**:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **API Documentation**:
   - Visit `http://localhost:8000/docs` for interactive API documentation
   - Visit `http://localhost:8000/redoc` for alternative documentation

## API Endpoints

### POST /api/predict
Upload an image and get food detection results with calorie information.

**Request**: Multipart form data with image file
**Response**:
```json
{
  "success": true,
  "total_calories": 450.2,
  "total_macros": {
    "protein": 18.5,
    "carbs": 65.2,
    "fat": 12.3
  },
  "detected_foods": [
    {
      "food_name": "rice",
      "portion_grams": 150.0,
      "calories": 195.0,
      "protein": 4.1,
      "carbs": 42.0,
      "fat": 0.5,
      "confidence": 0.85,
      "bbox": [100, 100, 200, 150]
    }
  ],
  "image_info": {
    "width": 640,
    "height": 480,
    "format": "JPEG"
  }
}
```

### GET /api/history
Get user's prediction history (requires authentication - to be implemented).

## Integration Points

### With ML Lead
- `app/utils/food_detection.py` - Interface for YOLO model
- Replace mock detection with actual YOLO inference
- Update `load_yolo_model()` function with provided model path

### With Data Manipulation
- `app/utils/calorie_calculator.py` - Nutrition database and portion estimation
- Replace `NUTRITION_DB` with CSV-based database
- Update `estimate_portion_from_bbox()` with refined logic

### With frontend
- API endpoints ready for frontend integration
- CORS enabled for cross-origin requests
- JSON responses formatted for easy frontend consumption

## Database Schema

### Predictions Collection
```json
{
  "prediction_id": "uuid",
  "timestamp": "datetime",
  "user_id": "string",
  "prediction_data": {
    "total_calories": "number",
    "detected_foods": "array",
    "image_info": "object"
  }
}
```

## Development Notes

- Mock data is used for development until other team members provide their components
- Database operations are optional - API works without MongoDB for testing
- Image validation ensures proper file types and sizes
- Error handling provides meaningful responses for debugging

## Next Steps

1. Integrate actual YOLO model from Team Member 1
2. Replace nutrition database with Team Member 2's CSV data
3. Implement user authentication and authorization
4. Add more sophisticated portion estimation algorithms
5. Implement caching for better performance
