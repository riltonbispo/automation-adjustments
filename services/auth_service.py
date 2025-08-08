import os
import requests
from dotenv import load_dotenv

load_dotenv()

LOGIN_CPF = os.getenv("LOGIN_CPF")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
API_BASE_URL = os.getenv("API_BASE_URL")

def authenticate():
    session = requests.Session()
    response = session.post(
        f"{API_BASE_URL}/api/auth/sign_in",
        json={"login": LOGIN_CPF, "password": LOGIN_PASSWORD}
    )

    if response.status_code != 201:
        raise Exception(f"Login error: {response.status_code} - {response.text}")

    data = response.json()
    token = data.get("token")
    client_id = data.get("client_id")

    if not token or not client_id:
        raise Exception("Missing token or client_id!")

    session.headers.update({
        "accept": "application/json",
        "access-token": token,
        "api-version": "2",
        "client": client_id,
        "content-type": "application/json",
        "origin": "https://atma2.pontomais.com.br",
        "referer": "https://atma2.pontomais.com.br/",
        "token": token,
        "uid": LOGIN_CPF,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "uuid": "f1eb4783-8c9f-43f6-9fc7-39b90373146f"
    })

    print("Successfully authenticated.")
    return session
