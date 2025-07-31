from db.database import SessionLocal, Base, engine
from models.models import RPAProposalV2

session = SessionLocal()

print("⚠️ Limpando registros...")

session.query(RPAProposalV2).delete()

session.commit()
session.close()

print("🧹 Todos os dados foram removidos com sucesso.")
