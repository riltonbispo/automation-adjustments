import os
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from tqdm import tqdm
from models.employee import RPAProposal
from models.person import Person


load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

def process_employee(session_api, db_session, emp):
    today = date.today()
    start_date = today - timedelta(days=30)

    current_date = start_date
    while current_date <= today:
        try:
            formatted_date = current_date.strftime("%d-%m-%Y")
            iso_date = current_date.strftime("%Y-%m-%d")
            employee_id = str(emp.personID)

            current_date_info = session_api.get(
                f"https://atma-api.pontomais.com.br/api/time_card_control/{employee_id}/work_days",
                params={
                    "end_date": iso_date,
                    "start_date": iso_date,
                    "with_employee": "true",
                    "employee_id": employee_id
                }
            )
            data = current_date_info.json()

            work_days = data.get("work_days", [])

            time_cards = work_days[0].get("time_cards")
            if not time_cards:
                print(f"Sem marcações de ponto (time_cards) para o colaborador {employee_id} no dia {current_date.strftime('%d/%m/%Y')}. Pulando para o próximo dia.")
                continue

            missing_time = work_days[0].get("missing_time", 0.0)
            if missing_time == 0.0:
                print(f"Nenhuma hora faltante para o colaborador {employee_id} no dia {current_date.strftime('%d/%m/%Y')}. Pulando para o próximo dia.")
                continue

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

            emp.date = current_date
            emp.integrationDateTime = datetime.now()
            emp.status = str(response.status_code)
            emp.content = str(response.json())
            db_session.commit()

            new_proposal = RPAProposal(
                date=current_date,
                employeeId=employee_id,
                integrationDateTime=datetime.now(),
                status=str(response.status_code),
                content=str(response.json()),
                eventId=860486
            )
            db_session.add(new_proposal)
            db_session.commit()

            hours = int(missing_time) // 60
            minutes = int(missing_time) % 60
            print(f"📤 Ajuste enviado para o colaborador {employee_id} no dia {current_date.strftime('%d/%m/%Y')} com {hours}h{minutes:02d}min faltantes.")


        except Exception as e:
            print(f"❌ Erro ao processar o dia {current_date} para o colaborador {emp.employeeId}: {e}")
        finally:
            current_date += timedelta(days=1)

def partial_leave(session_api, db_session, Person):
    employees = db_session.query(Person.filter(Person.eventId.is_(860486))).all()
    for emp in tqdm(employees):
        try:
            process_employee(session_api, db_session, emp)
        except Exception as e:
            print(f"❌ Erro ao processar o colaborador com ID {emp.employeeId}: {e}")
