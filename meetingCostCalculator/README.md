To create a Proof of Concept (POC) for a meeting cost calculator using Python's FastAPI framework, we can build a simple web application that calculates the cost of a meeting based on the number of attendees, their hourly compensation, and the meeting duration. Below is a step-by-step guide to implementing this:

### Step 1: Set Up the FastAPI Environment

First, ensure you have Python installed. Then, install FastAPI and Uvicorn (an ASGI server to run the FastAPI app):

```bash
pip install fastapi uvicorn
```

### Step 2: Create the FastAPI Application

Create a new Python file, e.g., `meeting_cost_calculator.py`, and set up the FastAPI app:

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Attendee(BaseModel):
    hourly_compensation: float

class MeetingCostRequest(BaseModel):
    attendees: List[Attendee]
    duration_minutes: int

@app.post("/calculate-meeting-cost")
def calculate_meeting_cost(request: MeetingCostRequest):
    total_cost = sum(attendee.hourly_compensation for attendee in request.attendees) * (request.duration_minutes / 60)
    return {"total_meeting_cost": total_cost}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Meeting Cost Calculator!"}
```

### Step 3: Run the FastAPI Application

Run the FastAPI app using Uvicorn:

```bash
uvicorn meeting_cost_calculator:app --reload
```

The `--reload` flag enables auto-reloading, so the server will restart whenever you make changes to the code.

### Step 4: Test the API

You can test the API using tools like `curl`, Postman, or directly in your browser.

#### Example Request

Send a POST request to `http://127.0.0.1:8000/calculate-meeting-cost` with the following JSON body:

```json
{
  "attendees": [
    {"hourly_compensation": 100},
    {"hourly_compensation": 150},
    {"hourly_compensation": 200}
  ],
  "duration_minutes": 30
}
```

#### Example Response

The response will be:

```json
{
  "total_meeting_cost": 225.0
}
```

### Step 5: Enhance the POC (Optional)

You can enhance the POC by adding features such as:

1. **Executives' Premium**: Add a flag to indicate if an executive is present, which could multiply the cost by a certain factor.
2. **Currency Conversion**: Allow users to specify different currencies and convert the total cost.
3. **Historical Data**: Store past meeting costs in a database and provide analytics.

### Example Enhancement: Executives' Premium

Modify the `calculate_meeting_cost` function to include an executive premium:

```python
@app.post("/calculate-meeting-cost")
def calculate_meeting_cost(request: MeetingCostRequest, has_executive: bool = False):
    base_cost = sum(attendee.hourly_compensation for attendee in request.attendees) * (request.duration_minutes / 60)
    if has_executive:
        base_cost *= 1.5  # 50% premium for having an executive
    return {"total_meeting_cost": base_cost}
```

Now, you can include the `has_executive` parameter in your request:

```json
{
  "attendees": [
    {"hourly_compensation": 100},
    {"hourly_compensation": 150},
    {"hourly_compensation": 200}
  ],
  "duration_minutes": 30,
  "has_executive": true
}
```

The response will now account for the executive premium:

```json
{
  "total_meeting_cost": 337.5
}
```

### Conclusion

This POC demonstrates how to build a simple meeting cost calculator using FastAPI. You can further expand this application by adding more features, improving the UI, or integrating it with other systems. FastAPI's simplicity and performance make it an excellent choice for building such APIs quickly and efficiently.
