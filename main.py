from fastapi import FastAPI
from routes import hospitals, alerts

app = FastAPI(title="Timely Assistance API")

# Include Routes
app.include_router(hospitals.router)
app.include_router(alerts.router)

@app.get("/")
def home():
    return {"message": "Timely Assistance API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
