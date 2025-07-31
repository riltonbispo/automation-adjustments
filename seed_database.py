from db.database import Base, engine
from sqlalchemy.orm import Session
from models.models import Employee, Event
from datetime import datetime

def seed():
    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    employees_data = [
        {"id_ponto_mais": 1457885},
    ]
    employees = [Employee(**data) for data in employees_data]

    event = Event(event_id=860486, date=datetime.now())

    event.employees.extend(employees)

    session.add(event)
    session.add_all(employees)

    session.commit()
    session.close()

if __name__ == "__main__":
    seed()
