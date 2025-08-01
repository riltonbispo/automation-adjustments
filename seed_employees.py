from db.database import SessionLocal, Base, engine
from models.employee import RPAProposal
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

session = SessionLocal()

employee_ids = [
    1561952,
    1601682,
    1601698,
    1603834,
    1603876,
    1607962,
    1607963,
    1607971,
    1579281,
    1589763,
    1563321,
    1603853,
    1603857,
    1603859,
    1601973,
    1601276,
    1579281,
    1589763,
    1563321,
    1603853
]

start_date = datetime.strptime("18/07/2025", "%d/%m/%Y").date()
end_date = datetime.strptime("18/07/2025", "%d/%m/%Y").date()

current_date = start_date

while current_date <= end_date:
    for emp_id in employee_ids:
        new_proposal = RPAProposal(
            date=current_date,
            employeeId=emp_id,
            integrationDateTime=None,
            status=None,
            content=None,
            eventId=860486
        )
        session.add(new_proposal)
    current_date += timedelta(days=1)

session.commit()
session.close()

print("✅ Registros inseridos com sucesso de 25/06/2025 até 25/07/2025.")
