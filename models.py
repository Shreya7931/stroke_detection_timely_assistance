from sqlalchemy import Column, String
from database import Base

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    phone_number = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    relationship = Column(String)
