from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.api.predict import router as predict_router

app = FastAPI(
    title="Smart Diet Recommender API",
    description="Backend API for food detection and calorie calculation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api", tags=["prediction"])

@app.on_event("startup")
async def startup_event():
    print("🚀 Smart Diet Recommender API Started")
    print("📊 Food Detection Model: Ready")
    print("🥗 Nutrition Database: Loaded")

@app.get("/")
async def root():
    return {
        "message": "Smart Diet Recommender API is running",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/predict",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api": "operational",
        "model": "ready"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)