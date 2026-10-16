from PrepareDB.fetch_iq_option_candles import fetch_iq_option_candles
from PrepareDB.build_denoised_matrix import build_denoised_matrix
from PrepareDB.build_and_save_db import build_and_save_db
from PrepareDB.plot_pattern_comparison import plot_pattern_comparison

import numpy as np

def prepareDB_main(email, password, symbol="EURUSD-OTC", filepath='db.npz', timeframe=60, days=60, window=30):
    prices, candle_timestamps, raw_timestamps = fetch_iq_option_candles(email, password, symbol, timeframe, days)
    X_denoised, future_return, valid_timestamps = build_denoised_matrix(prices=prices, timestamps=candle_timestamps, window_size=window, k=3)
    build_and_save_db(filepath=filepath, X_denoised=X_denoised, prices=prices, valid_timestamps=valid_timestamps, future_returns=future_return, raw_timestamps=raw_timestamps)

    # โหลดไฟล์มาตรวจสอบ
    data = np.load('db.npz')

    print()
    print("Keys ในไฟล์:", data.files)
    print("ขนาด Patterns Matrix:", data['patterns'].shape)
    print("จำนวน Future Returns:", len(data['future_returns']))

    return prices
