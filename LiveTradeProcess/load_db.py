import time
import numpy as np

# ========================================================
# Step 1: โหลดคลังข้อมูลเข้า RAM ครั้งเดียว (ทำตอนเปิดโปรแกรม)
# ========================================================
def load_db(filepath):
    print("กำลังโหลดคลังข้อมูลเข้า RAM...")
    start_time = time.time()

    with np.load(filepath) as data:
        X_denoised = data['patterns']
        future_returns = data['future_returns']
        timestamps = data['timestamps']

    print(f"โหลดข้อมูลสำเร็จใน {time.time() - start_time:.2f} วินาที (พร้อมเทรด Real-time)")

    return X_denoised, future_returns, timestamps