from services.auth_service import authenticate
from services.adjustment_service import send_adjustments
import pandas as pd

def main():
    try:
        df = pd.read_excel("datas.xlsx")
        session = authenticate()
        send_adjustments(session, df)
    except Exception as e:
        print("❌ General error:", e)

if __name__ == "__main__":
    main()
