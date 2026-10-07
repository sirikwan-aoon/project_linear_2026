from PrepareDB.fetch_iq_option_candles import fetch_iq_option_candles
from PrepareDB.build_denoised_matrix import build_denoised_matrix
from PrepareDB.build_and_save_db import build_and_save_db
from PrepareDB.plot_pattern_comparison import plot_pattern_comparison

import numpy as np

def prepareDB_main(email, password, symbol="EURUSD-OTC", timeframe=60, days=60, n=30, forecast_horizon=1):
    prices, candle_timestamps, raw_timestamps = fetch_iq_option_candles(email, password, symbol, timeframe, days)
    X, X_denoised, future_return, valid_timestamps = build_denoised_matrix(prices=prices, timestamps=candle_timestamps, n=30, k=3)
    build_and_save_db(filepath='db.npz', X_denoised=X_denoised, prices=prices, valid_timestamps=valid_timestamps, future_returns=future_return, raw_timestamps=raw_timestamps)

    # โหลดไฟล์มาตรวจสอบ
    data = np.load('db.npz')

    print()
    print("Keys ในไฟล์:", data.files)
    print("ขนาด Patterns Matrix:", data['patterns'].shape)
    print("จำนวน Future Returns:", len(data['future_returns']))

    return prices
