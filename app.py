# Extraits de modifications pour app.py
import joblib
import numpy as np

# Charger le modèle d'IA au démarrage
try:
    ia_model = joblib.load('models/malnutrition_rf_model.pkl')
except:
    ia_model = None
    print("Attention: Modèle d'IA non trouvé, repli sur le CUSUM uniquement.")

# Liste pour stocker les dictionnaires de visites complexes
history_visites = [] 

def verifier_sante():
    try:
        poids = float(entry_poids.get())
        age = int(entry_age.get())
        
        # 1. Calcul du Z-Score actuel via vos standards OMS
        z = calculate_z_score(poids, age, oms_df)
        
        # 2. Préparation des caractéristiques pour l'IA
        delta_z = 0
        velocite = 0
        cusum = 0
        
        if len(history_visites) > 0:
            last_visit = history_visites[-1]
            delta_time = age - last_visit['age']
            if delta_time > 0:
                delta_z = z - last_visit['z_score']
                velocite = delta_z / delta_time
                
            # Calcul du CUSUM basé sur la première visite de l'historique
            z_cible = history_visites[0]['z_score']
            cusum = max(0, (z_cible - z) - 0.25)

        # Enregistrement de la visite actuelle
        history_visites.append({'age': age, 'z_score': z})
        
        # 3. Prédiction par le modèle d'IA
        alert = False
        if ia_model and len(history_visites) >= 2:
            # Créer le vecteur de caractéristiques correspondant à l'entraînement
            features = np.array([[age, z, delta_z, velocite, cusum]])
            prediction = ia_model.predict(features)
            alert = (prediction[0] == 1)
        else:
            # Système de secours : Votre logique CUSUM d'origine si l'IA n'est pas prête
            list_z_scores = [v['z_score'] for v in history_visites]
            alert, _ = detect_malnutrition_risk(list_z_scores)
        
        # 4. Affichage des résultats (votre logique d'origine)
        resultat = f"Z-Score actuel : {z:.2f}\n"
        if alert:
            resultat += "!!! ALERTE IA : Risque critique détecté !!!"
            messagebox.showwarning("Alerte Santé", "L'IA détecte une dérive pathologique.")
        else:
            resultat += "Statut : Trajectoire normale."
            messagebox.showinfo("Résultat", "L'enfant suit sa courbe normalement.")
            
        label_resultat.config(text=resultat)
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")