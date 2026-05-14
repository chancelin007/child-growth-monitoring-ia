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