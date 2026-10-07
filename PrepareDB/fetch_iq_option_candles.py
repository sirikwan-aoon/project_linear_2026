from iqoptionapi.stable_api import IQ_Option
import time
import pandas as pd

# ==========================================
# 1. Historical Data Harvesting Function
# ==========================================
def fetch_iq_option_candles(email, password, symbol="EURUSD", timeframe=60, days=60):
    API = IQ_Option(email, password)
    API.connect()
    
    # 2 เดือนมีประมาณ 60 วัน * 24 ชม. * 60 นาที = 86,400 แท่ง
    total_candles = days * 24 * 60
    all_candles = []
    end_time = time.time()

    print('fetching...')

    while len(all_candles) < total_candles:
        fetch_count = min(1000, total_candles - len(all_candles))
        candles = API.get_candles(symbol, timeframe, fetch_count, end_time)
        # print(candles) #ถ้าไม่อยากให้แสดงข้อมูลที่โหลดเข้ามา comment ตรงนี้!!!!!
        if not candles:
            break
            
        all_candles = candles + all_candles  # ต่อข้อมูลย้อนหลัง
        end_time = candles[0]['from'] - 1   # ขยับ timestamp ย้อนกลับไปก่อนแท่งแรกสุดที่ดึงได้
        time.sleep(0.2)  # ป้องกัน Rate Limit

    print('='*50)
    print('Fetching Success✅')
    print('='*50)
    
    print()
    print('='*50)
    print('Raw data')
    print('='*50)
    
    print(all_candles)
    
    print()
    print('='*50)
    print('Raw data converted into a DataFrame')
    print('='*50)
    
    df = pd.DataFrame(all_candles)

    print(type(df))
    print(df)

    print()
    print('='*50)
    print('Close price vector')
    print('='*50)

    prices = df['close'].to_numpy()
    candle_timestamps = df['from'].to_numpy()

    print()
    print(type(prices))
    print(prices)
    print("Shape :", prices.shape)

    return prices, candle_timestamps, df['from']