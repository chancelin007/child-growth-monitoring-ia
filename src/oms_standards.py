import pandas as pd

def calculate_z_score(weight, age_days, oms_data):
    # Trouver la ligne correspondant à l'âge le plus proche
    row = oms_data.iloc[(oms_data['Age_days'] - age_days).abs().argsort()[:1]]
    L = row['L'].values[0]
    M = row['M'].values[0]
    S = row['S'].values[0]
    
    # Formule du Z-score de l'OMS
    z_score = (((weight / M)**L) - 1) / (L * S)
    return z_score