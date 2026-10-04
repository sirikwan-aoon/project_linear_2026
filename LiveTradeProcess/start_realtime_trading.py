from LiveTradeProcess.prepare_live_prices import prepare_live_prices
from LiveTradeProcess.order_process import check_order_result, execute_order
from LiveTradeProcess.predict_pattern_knn import predict_pattern_knn
from LiveTradeProcess.plot_match_pattern import plot_matched_patterns_macro, plot_matched_patterns_with_local_zoom
from SupportResistanceAnalyze.get_sr_kmeans import get_sr_kmeans
from SupportResistanceAnalyze.is_near_sr_level import is_near_sr_level

from iqoptionapi.stable_api import IQ_Option
import numpy as np
import time

# ========================================================
# Step 3: Real-time Loop (Candle Synced)
# ========================================================
def start_realtime_trading(email, password, X_denoised, future_returns, timestamps, prices, symbol="EURUSD-OTC", amount=10, duration=1):
    API = IQ_Option(email, password)
    API.connect()
    
    if not API.check_connect():
        print("❌ เชื่อมต่อ IQ Option ไม่สำเร็จ")
        return

    print(f"✅ เชื่อมต่อ IQ Option สำเร็จ! เริ่มเฝ้าราคา {symbol}...")

    while True:
        try:
            # 1. ดึงราคา 30 แท่งล่าสุดผ่าน Connection เดิม (เร็วกว่า ไม่ต้อง Re-login)
            candles = API.get_candles(symbol, 60, 30, time.time())
            live_prices = np.array([c['close'] for c in candles])
            
            p_live_norm = prepare_live_prices(live_prices)
            
            # 2. คำนวณ Pattern Matching
            result = predict_pattern_knn(
                p_live_norm, X_denoised, future_returns, timestamps, k=5, min_win_rate=80.0
            )

            plot_matched_patterns_macro(p_live_norm, X_denoised, result, prices, symbol="EURUSD-OTC") #กรณีที่ต้องการดูกราฟแพทเทิร์นที่คล้ายกัน กับ แพทเทิร์นปัจจุบัน
            # plot_matched_patterns_with_local_zoom(prices, result, n=30, context_padding=50, symbol="EURUSD-OTC")

            # ดึงราคาย้อนหลัง 100-150 แท่งเพื่อหาแนวระดับใหญ่
            candles = API.get_candles(symbol, 60, 150, time.time())
            current_price = candles[-1]['close']

            # หาแนวรับ-แนวต้าน 3 แนวหลัก (K=3)
            supports, resistances = get_sr_kmeans(candles, window=3, n_clusters=3)

            # เช็คระยะห่างว่าใกล้แนวรับ/ต้าน หรือไม่ ( tolerance 0.05% )
            near_support = is_near_sr_level(current_price, supports, tolerance_pct=0.0005)
            near_resistance = is_near_sr_level(current_price, resistances, tolerance_pct=0.0005)

            signal = result['signal']
            is_confirmed = False

            # ยืนยันสัญญาณด้วยแนวรับ-แนวต้าน
            if signal == "CALL" and near_support:
                is_confirmed = True
                print(f"\n🎯 [{time.strftime('%H:%M:%S')}] [CONFIRMED] สัญญาณ CALL + แตะแนวรับที่ {current_price:.5f}")
            elif signal == "PUT" and near_resistance:
                is_confirmed = True
                print(f"\n🎯 [{time.strftime('%H:%M:%S')}] [CONFIRMED] สัญญาณ PUT + แตะแนวต้านที่ {current_price:.5f}")
            elif signal != "WAIT":
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ ข้ามสัญญาณ {signal}: รูปทรงตรงแต่ราคาไม่อยู่ใกล้แนวรับ-แนวต้าน", end="\r")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] รูปทรงยังไม่ชัดเจน (WAIT)", end="\r")

            # ยิงออเดอร์เมื่อผ่านการกรองครบทุกเงื่อนไขเท่านั้น
            if is_confirmed:
                win_rate = result['win_rate_call'] if signal == 'CALL' else result['win_rate_put']
                print(f"📊 Win Rate คาดการณ์: {win_rate:.1f}% | ผลตอบแทนเฉลี่ย: {result['avg_return_%']:.4f}%")
                
                # ส่งคำสั่งเข้า API
                success, order_id = execute_order(API, signal, active=symbol, amount=amount, duration=duration)
                
                # หากยิงสำเร็จ พักลูปตามเวลา duration เพื่อป้องกันการยิงซ้ำซ้อนระหว่างถือไม้
                if success:
                    time.sleep(duration * 60 - 2)

                    check_order_result(API, order_id)

            # 4. รอจนกระทั่งจบวินาทีที่ 59 เพื่อเริ่มเช็คแท่งถัดไปพอดี
            time_to_next_minute = 60 - (time.time() % 60)
            time.sleep(time_to_next_minute)

        except Exception as e:
            print(f"\n⚠️ เกิดข้อผิดพลาด: {e}")
            time.sleep(2)