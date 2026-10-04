from LiveTradeProcess.load_db import load_db
from LiveTradeProcess.start_realtime_trading import start_realtime_trading
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    load_dotenv()
    email = os.getenv("IQ_EMAIL")
    password = os.getenv("IQ_PASSWORD")

    #โหลดข้อมูลจาก db.npz เข้ามาก่อน
    X_denoised, future_returns, timestamps = load_db('db.npz')

    # เริ่มรันระบบ
    start_realtime_trading(email, password, X_denoised, future_returns, timestamps, symbol="EURUSD-OTC", amount=10, duration=1)