import os
import pandas as pd
import numpy as np

# ==========================================
# 2. Data Pipeline Processing Logic
# ==========================================
def build_denoised_matrix(prices, n=30, k=3, export_csv=True, output_dir="process_denoise_csv_output"):
    # ขั้นตอนที่ 2: Sliding Window Vectorization
    m = len(prices) - n + 1
    windows = np.array([prices[i : i + n] for i in range(m)])

    cols = [f"t+{i}" for i in range(n)]
    rows = [f"Window_{i}" for i in range(m)]

    if export_csv:
        pd.DataFrame(windows, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "1_sliding_window.csv")
        )

    # ขั้นตอนที่ 3: Mean Centering
    means = np.mean(windows, axis=1, keepdims=True)
    p_centered = windows - means

    if export_csv:
        # บันทึก ค่าเฉลี่ยของแต่ละ Window
        pd.DataFrame(means, index=rows, columns=["mean"]).to_csv(
            os.path.join(output_dir, "2_window_means.csv")
        )
        # บันทึก ข้อมูลที่ Mean Center แล้ว
        pd.DataFrame(p_centered, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "2_mean_centered.csv")
        )

    # ขั้นตอนที่ 4: Vector Normalization
    norms = np.linalg.norm(p_centered, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    p_norm = p_centered / norms

    if export_csv:
        # บันทึก ค่า Norm
        pd.DataFrame(norms, index=rows, columns=["norm"]).to_csv(
            os.path.join(output_dir, "3_norms.csv")
        )
        # บันทึก ข้อมูลที่ Normalize แล้ว
        pd.DataFrame(p_norm, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "3_normalized.csv")
        )

    # ขั้นตอนที่ 5: Data Matrix Construction
    X = np.vstack(p_norm)

    if export_csv:
        pd.DataFrame(X, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "4_data_matrix_X.csv")
        )

    # ขั้นตอนที่ 6: Denoising via SVD
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    X_denoised = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

    if export_csv:
        # บันทึก Singular Values
        pd.DataFrame(S, columns=["Singular_Value"]).to_csv(
            os.path.join(output_dir, "5_singular_values.csv"),
            index_label="Component",
        )
        # บันทึก X_denoised ผลลัพธ์สุดท้าย
        pd.DataFrame(X_denoised, index=rows, columns=cols).to_csv(
            os.path.join(output_dir, "5_X_denoised.csv")
        )

    return X, X_denoised