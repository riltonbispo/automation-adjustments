from db.database import SessionLocal, Base, engine
from models.models import EmployeeEvent, Employee, Event
from sqlalchemy import delete

session = SessionLocal()

print("⚠️ Limpando registros...")


session.execute(delete(EmployeeEvent))

session.execute(delete(Employee))
session.execute(delete(Event))


session.commit()
session.close()

print("🧹 Todos os dados foram removidos com sucesso.")
