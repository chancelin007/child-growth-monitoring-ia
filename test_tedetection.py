import pandas as pd
from src.oms_standards import calculate_z_score
from src.cusum_logic import detect_malnutrition_risk

# 1. Charger les données de référence de l'OMS
try:
    oms_df = pd.read_csv('data/raw/oms_weight_for_age.csv')
except FileNotFoundError:
    print("Erreur : Le fichier CSV de l'OMS est introuvable !")
    exit()

# 2. Simuler les pesées d'un enfant (Enfant qui commence à perdre du poids)
# Age en jours : [0, 30, 60, 90, 120, 150]
# Poids en kg  : [3.4, 4.4, 5.2, 5.8, 5.9, 5.8] <--- On voit une stagnation/baisse à la fin
age_history = [0, 30, 60, 90, 120, 150]
weight_history = [3.4, 4.4, 5.2, 5.8, 5.9, 5.8]

# 3. Calculer les Z-scores pour chaque pesée
z_scores = []
for i in range(len(age_history)):
    z = calculate_z_score(weight_history[i], age_history[i], oms_df)
    z_scores.append(z)
    print(f"Jour {age_history[i]} : Poids = {weight_history[i]}kg | Z-Score = {z:.2f}")

# 4. Lancer la détection CUSUM
alert, index = detect_malnutrition_risk(z_scores)

if alert:
    print(f"\n/!\\ ALERTE DÉTECTÉE à la pesée n°{index+1} (Jour {age_history[index]})")
    print("Action : Envoi SMS au centre de santé recommandé.")
else:
    print("\nCroissance normale. Aucune alerte.")