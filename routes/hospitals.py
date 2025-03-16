from fastapi import APIRouter
from services.google_places import get_nearby_hospitals

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.get("/")
def fetch_hospitals(lat: float, lon: float):
    return get_nearby_hospitals(lat, lon)
