from datetime import date, datetime
from db.database import SessionLocal, engine, Base
from models.models import Employee, Event

Base.metadata.create_all(bind=engine)

def seed():
    session = SessionLocal()

    try:
        employees = [
            {"id": 1, "id_ponto_mais": 1001},
            {"id": 2, "id_ponto_mais": 1002},
            {"id": 3, "id_ponto_mais": 1003},
        ]

        for emp in employees:
            new_emp = Employee(id=emp["id"], id_ponto_mais=emp["id_ponto_mais"])
            session.add(new_emp)

        events = [
            {"id": 1, "event_id": 5001, "date": date(2025, 7, 31)},
            {"id": 2, "event_id": 5002, "date": date(2025, 8, 1)},
            {"id": 3, "event_id": 5003, "date": date(2025, 8, 2)},
        ]

        for event_data in events:
            event = Event(id=event_data["id"], event_id=event_data["event_id"], date=event_data["date"])
            session.add(event)

        session.commit()
        print("Seed realizado com sucesso!")

    except Exception as e:
        session.rollback()
        print("Erro ao realizar seed:", e)
    finally:
        session.close()

if __name__ == "__main__":
    seed()
