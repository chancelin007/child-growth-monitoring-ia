import numpy as np

def detect_malnutrition_risk(z_scores, threshold=1.5, drift=0.25):
    """
    Détecte une baisse persistante du Z-score.
    """
    s_low = 0
    for z in z_scores:
        # On calcule l'écart par rapport à la normale (0)
        deviation = 0 - z
        s_low = max(0, s_low + deviation - drift)
        
        if s_low > threshold:
            return True, z_scores.index(z)
            
    return False, None