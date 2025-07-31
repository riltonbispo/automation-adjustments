from services.auth_service import authenticate
from services.partial_leave import partial_leave
from db.database import SessionLocal, engine, Base
from models.models import Employee

def main():
    try:
        print("🛠️ Verificando/criando tabelas...")
        Base.metadata.create_all(bind=engine)
        
        db_session = SessionLocal()


        new_person = Employee(
            personID=1457885,
            eventId=860486
        )

        db_session.add(new_person)
        db_session.commit()

        session_api = authenticate()
        partial_leave(session_api, db_session, Employee)

    except Exception as e:
        print("❌ General error:", e)
    finally:
        db_session.close()

if __name__ == "__main__":
    main()
