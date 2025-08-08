from db.database import SessionLocal
from models.employee import RPAProposal

session = SessionLocal()

print("Limpando registros...")

session.query(RPAProposal).delete()

session.commit()
session.close()

print("Todos os dados foram removidos com sucesso.")
