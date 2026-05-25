
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

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from src.oms_standards import calculate_z_score
from src.cusum_logic import detect_malnutrition_risk
from src.alerts import send_malnutrition_alert

# Chargement des données
oms_df = pd.read_csv('data/raw/oms_weight_for_age.csv')
history_z = []


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

        # Calcul
        z = calculate_z_score(poids, age, oms_df)
        history_z.append(z)
        
        # Diagnostic
        alert, _ = detect_malnutrition_risk(history_z)
        
        resultat = f"Z-Score actuel : {z:.2f}\n"
        if alert:
            resultat += "!!! ALERTE : Risque détecté !!!"
            send_malnutrition_alert("ENFANT-TEST", age, z)
            messagebox.showwarning("Alerte Santé", "Risque de malnutrition détecté !")
        else:
            resultat += "Statut : Croissance normale."

            messagebox.showinfo("Résultat", "L'enfant suit sa courbe normalement.")
            
        label_resultat.config(text=resultat)
        
    except Exception as e:

        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

        messagebox.showerror("Erreur", "Veuillez entrer des chiffres valides.")

# Création de la fenêtre
root = tk.Tk()
root.title("IA Suivi Croissance - Tchad")
root.geometry("300x250")

tk.Label(root, text="Âge de l'enfant (jours) :").pack(pady=5)
entry_age = tk.Entry(root)
entry_age.pack()

tk.Label(root, text="Poids de l'enfant (kg) :").pack(pady=5)
entry_poids = tk.Entry(root)
entry_poids.pack()

tk.Button(root, text="Analyser la santé", command=verifier_sante, bg="green", fg="white").pack(pady=20)

label_resultat = tk.Label(root, text="")
label_resultat.pack()

root.mainloop()

