import os
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

def partial_leave(session_api, db_session, Employee):
    employees = db_session.query(Employee).filter(Employee.integrationDateTime.is_(None)).all()

    for idx, emp in enumerate(tqdm(employees)):
        try:
            formatted_date = emp.date.strftime("%d-%m-%Y")
            iso_date = emp.date.strftime("%Y-%m-%d")
            employee_id = str(emp.employeeId)

            payload = {
                "proposal": {
                    "date": iso_date,
                    "times_attributes": [],
                    "proposal_type": 2,
                    "employee_id": employee_id,
                    "status_id": emp.eventId
                },
                "_appVersion": "0.10.32",
                "_device": {
                    "browser": {
                        "name": "chrome",
                        "version": "138.0.0.0",
                        "versionSearchString": "chrome"
                    }
                },
                "_path": f"/controle-de-ponto/gerenciar-ponto/ajuste/{formatted_date}/colaborador/{employee_id}?id={employee_id}"
            }

            response = session_api.post(f"{API_BASE_URL}/api/time_cards/proposals/adjust", json=payload)

            emp.integrationDateTime = datetime.now()
            emp.status = str(response.status_code)
            emp.content = str(response.json())
            db_session.commit()

        except Exception as e:
            print(f"\n Erro na linha {idx + 1}: {e}")

    print("\n Ajustes enviados com sucesso.")