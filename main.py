from services.auth_service import authenticate
from services.adjustment_service import send_adjustments
from db.database import SessionLocal, engine, Base
from models.employee import RPAProposal

def main():
    try:
        print("🛠️ Verificando/criando tabelas...")
        Base.metadata.create_all(bind=engine)
        
        db_session = SessionLocal()
        session_api = authenticate()
        send_adjustments(session_api, db_session, RPAProposal)

    except Exception as e:
        print("❌ General error:", e)
    finally:
        db_session.close()

if __name__ == "__main__":
    main()
