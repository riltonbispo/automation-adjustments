from sqlalchemy import Column, Integer, BigInteger
from db.database import Base

class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    personID = Column(BigInteger, nullable=False)
    eventId = Column(BigInteger)