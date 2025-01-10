from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import cv2
import numpy as np
from datetime import datetime, date
import uvicorn
import io
import uuid
import os
from pathlib import Path

# Create models
class FoodItem(BaseModel):
    food: str
    confidence: float
    calories: int

class MealEntry(BaseModel):
    id: str
    timestamp: datetime
    items: List[str]
    calories: int
    image_path: str

class DailySummary(BaseModel):
    date: date
    total_calories: int
    meal_count: int
    foods_eaten: List[str]

# Create FastAPI app
app = FastAPI(
    title="Food Calorie Tracker API",
    description="API for tracking calories through food images",
    version="1.0.0"
)

# Initialize storage
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class CalorieTrackerService:
    def __init__(self):
        self.food_database = {
            'apple': 95,
            'banana': 105,
            'sandwich': 350,
            'salad': 120,
            'pizza_slice': 285,
            'chicken_breast': 165
        }
        self.meal_history: List[MealEntry] = []

    async def process_image(self, image_data: bytes) -> List[FoodItem]:
        """Process the food image and identify items"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Could not decode image")
            
            # Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Simulate detection
            detected_foods = self.simulate_food_detection(image)
            return detected_foods
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")

    def simulate_food_detection(self, image: np.ndarray) -> List[FoodItem]:
        """Simulate food detection (would use ML model in production)"""
        import random
        
        detected_items = []
        food_items = list(self.food_database.keys())
        
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            food = random.choice(food_items)
            detected_items.append(
                FoodItem(
                    food=food,
                    confidence=random.uniform(0.75, 0.98),
                    calories=self.food_database[food]
                )
            )
            
        return detected_items

    def calculate_calories(self, detected_foods: List[FoodItem]) -> tuple[int, List[str]]:
        """Calculate total calories from detected foods"""
        total_calories = 0
        items = []
        
        for food in detected_foods:
            if food.confidence > 0.8:
                total_calories += food.calories
                items.append(food.food)
                
        return total_calories, items

# Initialize service
tracker_service = CalorieTrackerService()

# API Routes
@app.post("/meals/", response_model=MealEntry)
async def create_meal(file: UploadFile = File(...)):
    """Upload a food image and get calorie estimation"""
    try:
        # Read and save image
        image_data = await file.read()
        image_id = str(uuid.uuid4())
        image_path = UPLOAD_DIR / f"{image_id}.jpg"
        
        with open(image_path, "wb") as f:
            f.write(image_data)
        
        # Process image
        detected_foods = await tracker_service.process_image(image_data)
        total_calories, items = tracker_service.calculate_calories(detected_foods)
        
        # Create meal entry
        meal_entry = MealEntry(
            id=image_id,
            timestamp=datetime.now(),
            items=items,
            calories=total_calories,
            image_path=str(image_path)
        )
        
        tracker_service.meal_history.append(meal_entry)
        return meal_entry
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/meals/", response_model=List[MealEntry])
async def get_meals(start_date: Optional[date] = None, end_date: Optional[date] = None):
    """Get meal history with optional date filtering"""
    meals = tracker_service.meal_history
    
    if start_date:
        meals = [meal for meal in meals if meal.timestamp.date() >= start_date]
    if end_date:
        meals = [meal for meal in meals if meal.timestamp.date() <= end_date]
        
    return meals

@app.get("/meals/{meal_id}", response_model=MealEntry)
async def get_meal(meal_id: str):
    """Get specific meal by ID"""
    for meal in tracker_service.meal_history:
        if meal.id == meal_id:
            return meal
    raise HTTPException(status_code=404, detail="Meal not found")

@app.get("/summary/daily/", response_model=DailySummary)
async def get_daily_summary(date: Optional[date] = None):
    """Get calorie summary for a specific date"""
    if date is None:
        date = datetime.now().date()
        
    daily_meals = [
        meal for meal in tracker_service.meal_history 
        if meal.timestamp.date() == date
    ]
    
    return DailySummary(
        date=date,
        total_calories=sum(meal.calories for meal in daily_meals),
        meal_count=len(daily_meals),
        foods_eaten=[item for meal in daily_meals for item in meal.items]
    )

@app.get("/foods/", response_model=dict[str, int])
async def get_food_database():
    """Get the food database with calorie information"""
    return tracker_service.food_database

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
