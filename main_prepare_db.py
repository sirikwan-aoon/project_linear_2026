from PrepareDB.prepareDB_main import prepareDB_main
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("IQ_EMAIL")
    password = os.getenv("IQ_PASSWORD")

    prepareDB_main(email, password, symbol="EURUSD-OTC", timeframe=60, days=60)
