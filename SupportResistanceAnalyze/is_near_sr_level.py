import numpy as np

def is_near_sr_level(current_price, levels, tolerance_pct=0.0005):
    """
    เช็คว่าราคาปัจจุบันอยู่ใกล้แนวรับ/แนวต้านในระยะที่กำหนดหรือไม่
    tolerance_pct: ระยะเผื่อ (0.0005 คือ 0.05% ของราคาปัจจุบัน)
    """
    if len(levels) == 0:
        return False
        
    # คำนวณระยะห่างระหว่างราคาปัจจุบันกับทุกแนว
    distances = np.abs(levels - current_price) / current_price
    
    # ถ้าระยะห่างน้อยกว่าค่า tolerance แสดงว่าอยู่ใกล้แนว
    return np.min(distances) <= tolerance_pct