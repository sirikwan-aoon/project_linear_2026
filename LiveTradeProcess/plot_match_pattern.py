import matplotlib.pyplot as plt

def plot_matched_patterns(query_norm, X_denoised, result, symbol="EURUSD-OTC"):
    """
    ฟังก์ชันแสดงผลเปรียบเทียบรูปทรงกราฟปัจจุบันกับ Top-k แฝดในอดีต (แสดงวัน-เวลา)
    """
    top_k_indices = result['top_k_indices']
    top_k_scores = result['top_k_scores']
    top_k_returns = result['top_k_returns']
    # 1. ดึงข้อมูลวัน-เวลา เพิ่มเติมจาก dict 'result' (ใช้ .get เผื่อกรณีไม่ได้ส่งมาเพื่อป้องกันโปรแกรมพัง)
    top_k_dates = result.get('top_k_dates', [''] * len(top_k_indices))
    
    k = len(top_k_indices)

    plt.figure(figsize=(13, 6.5)) # ปรับขนาดรูปเพิ่มเล็กน้อยเพื่อให้ใส่ Legend พอดี

    # 2. พล็อตทรงกราฟปัจจุบัน (Live Query) เป็นเส้นทึบสีน้ำเงินหนา
    plt.plot(query_norm, label="Current Live Pattern (Query)", color="#1f77b4", linewidth=3.5, zorder=10)

    # 3. พล็อตทรงกราฟแฝดในอดีตทั้ง k อันดับ พร้อมใส่ Date String
    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # เพิ่ม top_k_dates เข้าไปใน zip(...)
    for rank, (idx, score, ret, date_str) in enumerate(zip(top_k_indices, top_k_scores, top_k_returns, top_k_dates), 1):
        ret_pct = ret * 100
        direction = "🟢 UP" if ret > 0 else "🔴 DOWN"
        
        # จัดรูปแบบข้อความวันที่ช็อตสั้นๆ หากมีข้อมูล
        date_display = f" [{date_str}]" if date_str else ""
        
        # เพิ่ม [วัน-เวลา] ลงใน label_text
        label_text = f"Top {rank}{date_display} | Sim: {score:.4f} | Future: {ret_pct:+.3f}% ({direction})"
        
        color_idx = (rank - 1) % len(colors)
        plt.plot(
            X_denoised[idx], 
            linestyle="--", 
            linewidth=1.8, 
            alpha=0.8, 
            color=colors[color_idx],
            label=label_text
        )

    # 4. ตกแต่งกราฟ
    signal_color = 'green' if result['signal'] == 'CALL' else ('red' if result['signal'] == 'PUT' else 'gray')
    plt.title(
        f"Pattern Matching Visualizer [{symbol}] | Signal: {result['signal']} "
        f"(CALL WinRate: {result['win_rate_call']:.0f}% / PUT WinRate: {result['win_rate_put']:.0f}%)",
        fontsize=12, fontweight='bold', color=signal_color
    )
    plt.xlabel("Time Step within Window ($n$)", fontsize=10)
    plt.ylabel("Normalized Price Value", fontsize=10)
    plt.axhline(0, color='black', linestyle=':', alpha=0.4)
    plt.grid(True, linestyle=":", alpha=0.6)
    
    # ปรับขนาดฟอนต์ Legend เป็น 8.5 เพื่อให้แสดงข้อความวันที่ยาวๆ ได้สวยงามไม่บังเส้นกราฟ
    plt.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
    plt.tight_layout()
    plt.show()