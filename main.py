from services.auth_service import authenticate
from services.partial_leave import partial_leave
from db.database import SessionLocal, engine, Base
from models.employee import RPAProposal

def main():
    try:
        print("🛠️ Verificando/criando tabelas...")
        Base.metadata.create_all(bind=engine)
        
        db_session = SessionLocal()
        session_api = authenticate()
        partial_leave(session_api, db_session, RPAProposal)

    except Exception as e:
        print("❌ General error:", e)
    finally:
        db_session.close()

if __name__ == "__main__":
    main()
