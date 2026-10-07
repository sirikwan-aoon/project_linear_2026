import numpy as np

# ==========================================
# 3. การสร้างและบันทึกคลังข้อมูล (Save Pattern DB)
# ==========================================
def build_and_save_db(filepath, X_denoised, prices, valid_timestamps, future_returns, raw_timestamps):
          
    # บันทึกลงไฟล์ .npz
    np.savez_compressed(
        filepath, 
        patterns=X_denoised, 
        future_returns=np.array(future_returns),
        timestamps=np.array(valid_timestamps),
        full_prices=prices,
        raw_timestamps=raw_timestamps,
    )