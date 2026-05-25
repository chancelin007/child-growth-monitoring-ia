import pandas as pd
from src.oms_standards import calculate_z_score
from src.cusum_logic import detect_malnutrition_risk
from src.alerts import send_malnutrition_alert  # On importe l'alerte

# 1. Configuration
oms_df = pd.read_csv('data/raw/oms_weight_for_age.csv')
CHILD_ID = "CHAD-2024-001"

# 2. Données de l'enfant (Simulation de perte de poids)
age_history = [0, 30, 60, 90, 120, 150]
weight_history = [3.4, 4.4, 5.2, 5.8, 5.9, 5.8]

# 3. Calcul des Z-scores
z_scores = []
for i in range(len(age_history)):
    z = calculate_z_score(weight_history[i], age_history[i], oms_df)
    z_scores.append(z)

# 4. Détection et Alerte
alert_triggered, index = detect_malnutrition_risk(z_scores)

if alert_triggered:
    # Si l'IA détecte un risque, on appelle le module d'alerte
    send_malnutrition_alert(CHILD_ID, age_history[index], z_scores[index])
else:
    print("Suivi normal : aucune alerte nécessaire.")