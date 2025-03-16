from fastapi import APIRouter
from services.sms_alert import send_sms

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/send_sms/")
def alert_family(phone_number: str, message: str):
    send_sms(phone_number, message)
    return {"message": "Alert sent successfully!"}
