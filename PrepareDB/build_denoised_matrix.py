import os
import pandas as pd
import numpy as np

# ==========================================
# 2. Data Pipeline Processing Logic
# ==========================================
def build_denoised_matrix(
    prices,
    timestamps,
    n=30,
    k=3,
    forecast_horizon=1,
    max_gap_sec=65, # จริงๆ คือ 60 วินาที แต่ 65 เป็นค่าที่ยอมรับได้เผื่อระบบดีเลย์เล็กน้อย
    export_csv=True,
    output_dir="process_denoise_csv_output",
):
    if export_csv and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # ขั้นตอนที่ 1: Sliding Window Vectorization
    valid_windows = []
    valid_timestamps = []
    valid_future_returns = []
    valid_indices = []

    total_len = len(prices)
    max_iter = total_len - n - forecast_horizon + 1

    for i in range(max_iter):
        # 1.1 ดึงเวกเตอร์ราคารวม (P_i) และเวกเตอร์เวลารวม (T_i) ขนาด (n + h) แท่ง
        full_prices = prices[i : i + n + forecast_horizon]      # P_i in R^(n+h)
        full_ts     = timestamps[i : i + n + forecast_horizon]  # T_i in R^(n+h)

        # 1.2 ตรวจสอบ Time Gap รวดเดียวตลอดทั้ง (n + h)
        if np.any(np.diff(full_ts) > max_gap_sec):
            continue  # หากจุดใดจุดหนึ่งใน 31 แท่งมี Gap เกินกำหนด ให้ข้ามทิ้ง

        # 1.3 แยกส่วน Feature Vector (n แท่งแรก) และ Target
        window_prices = full_prices[:n]
        p_current     = full_prices[n - 1]     # ราคาปิดแท่งสุดท้ายใน Window (t_n)
        p_future      = full_prices[n + forecast_horizon - 1] # ราคาปิดอนาคต (t_n+h)
        
        # 1.4 คำนวณ Future Return (%)
        ret = (p_future - p_current) / p_current

        valid_windows.append(window_prices)
        valid_timestamps.append(full_ts[n - 1])  # เก็บ Timestamp ของแท่งราคาปิดแท่งสุดท้าย
        valid_future_returns.append(ret)
        valid_indices.append(i)

    # แปลงเป็น NumPy Array
    windows = np.array(valid_windows)
    valid_timestamps = np.array(valid_timestamps)
    valid_future_returns = np.array(valid_future_returns)

    cols = [f"t+{i}" for i in range(n)]
    rows = [f"Window_{idx}" for idx in valid_indices]  # ใช้ Index ดั้งเดิมตั้งชื่อแถว

    if export_csv:
        pd.DataFrame(windows, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "1_sliding_window.csv"), float_format="%.4f"
        )

    # ขั้นตอนที่ 2: Mean Centering
    means = np.mean(windows, axis=1, keepdims=True)
    p_centered = windows - means

    if export_csv:
        # บันทึก ค่าเฉลี่ยของแต่ละ Window
        pd.DataFrame(means, index=rows, columns=["mean"]).to_csv(
            os.path.join(output_dir, "2_window_means.csv"), float_format="%.4f"
        )
        # บันทึก ข้อมูลที่ Mean Center แล้ว
        pd.DataFrame(p_centered, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "2_mean_centered.csv"), float_format="%.4f"
        )

    # ขั้นตอนที่ 3: Vector Normalization
    norms = np.linalg.norm(p_centered, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    p_norm = p_centered / norms

    if export_csv:
        # บันทึก ค่า Norm
        pd.DataFrame(norms, index=rows, columns=["norm"]).to_csv(
            os.path.join(output_dir, "3_norms.csv"), float_format="%.4f"
        )
        # บันทึก ข้อมูลที่ Normalize แล้ว
        pd.DataFrame(p_norm, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "3_normalized.csv"), float_format="%.4f"
        )

    X = p_norm

    # ขั้นตอนที่ 4: Denoising via SVD
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    X_denoised = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

    if export_csv:
        # บันทึก Singular Values
        pd.DataFrame(S, columns=["Singular_Value"]).to_csv(
            os.path.join(output_dir, "4_singular_values.csv"),
            index_label="Component",
            float_format="%.4f",
        )
        # บันทึก X_denoised ผลลัพธ์สุดท้าย
        pd.DataFrame(X_denoised, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "4_X_denoised.csv"), float_format="%.4f"
        )

    print()
    print('='*50)
    print('Denoised data matrix')
    print('='*50)
    df = pd.DataFrame(X_denoised, index=rows, columns=cols)
    print(df)
    
    return X, X_denoised, valid_future_returns, valid_timestamps