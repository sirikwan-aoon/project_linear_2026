import matplotlib.pyplot as plt

def plot_pattern_comparison(X, X_denoised, sample_indices=[0, 100, 500]):
    """
    ฟังก์ชันพล็อตเปรียบเทียบเวกเตอร์ก่อนและหลัง Denoising
    sample_indices: ดัชนีของ Window ที่ต้องการสุ่มมาดูเปรียบเทียบ
    """
    num_samples = len(sample_indices)
    fig, axes = plt.subplots(num_samples, 1, figsize=(10, 3 * num_samples), sharex=True)
    
    if num_samples == 1:
        axes = [axes]
        
    for i, idx in enumerate(sample_indices):
        # เส้นสีเทาประ: ข้อมูลหลัง Normalized ที่ยังมี Noise
        axes[i].plot(X[idx], label='Original Normalized (With Noise)', 
                     color='gray', linestyle='--', alpha=0.7, marker='o', markersize=4)
        
        # เส้นสีน้ำเงินทึบ: ข้อมูลที่ผ่านการกรอง SVD แล้ว
        axes[i].plot(X_denoised[idx], label='SVD Denoised (Main Pattern)', 
                     color='#1f77b4', linewidth=2.5)
        
        axes[i].set_title(f"Sliding Window Index: {idx}", fontsize=11, fontweight='bold')
        axes[i].set_ylabel("Normalized Value")
        axes[i].grid(True, linestyle=':', alpha=0.6)
        axes[i].legend(loc='upper left')
        
    axes[-1].set_xlabel("Time Step within Window ($n$)")
    plt.tight_layout()
    plt.show()