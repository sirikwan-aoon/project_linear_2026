import numpy as np

# ========================================================
# Step 2: ฟังก์ชันเตรียมข้อมูลปัจจุบัน
# ========================================================
def prepare_live_prices(prices_30):
    p_centered = prices_30 - np.mean(prices_30)
    norm = np.linalg.norm(p_centered)
    return p_centered / (norm if norm != 0 else 1e-10)