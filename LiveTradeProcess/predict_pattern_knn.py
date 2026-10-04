from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def predict_pattern_knn(
    query_norm,
    X_denoised,
    future_returns,
    timestamps,
    k=5,
    threshold=0.00001,
    min_win_rate=60.0,
):
  """พยากรณ์ทิศทางราคาอนาคตด้วย k-NN Pattern Matching

  Parameters:
  - query_norm: เวกเตอร์ราคาปัจจุบันที่ผ่าน Mean Centering และ Normalization แล้ว
  - X_denoised: เมทริกซ์คลังข้อมูลรูปทรงกราฟในอดีต (m x n)
  - future_returns: อัตราผลตอบแทนอนาคตที่ผูกไว้กับคลังข้อมูล (ขนาด m)
  - timestamps: Array เก็บ Unix Timestamp ของทรงกราฟในอดีต (ขนาด m)
  - k: จำนวนแพตเทิร์นที่คล้ายที่สุดที่ต้องการดึงมาเปรียบเทียบ (Default: 5)
  - threshold: ค่าเฉลี่ยผลตอบแทนขั้นต่ำในการกรองสัญญาณ (Default: 0.00001)
  - min_win_rate: เกณฑ์ Win Rate ขั้นต่ำในการส่งสัญญาณเป็น % (Default: 60.0)
  """
  # 1. คำนวณ Cosine Similarity
  scores = cosine_similarity(query_norm.reshape(1, -1), X_denoised)[0]

  # 2. ดึง k อันดับแรกที่คล้ายที่สุด
  top_k_indices = np.argsort(scores)[-k:][::-1]
  top_k_scores = scores[top_k_indices]
  top_k_returns = future_returns[top_k_indices]

  # 3. ดึงและแปลง Unix Timestamp เป็นรูปแบบวันที่-เวลา (YYYY-MM-DD HH:MM:SS)
  top_k_raw_ts = timestamps[top_k_indices]
  top_k_dates = [
      datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
      for ts in top_k_raw_ts
  ]

  # 4. คำนวณ Win Rate และค่าเฉลี่ยผลตอบแทน
  up_count = np.sum(top_k_returns > 0)
  down_count = np.sum(top_k_returns < 0)

  win_rate_call = (up_count / k) * 100
  win_rate_put = (down_count / k) * 100
  avg_return = np.nanmean(top_k_returns)

  # 5. ตัดสินใจส่งสัญญาณเทรด
  if win_rate_call >= min_win_rate and avg_return > threshold:
    signal = "CALL"
  elif win_rate_put >= min_win_rate and avg_return < -threshold:
    signal = "PUT"
  else:
    signal = "WAIT"

  return {
      "signal": signal,
      "win_rate_call": win_rate_call,
      "win_rate_put": win_rate_put,
      "avg_return_%": avg_return * 100,
      "top_k_indices": top_k_indices,
      "top_k_scores": top_k_scores,
      "top_k_returns": top_k_returns,
      "top_k_dates": top_k_dates,  # คืนค่า List ของ String วันที่และเวลา
  }