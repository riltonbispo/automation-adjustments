from db.database import SessionLocal, Base, engine
from models.employee import RPAProposal
from datetime import datetime

Base.metadata.create_all(bind=engine)

session = SessionLocal()

employee_ids = [
    1457885
]

record_date = datetime.strptime("25/07/2025", "%d/%m/%Y").date()

for emp_id in employee_ids:
    new_proposal = RPAProposal(
        date=None,
        employeeId=emp_id,
        integrationDateTime=None,
        status=None,
        content=None,
        eventId=860486
    )
    session.add(new_proposal)

session.commit()
session.close()

print("✅ Registros inseridos com sucesso para os funcionários especificados em 25/07/2025.")
