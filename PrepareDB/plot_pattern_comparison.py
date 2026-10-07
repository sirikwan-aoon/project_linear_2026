import matplotlib.pyplot as plt
import os
import pandas as pd

def plot_pattern_comparison(window_idx=0):
    # ระบุ Folder ที่เก็บไฟล์ CSV
        output_dir = "process_denoise_csv_output"
    
        # 1. โหลดข้อมูล Window_0 จากแต่ละขั้นตอน
        w1 = pd.read_csv(
            os.path.join(output_dir, "1_sliding_window.csv"), index_col=0
        ).iloc[window_idx]
        w2 = pd.read_csv(
            os.path.join(output_dir, "2_mean_centered.csv"), index_col=0
        ).iloc[window_idx]
        w3 = pd.read_csv(
            os.path.join(output_dir, "3_normalized.csv"), index_col=0
        ).iloc[window_idx]
        w4 = pd.read_csv(
            os.path.join(output_dir, "4_X_denoised.csv"), index_col=0
        ).iloc[window_idx]
    
        # 2. พล็อตกราฟเปรียบเทียบแบบ 2x2
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
        # Step 1: Raw
        axes[0, 0].plot(w1.values, color="#1f77b4", linewidth=2)
        axes[0, 0].set_title("1. Raw Sliding Window (Original Price)")
        axes[0, 0].set_ylabel("Price")
        axes[0, 0].grid(True)
    
        # Step 2: Mean Centered
        axes[0, 1].plot(w2.values, color="#ff7f0e", linewidth=2)
        axes[0, 1].set_title("2. Mean Centered (Zero-Mean)")
        axes[0, 1].set_ylabel("Centered Price")
        axes[0, 1].grid(True)
    
        # Step 3: Normalized
        axes[1, 0].plot(w3.values, color="#2ca02c", linewidth=2)
        axes[1, 0].set_title("3. Normalized (Standardized Scale)")
        axes[1, 0].set_xlabel("Time Step (t)")
        axes[1, 0].set_ylabel("Normalized Value")
        axes[1, 0].grid(True)
    
        # Step 4: Denoised
        axes[1, 1].plot(w4.values, color="#d62728", linewidth=2)
        axes[1, 1].set_title("4. Denoised Matrix (Noise Reduced)")
        axes[1, 1].set_xlabel("Time Step (t)")
        axes[1, 1].set_ylabel("Denoised Value")
        axes[1, 1].grid(True)
    
        plt.suptitle(
            f"Transformation Steps of Window_{window_idx} Pattern Pipeline",
            fontsize=14,
            fontweight="bold",
        )
        plt.tight_layout()
        plt.show()