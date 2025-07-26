from sqlalchemy import Column, Integer, String, Date, DateTime
from db.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    data = Column(Date, nullable=False)
    employeeId = Column(Integer, nullable=False)
    integrationDateTime = Column(DateTime)
    statusCode = Column(String)
    content = Column(String)
    eventId = Column(Integer)
