# src/cusum_logic.py
import numpy as np

def detect_malnutrition_risk(z_scores, threshold=1.5, drift=0.25):
    if len(z_scores) < 2:
        return False, None
        
    s_low = 0
    # On définit la cible comme le premier Z-score connu de l'enfant (ou une moyenne des premiers)
    z_cible = z_scores[0] 
    
    for i, z in enumerate(z_scores):
        # L'écart se calcule par rapport à la trajectoire propre de l'enfant
        deviation = z_cible - z
        s_low = max(0, s_low + deviation - drift)
        
        if s_low > threshold:
            return True, i
            
    return False, None