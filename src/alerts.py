def send_malnutrition_alert(child_id, day, z_score):
    """
    Simule l'envoi d'une alerte (SMS/Notification).
    """
    message = (
        f"--- ALERTE SANTÉ ---\n"
        f"ID Enfant: {child_id}\n"
        f"Diagnostic: Risque de malnutrition détecté au jour {day}.\n"
        f"Z-Score actuel: {z_score:.2f}\n"
        f"Action: Une visite à domicile est requise sous 48h."
    )
    
    print("\n[SERVEUR D'ALERTE] Envoi du SMS en cours...")
    print(message)
    print("[SERVEUR D'ALERTE] SMS envoyé avec succès.\n")