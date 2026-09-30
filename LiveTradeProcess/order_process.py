import time

def execute_order(API, signal, active="EURUSD-OTC", amount=10, duration=1):
    action = signal.lower()
    
    # แก้ไข: คืนค่า 2 ตัวแปรให้ตรงกับฝั่งรับเสมอ
    if action not in ["call", "put"]:
        print(f"⚠️ สัญญาณข้ามการทำงาน: {signal}")
        return False, None

    status, order_id = API.buy(amount, active, action, duration)
    
    if status:
        print(f"✅ [{time.strftime('%H:%M:%S')}] เปิดออเดอร์สำเร็จ! | ทิศทาง: {signal} | ID: {order_id} | จำนวน: ${amount} | เวลา: {duration} นาที")
        return True, order_id
    else:
        print(f"❌ [{time.strftime('%H:%M:%S')}] เปิดออเดอร์ไม่สำเร็จ! เช็คยอดเงินหรือการเชื่อมต่อ")
        return False, None


def check_order_result(API, order_id):
    """
    check_win_v3 คืนค่า float เพียงตัวเดียว (ไม่ใช้ Tuple)
    """
    profit = API.check_win_v3(order_id)
    
    if profit > 0:
        print(f"🎉 [{time.strftime('%H:%M:%S')}] [RESULT] WIN! | กำไร: +${profit:.2f}")
    elif profit < 0:
        print(f"💀 [{time.strftime('%H:%M:%S')}] [RESULT] LOSS | ขาดทุน: -${abs(profit):.2f}")
    else:
        print(f"➖ [{time.strftime('%H:%M:%S')}] [RESULT] EQUAL | คืนเงินทุน: $0.00")
        
    return profit