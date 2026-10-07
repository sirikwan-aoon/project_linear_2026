import numpy as np
import pandas as pd

def audit_data_cleaning_proof(
    npz_filepath,
    window_size=30,
    forecast_horizon=1,
    expected_interval_sec=60,
):

  npz_data = np.load(npz_filepath, allow_pickle=True)

  # 1. ดึงข้อมูลราคาดิบ/ตราเวลา
  raw_data = npz_data["raw_timestamps"]
  if isinstance(raw_data, np.ndarray) and raw_data.ndim == 0:
    raw_data = raw_data.item()

  if isinstance(raw_data, pd.DataFrame):
    timestamps = raw_data["from"].values
  else:
    timestamps = np.array(raw_data)

  total_raw = len(timestamps)  # 86,400

  # 2. จำนวน Window จริงที่มีในไฟล์ .npz
  valid_windows = len(npz_data["future_returns"])  # 84,570
  total_dropped = total_raw - valid_windows  # 1,830

  # 3. คำนวณ Effective Window Size รวมระยะพยากรณ์อนาคต
  effective_window = window_size + forecast_horizon  # 30 + 1 = 31
  loss_per_segment = effective_window - 1  # 30

  # 4. ตรวจหา Time Gaps ในข้อมูลดิบ
  time_diffs = np.diff(timestamps)
  gap_indices = np.where(time_diffs > expected_interval_sec)[0]
  total_gaps = len(gap_indices)  # 60
  num_segments = total_gaps + 1  # 61 ท่อนข้อมูล

  # 5. คำนวณ Expected Dropped ตามทฤษฎีทางสถิติ
  expected_dropped = num_segments * loss_per_segment  # 61 * 30 = 1,830
  other_loss = total_dropped - expected_dropped

  print("=" * 65)
  print("      DATA CLEANING AUDIT & VERIFICATION REPORT")
  print("=" * 65)
  print(
      "จำนวนแท่งเทียนราคาดิบตั้งต้น (Theoretical Total) :"
      f" {total_raw:>8,} แท่งเทียน (100.00%)"
  )
  print(
      "จำนวนชุดข้อมูลที่สมบูรณ์ (.npz Valid Windows)      :"
      f" {valid_windows:>8,} ชุด ({valid_windows/total_raw*100:.2f}%)"
  )
  print(
      "จำนวนชุดข้อมูลที่ถูกตัดออกจริง (Actual Dropped)    :"
      f" {total_dropped:>8,} ชุด ({total_dropped/total_raw*100:.2f}%)"
  )
  print("-" * 65)
  print("การแจกแจงวิเคราะห์โครงสร้างข้อมูล:")
  print(
      f"  1. จำนวน Time Gaps ตรวจพบ (ห่าง > {expected_interval_sec}s) :"
      f" {total_gaps:>6,} จุด (แบ่งได้ {num_segments} Segments)"
  )
  print(
      f"  2. Effective Window Loss ({num_segments} Segments x {loss_per_segment}"
      f" Bars) : {expected_dropped:>6,} ชุด"
  )
  print(
      f"  3. Unexplained / Filter Loss                     :"
      f" {other_loss:>6,} ชุด"
  )

  # 6. ตรวจสอบความถูกต้องสมบูรณ์ (Verification Status)
  is_passed = total_dropped == expected_dropped
  status_str = "[PASSED]" if is_passed else "[FAILED / MISMATCH]"

  print("=" * 65)
  print(f"ผลการตรวจสอบความสอดคล้องทางคณิตศาสตร์: {status_str}")
  print("=" * 65)

if __name__ == "__main__":
    audit_data_cleaning_proof('db.npz', window_size=30)