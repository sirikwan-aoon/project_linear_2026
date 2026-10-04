import numpy as np

# ==========================================
# 3. การสร้างและบันทึกคลังข้อมูล (Save Pattern DB)
# ==========================================
def build_and_save_db(filepath, X_denoised, prices, candle_timestamps, n=30, forecast_horizon=1):
    # คำนวณ Future Return ในอีก forecast_horizon แท่งข้างหน้า
    m = len(X_denoised)
    future_returns = []
    pattern_timestamps = []
    
    for i in range(m):
        pattern_timestamps.append(candle_timestamps[i + n - 1])
        future_idx = i + n - 1 + forecast_horizon
        if future_idx < len(prices):
            current_price = prices[i + n - 1]
            future_price = prices[future_idx]
            ret = (future_price - current_price) / current_price
            future_returns.append(ret)
        else:
            future_returns.append(np.nan)
            
    # บันทึกลงไฟล์ .npz
    np.savez_compressed(
        filepath, 
        patterns=X_denoised, 
        future_returns=np.array(future_returns),
        timestamps=np.array(pattern_timestamps)
    )