from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn
from datetime import datetime, timedelta

app = FastAPI()

class TripRequest(BaseModel):
    origin: str
    destination: str
    startDate: str
    endDate: str
    budget: float
    pax: int

@app.get("/health")
async def health():
    return {"ok": True}

# Optional: keep HEAD happy if you use wait-on without --http-get
@app.head("/health")
async def health_head():
    return Response(status_code=200)

@app.post("/plan")
async def plan(req: TripRequest):
    start = datetime.strptime(req.startDate, "%Y-%m-%d")
    end = datetime.strptime(req.endDate, "%Y-%m-%d")

    days = []
    d = start
    while d <= end:
        days.append({
            "date": d.strftime("%Y-%m-%d"),
            "activities": [
                {"name": f"Explore {req.destination}", "startTime": "09:00", "endTime": "11:00"},
                {"name": "Lunch", "startTime": "12:00", "endTime": "13:00", "cost": 20},
            ]
        })
        d += timedelta(days=1)

    return {
        "days": days,
        "summary": f"{len(days)}-day itinerary for {req.destination} (pax {req.pax})"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)
