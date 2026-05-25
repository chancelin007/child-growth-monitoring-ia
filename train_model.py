# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def generate_mock_trajectory_data():
    """Simule des données de trajectoires pour l'entraînement."""
    np.random.seed(42)
    data = []
    
    for enfant_id in range(500): # 500 enfants simulés
        age_initial = np.random.randint(30, 180) # Âge en jours
        sexe = np.random.choice([0, 1])
        z_initial = np.random.normal(0, 1) # Couloir de base de l'enfant
        
        # Simuler 4 visites
        z_current = z_initial
        history = [z_initial]
        
        # Déterminer si cet enfant va subir une malnutrition ou non
        is_malnourished = np.random.choice([0, 1], p=[0.8, 0.2])
        
        for visite in range(1, 4):
            age = age_initial + (visite * 30) # Visites tous les 30 jours
            
            if is_malnourished and visite >= 2:
                # Chute sévère du Z-score
                z_current -= np.random.uniform(0.4, 0.8)
            else:
                # Fluctuation normale
                z_current += np.random.normal(0, 0.1)
                
            history.append(z_current)
            
            # Feature Engineering pour l'instant T
            delta_z = history[-1] - history[-2]
            velocite = delta_z / 30.0 # Variation par jour
            
            # CUSUM simplifié
            cusum = max(0, (history[0] - history[-1]) - 0.25)
            
            # On n'enregistre pour l'entraînement que les lignes à partir de la visite 2
            if visite >= 2:
                data.append({
                    'age_jours': age,
                    'z_score_actuel': z_current,
                    'delta_z': delta_z,
                    'velocite': velocite,
                    'cusum': cusum,
                    'label': 1 if (is_malnourished and visite == 3) else 0
                })
                
    return pd.DataFrame(data)

# 1. Préparation des données
df = generate_mock_trajectory_data()

X = df[['age_jours', 'z_score_actuel', 'delta_z', 'velocite', 'cusum']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_test_split=0.2, random_state=42)

# 2. Entraînement du modèle
print("Entraînement de l'IA (Random Forest)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Évaluation
y_pred = model.predict(X_test)
print("\nRapport de performance :")
print(classification_report(y_test, y_pred))

# 4. Sauvegarde du modèle entraîné
joblib.dump(model, 'models/malnutrition_rf_model.pkl')
print("Modèle sauvegardé dans 'models/malnutrition_rf_model.pkl'")