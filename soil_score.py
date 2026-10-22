import math

def calculate_soil_score(n, p, k, humidity, ph):
    if n < 40: n_score = n / 40.0
    elif 40 <= n <= 90: n_score = 1.0
    else: n_score = max(0.0, 1.0 - ((n - 90) / (140.0 - 90.0)))
        
    if p < 35: p_score = p / 35.0
    elif 35 <= p <= 75: p_score = 1.0
    else: p_score = max(0.0, 1.0 - ((p - 75) / (145.0 - 75.0)))
        
    if k < 25: k_score = k / 25.0
    elif 25 <= k <= 65: k_score = 1.0
    else: k_score = max(0.0, 1.0 - ((k - 65) / (205.0 - 65.0)))
        
    if humidity < 50: h_score = humidity / 50.0
    elif 50 <= humidity <= 90: h_score = 1.0
    else: h_score = max(0.0, 1.0 - ((humidity - 90) / (100.0 - 90.0)))
        
    if 6.0 <= ph <= 7.5: ph_score = 1.0
    elif ph < 6.0: ph_score = ph / 6.0
    else: ph_score = (14.0 - ph) / (14.0 - 7.5)
    ph_score = max(0.0, min(ph_score, 1.0))

    total_nutrients = n + p + k
    if total_nutrients > 0:
        p_n, p_p, p_k = n / total_nutrients, p / total_nutrients, k / total_nutrients
        deviation = math.sqrt((p_n - 0.38)**2 + (p_p - 0.35)**2 + (p_k - 0.27)**2)
        balance_factor = 1.0 - min(0.35, 1.8 * deviation)
    else:
        balance_factor = 0.5

    base_score = (n_score * 0.25 + p_score * 0.20 + k_score * 0.20 + ph_score * 0.20 + h_score * 0.15) * 100
    final_score = max(0.0, min(base_score * balance_factor, 100.0))
    
    if final_score <= 40.0: label, color = "Poor", "red"
    elif final_score <= 70.0: label, color = "Medium", "orange"
    else: label, color = "Good", "green"
        
    return round(final_score, 2), label, color
    