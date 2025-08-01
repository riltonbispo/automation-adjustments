import json
from datetime import datetime
from db.database import SessionLocal, Base, engine
from models.employee import RPAProposal

Base.metadata.create_all(bind=engine)
session = SessionLocal()

with open("data.json", "r") as file:
    data_para_seed = json.load(file)

for item in data_para_seed:
    proposal = RPAProposal(
        date=datetime.strptime(item["date"], "%d/%m/%Y").date(),
        employeeId=item["employeeId"],
        integrationDateTime=None,
        status=None,
        content=None,
        eventId=860486
    )
    session.add(proposal)

session.commit()
session.close()

print("✅ Registros inseridos com sucesso")
