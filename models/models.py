from sqlalchemy import Table, Column, Integer, BigInteger, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

EmployeeEvent = Table(
    "EmployeeEvent",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("Employee.id_ponto_mais"), primary_key=True),
    Column("event_id", Integer, ForeignKey("Event.event_id"), primary_key=True),
)

class Employee(Base):
    __tablename__ = "Employee"

    id = Column(Integer, autoincrement=True)
    id_ponto_mais = Column(Integer, primary_key=True)

    proposals = relationship("RPAProposalV2", back_populates="employee")
    events = relationship("Event", secondary=EmployeeEvent, back_populates="employees")


class Event(Base):
    __tablename__ = "Event"

    id = Column(Integer, autoincrement=True)
    event_id = Column(Integer, primary_key=True)
    date = Column(Date)

    proposals = relationship("RPAProposalV2", back_populates="event")
    employees = relationship("Employee", secondary=EmployeeEvent, back_populates="events")


class RPAProposalV2(Base):
    __tablename__ = 'RPAProposalV2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('Employee.id_ponto_mais'))
    event_id = Column(Integer, ForeignKey('Event.event_id'))
    date = Column(Date)
    status = Column(String)
    integration_datetime = Column(DateTime)

    employee = relationship('Employee', back_populates='proposals')
    event = relationship('Event', back_populates='proposals')

class RPAProposal(Base):
    __tablename__ = "RPAProposal"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    employeeId = Column(BigInteger, nullable=False)
    date = Column(Date)
    eventId = Column(BigInteger)
    integrationDateTime = Column(DateTime)
    status = Column(String(25))
    content = Column(String(1000))