import numpy as np
from scipy.signal import argrelextrema
from sklearn.cluster import KMeans

def get_sr_kmeans(candles, window=3, n_clusters=3):
    """
    หาแนวรับ-แนวต้านหลักด้วย Local Extrema ร่วมกับ K-Means Clustering
    """
    highs = np.array([c['max'] for c in candles])
    lows = np.array([c['min'] for c in candles])
    
    # 1. หาตำแหน่ง Local Extrema (จุด Swing High / Swing Low)
    min_idx = argrelextrema(lows, np.less, order=window)[0]
    max_idx = argrelextrema(highs, np.greater, order=window)[0]
    
    min_prices = lows[min_idx].reshape(-1, 1)
    max_prices = highs[max_idx].reshape(-1, 1)
    
    supports = np.array([])
    resistances = np.array([])
    
    # 2. จัดกลุ่มหา Centroid แนวรับ (ถ้าจุดสวิงมากกว่าจำนวน Cluster)
    if len(min_prices) >= n_clusters:
        kmeans_sup = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(min_prices)
        supports = kmeans_sup.cluster_centers_.flatten()
    elif len(min_prices) > 0:
        supports = min_prices.flatten()

    # 3. จัดกลุ่มหา Centroid แนวต้าน
    if len(max_prices) >= n_clusters:
        kmeans_res = KMeans(n_clusters=n_clusters, n_init=10, random_state=42).fit(max_prices)
        resistances = kmeans_res.cluster_centers_.flatten()
    elif len(max_prices) > 0:
        resistances = max_prices.flatten()
        
    return np.sort(supports), np.sort(resistances)