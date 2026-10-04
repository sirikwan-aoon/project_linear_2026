import matplotlib.pyplot as plt
import numpy as np

def plot_matched_patterns_macro(query_norm, X_denoised, result, full_prices, n=30, symbol="EURUSD-OTC"):
    """
    แสดงผลการแมตช์แพตเทิร์น 2 ระดับ:
    1. Macro View: เส้นราคาอดีตทั้งหมด พร้อมไฮไลต์ช่วงเวลา Top-k Matches
    2. Micro View: เปรียบเทียบทรงกราฟ Normalized (Live Query vs Top-k Twins)
    """
    top_k_indices = result['top_k_indices']
    top_k_scores = result['top_k_scores']
    top_k_returns = result['top_k_returns']
    top_k_dates = result.get('top_k_dates', [''] * len(top_k_indices))
    k = len(top_k_indices)

    # กำหนดโทนสีให้ตรงกันทั้งกราฟบนและกราฟล่าง
    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    # สร้าง Figure แบบ 2 Subplots (บน-ล่าง)
    fig, (ax_macro, ax_micro) = plt.subplots(
        2, 1, figsize=(14, 9), 
        gridspec_kw={'height_ratios': [1.8, 1.2]}
    )

    # =========================================================================
    # 1. MACRO VIEW: กราฟเส้นราคาอดีตทั้งหมด + ไฮไลต์ตำแหน่ง Top-k
    # =========================================================================
    ax_macro.plot(full_prices, color='#7f7f7f', linewidth=1.0, alpha=0.6, label="Historical Price Series")
    
    for rank, (idx, score, date_str) in enumerate(zip(top_k_indices, top_k_scores, top_k_dates), 1):
        color = colors[(rank - 1) % len(colors)]
        
        # ช่วงของ Window ในคลังข้อมูลอดีตคือตั้งแต่ index 'idx' ถึง 'idx + n'
        start_idx = idx
        end_idx = idx + n
        
        # วาดแถบสีไฮไลต์ช่วง Window ในอดีต (axvspan)
        ax_macro.axvspan(start_idx, end_idx, color=color, alpha=0.35, label=f"Rank {rank} Match ({score:.3f})")
        
        # วาดเส้นประแนวตั้งปิดหัว-ท้าย Window
        ax_macro.axvline(start_idx, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
        ax_macro.axvline(end_idx, color=color, linestyle="--", linewidth=1.2, alpha=0.8)
        
        # เขียนข้อความระบุ Rank เหนือแถบไฮไลต์
        mid_idx = start_idx + (n / 2)
        max_p = np.max(full_prices[start_idx:end_idx])
        ax_macro.text(
            mid_idx, max_p, f"R{rank}", 
            fontsize=9, fontweight='bold', color=color, 
            ha='center', va='bottom'
        )

    ax_macro.set_title(f"Macro View: Full Historical Database Search Area [{symbol}] ({len(full_prices):,} Candles)", fontsize=11, fontweight='bold')
    ax_macro.set_xlabel("Historical Candle Index (Timeline)", fontsize=9)
    ax_macro.set_ylabel("Raw Price", fontsize=9)
    ax_macro.grid(True, linestyle=":", alpha=0.5)
    ax_macro.legend(loc="upper left", fontsize=8.5, framealpha=0.9, ncol=2)

    # =========================================================================
    # 2. MICRO VIEW: ทรงกราฟ Normalized เปรียบเทียบ
    # =========================================================================
    # พล็อต Live Pattern ปัจจุบัน
    ax_micro.plot(query_norm, label="Current Live Pattern (Query)", color="#1f77b4", linewidth=3.5, zorder=10)

    # พล็อต Top-k Patterns
    for rank, (idx, score, ret, date_str) in enumerate(zip(top_k_indices, top_k_scores, top_k_returns, top_k_dates), 1):
        ret_pct = ret * 100
        direction = "🟢 UP" if ret > 0 else "🔴 DOWN"
        date_display = f" [{date_str}]" if date_str else ""
        label_text = f"Top {rank}{date_display} | Sim: {score:.4f} | Future: {ret_pct:+.3f}% ({direction})"
        
        color = colors[(rank - 1) % len(colors)]
        ax_micro.plot(
            X_denoised[idx], 
            linestyle="--", 
            linewidth=1.8, 
            alpha=0.85, 
            color=color,
            label=label_text
        )

    signal_color = 'green' if result['signal'] == 'CALL' else ('red' if result['signal'] == 'PUT' else 'gray')
    ax_micro.set_title(
        f"Micro View: Normalized Pattern Alignment | Signal: {result['signal']} "
        f"(CALL WR: {result['win_rate_call']:.0f}% / PUT WR: {result['win_rate_put']:.0f}%)",
        fontsize=11, fontweight='bold', color=signal_color
    )
    ax_micro.set_xlabel("Time Step within Window ($n$)", fontsize=9)
    ax_micro.set_ylabel("Normalized Price Value", fontsize=9)
    ax_micro.axhline(0, color='black', linestyle=':', alpha=0.4)
    ax_micro.grid(True, linestyle=":", alpha=0.5)
    ax_micro.legend(loc="upper left", fontsize=8, framealpha=0.9)

    plt.tight_layout()
    plt.show()



def plot_matched_patterns_with_local_zoom(
    full_prices, result, n=30, context_padding=50, symbol="EURUSD-OTC"
):
  """แสดงภาพรวม Macro View พร้อมขยายภาพเจาะลึก (Local Context Zoom) ของ Top-k แต่ละอันดับ

  ปรับปรุง: เพิ่มเส้นประ 2 ขอบ (เริ่ม-จบ) + ถมสีไฮไลต์ตรงกลาง พิกัดตรงเป๊ะ 100%
  """
  top_k_indices = result["top_k_indices"]
  top_k_scores = result["top_k_scores"]
  top_k_returns = result["top_k_returns"]
  top_k_dates = result.get("top_k_dates", [""] * len(top_k_indices))
  k = len(top_k_indices)

  colors = ["#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

  fig = plt.figure(figsize=(16, 9))
  gs = fig.add_gridspec(2, k, height_ratios=[1.2, 1.0])

  # -------------------------------------------------------------------------
  # 1. MACRO OVERVIEW (แถวบน)
  # -------------------------------------------------------------------------
  ax_macro = fig.add_subplot(gs[0, :])
  ax_macro.plot(
      full_prices,
      color="#a0a0a0",
      linewidth=0.8,
      alpha=0.6,
      label="Full Historical Prices",
  )

  for rank, (idx, score) in enumerate(zip(top_k_indices, top_k_scores), 1):
    color = colors[(rank - 1) % len(colors)]
    start_idx = idx  # จุดเริ่มต้น Window (แท่งที่ 1)
    end_idx = idx + n  # จุดสิ้นสุด Window (แท่งที่ 30)

    # 1.1 ถมแถบสีไฮไลต์โปร่งแสงระหว่างขอบซ้าย-ขวา
    ax_macro.axvspan(
        start_idx,
        end_idx,
        color=color,
        alpha=0.25,
        label=f"Rank {rank} ({score:.3f})",
    )

    # 1.2 วาดเส้นประแนวตั้งปิดหัว-ท้าย 2 เส้น
    ax_macro.axvline(
        start_idx, color=color, linestyle="--", linewidth=1.2, alpha=0.85
    )
    ax_macro.axvline(
        end_idx, color=color, linestyle="--", linewidth=1.2, alpha=0.85
    )

    # 1.3 จุด Scatter และป้ายชื่อ Rank ตรงขอบขวา (จุดเกิดสัญญาณจริง)
    ax_macro.scatter(
        end_idx - 1, full_prices[end_idx - 1], color=color, s=50, zorder=5
    )
    ax_macro.text(
        end_idx,
        full_prices[end_idx - 1],
        f" R{rank}",
        color=color,
        fontweight="bold",
        va="bottom",
        fontsize=9,
    )

  ax_macro.set_title(
      f"Macro Overview: Database Search Area [{symbol}] ({len(full_prices):,}"
      " Candles)",
      fontsize=11,
      fontweight="bold",
  )
  ax_macro.set_ylabel("Raw Price", fontsize=9)
  ax_macro.grid(True, linestyle=":", alpha=0.5)
  ax_macro.legend(loc="upper left", fontsize=8, ncol=k)

  # -------------------------------------------------------------------------
  # 2. LOCAL CONTEXT ZOOM (แถวล่าง: แยก k ช่อง)
  # -------------------------------------------------------------------------
  for rank, (idx, score, ret, date_str) in enumerate(
      zip(top_k_indices, top_k_scores, top_k_returns, top_k_dates), 1
  ):
    ax_sub = fig.add_subplot(gs[1, rank - 1])
    color = colors[(rank - 1) % len(colors)]

    start_ctx = max(0, idx - context_padding)
    end_ctx = min(len(full_prices), idx + n + context_padding)

    local_x = np.arange(start_ctx, end_ctx)
    local_y = full_prices[start_ctx:end_ctx]

    # พล็อตเส้นราคารอบข้าง (เส้นประสีเทาอ่อน)
    ax_sub.plot(
        local_x, local_y, color="#888888", linewidth=1.2, linestyle=":"
    )

    # พล็อตไฮไลต์รูปทรงแพตเทิร์น 30 แท่งที่แมตช์ได้ (เส้นหนาเน้นสี)
    match_x = np.arange(idx, idx + n)
    match_y = full_prices[idx : idx + n]
    ax_sub.plot(
        match_x,
        match_y,
        color=color,
        linewidth=2.5,
        label=f"Matched Window ({n} bars)",
    )

    # ถมแถบสีและใส่เส้นประ 2 เส้นขอบซ้าย-ขวา ในกราฟ Zoom ซูมด้วย
    ax_sub.axvspan(idx, idx + n, color=color, alpha=0.25)
    ax_sub.axvline(
        idx, color=color, linestyle="--", linewidth=1.2, alpha=0.8
    )
    ax_sub.axvline(
        idx + n, color=color, linestyle="--", linewidth=1.2, alpha=0.8
    )

    ret_pct = ret * 100
    direction = "🟢 UP" if ret > 0 else "🔴 DOWN"
    date_label = date_str.split(" ")[0] if date_str else ""

    ax_sub.set_title(
        f"Rank {rank} Context\nSim: {score:.4f} | Ret:"
        f" {ret_pct:+.2f}%\n[{date_label}]",
        fontsize=9,
        fontweight="bold",
        color=color,
    )
    ax_sub.grid(True, linestyle=":", alpha=0.5)
    ax_sub.tick_params(axis="x", rotation=30, labelsize=7)

  plt.tight_layout()
  plt.show()