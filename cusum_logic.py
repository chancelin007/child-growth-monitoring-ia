import numpy as np

def detect_malnutrition_risk(z_scores, threshold=1.5, drift=0.25):
    """
    Détecte une baisse significative et persistante du Z-score.
    - z_scores : Liste des derniers Z-scores de l'enfant
    - threshold (H) : Seuil d'alerte (plus il est bas, plus c'est sensible)
    - drift (K) : Tolérance pour les petites variations
    """
    s_low = 0  # Somme cumulée basse
    
    for i, z in enumerate(z_scores):
        # On calcule l'écart par rapport à la normale (0)
        # On s'inquiète si z devient négatif (perte de poids)
        deviation = 0 - z
        s_low = max(0, s_low + deviation - drift)
        
        if s_low > threshold:
            return True, i  # Alerte déclenchée à l'indice i
            
    return False, None