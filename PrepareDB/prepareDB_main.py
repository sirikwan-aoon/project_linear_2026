from PrepareDB.fetch_iq_option_candles import fetch_iq_option_candles
from PrepareDB.build_denoised_matrix import build_denoised_matrix
from PrepareDB.build_and_save_db import build_and_save_db
from PrepareDB.plot_pattern_comparison import plot_pattern_comparison

import numpy as np

def prepareDB_main(email, password, symbol="EURUSD-OTC", timeframe=60, days=60, n=30, forecast_horizon=1):
    prices, candle_timestamps = fetch_iq_option_candles(email, password, symbol, timeframe, days)
    X, X_denoised = build_denoised_matrix(prices, n=30, k=3)
    build_and_save_db('db.npz', X_denoised, prices, candle_timestamps, n, forecast_horizon)

    # plot_pattern_comparison(X, X_denoised, sample_indices=[10, 250, 1000])

    # โหลดไฟล์มาตรวจสอบ
    data = np.load('db.npz')

    print("Keys ในไฟล์:", data.files)
    print("ขนาด Patterns Matrix:", data['patterns'].shape)
    print("จำนวน Future Returns:", len(data['future_returns']))
