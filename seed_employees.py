from db.database import SessionLocal, Base, engine
from models.employee import RPAProposal
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

session = SessionLocal()

employee_ids = [
    1457885
]

start_date = datetime.strptime("25/06/2025", "%d/%m/%Y").date()
end_date = datetime.strptime("25/07/2025", "%d/%m/%Y").date()

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
