from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}  # Prevent redefinition

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
