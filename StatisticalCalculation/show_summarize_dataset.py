import numpy as np

def summarize_dataset(filepath, price_key='full_prices', return_key='future_returns'):
    # 1. โหลดข้อมูลจากไฟล์ .npz
    data = np.load(filepath)
    
    # 2. คำนวณสถิติของราคาดิบ (Raw Price Statistics)
    raw_prices = data[price_key]
    mean_price = np.mean(raw_prices)
    std_price = np.std(raw_prices)  # ค่าความผันผวน (Volatility)
    max_price = np.max(raw_prices)
    min_price = np.min(raw_prices)
    
    # 3. คำนวณสัดส่วนทิศทางผลตอบแทน (Target Distribution)
    returns = data[return_key]
    total_windows = len(returns)
    
    up_count = np.sum(returns > 0)
    down_count = np.sum(returns < 0)
    flat_count = np.sum(returns == 0)
    
    bullish_pct = (up_count / total_windows) * 100
    bearish_pct = (down_count / total_windows) * 100
    neutral_pct = (flat_count / total_windows) * 100
    
    # 4. สรุปผลลัพธ์เป็น Dictionary
    summary = {
        "Total Windows (N)": total_windows,
        "Mean Price": round(float(mean_price), 5),
        "Volatility (Std Dev)": round(float(std_price), 5),
        "Max Price": round(float(max_price), 5),
        "Min Price": round(float(min_price), 5),
        "Bullish Ratio (%)": round(bullish_pct, 2),
        "Bearish Ratio (%)": round(bearish_pct, 2),
        "Neutral Ratio (%)": round(neutral_pct, 2)
    }
    
    return summary

def show_data_dict(dict: dict):
    for key, val in dict.items():
        print(f"{key} : {val}")

if __name__ == "__main__":
    summarize = summarize_dataset('db.npz')
    show_data_dict(summarize)