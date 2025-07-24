import time
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

def send_adjustments(session, df):
    for _, row in df.iterrows():
        try:
            date = pd.to_datetime(row["data"])
            formatted_date = date.strftime("%d-%m-%Y")
            iso_date = date.strftime("%Y-%m-%d")
            employee_id = str(row["id"])

            payload = {
                "proposal": {
                    "date": iso_date,
                    "times_attributes": [],
                    "proposal_type": 2,
                    "employee_id": employee_id,
                    "status_id": 860486
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

            response = session.post(f"{API_BASE_URL}/api/time_cards/proposals/adjust", json=payload)

            print(f"📨 Sent to {employee_id} on {iso_date}: {response.status_code}")
            print(response.json())
        except Exception as e:
            print(f"❌ Error on row {_ + 1}: {e}")
        time.sleep(2)
