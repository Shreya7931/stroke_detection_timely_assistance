from pydantic import BaseModel

class EmergencyContactSchema(BaseModel):
    phone_number: str
    name: str
    relationship: str
