from sqlalchemy import Column, Integer, BigInteger, String, Date, DateTime
from db.database import Base

class RPAProposal(Base):
    __tablename__ = "RPAProposal"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    employeeId = Column(BigInteger, nullable=False)
    date = Column(Date, nullable=False)
    eventId = Column(BigInteger)
    integrationDateTime = Column(DateTime)
    status = Column(String(25))
    content = Column(String(1000))
