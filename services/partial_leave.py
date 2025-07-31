import os
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from tqdm import tqdm
from models.models import RPAProposalV2, Employee
from sqlalchemy.orm import Session

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")


def process_employee(session_api, db_session: Session, emp: Employee, event_id: int):
    today = date.today()
    start_date = today - timedelta(days=30)
    current_date = start_date

    while current_date <= today:
        try:
            formatted_date = current_date.strftime("%d-%m-%Y")
            iso_date = current_date.strftime("%Y-%m-%d")
            employee_id = str(emp.id_ponto_mais)

            response_api = session_api.get(
                f"https://atma-api.pontomais.com.br/api/time_card_control/{employee_id}/work_days",
                params={
                    "end_date": iso_date,
                    "start_date": iso_date,
                    "with_employee": "true",
                    "employee_id": employee_id
                }
            )
            data = response_api.json()
            work_days = data.get("work_days", [])

            time_cards = work_days[0].get("time_cards")
            if not time_cards:
                print(f"Sem marcações de ponto para {employee_id} em {formatted_date}. Pulando.")
                current_date += timedelta(days=1)
                continue

            missing_time = work_days[0].get("missing_time", 0.0)
            if missing_time == 0.0:
                print(f"Sem horas faltantes para {employee_id} em {formatted_date}. Pulando.")
                current_date += timedelta(days=1)
                continue

            payload = {
                "proposal": {
                    "date": iso_date,
                    "times_attributes": [],
                    "proposal_type": 2,
                    "employee_id": employee_id,
                    "status_id": event_id
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

            new_proposal = RPAProposalV2(
                date=current_date,
                employee_id=emp.id_ponto_mais,
                integration_datetime=datetime.now(),
                status=str(response.status_code),
                event_id=event_id
            )
            db_session.add(new_proposal)
            db_session.commit()

            hours = int(missing_time) // 60
            minutes = int(missing_time) % 60
            print(f"📤 Ajuste enviado para {employee_id} em {formatted_date} com {hours}h{minutes:02d}min faltantes.")

        except Exception as e:
            print(f"❌ Erro no dia {current_date} para o colaborador {emp.id_ponto_mais}: {e}")
        finally:
            current_date += timedelta(days=1)


def partial_leave(session_api, db_session: Session, event_id: int):
    employees = (
        db_session.query(Employee)
        .join(Employee.events)
        .filter_by(event_id=event_id)
        .all()
    )
    for emp in tqdm(employees):
        try:
            process_employee(session_api, db_session, emp, event_id)
        except Exception as e:
            print(f"❌ Erro ao processar colaborador {emp.id_ponto_mais}: {e}")
