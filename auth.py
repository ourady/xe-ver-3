import streamlit as st
import csv
import hashlib
import os



# Fonction pour hacher le mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction pour vérifier les identifiants depuis un fichier CSV
def verifier_identifiants(nom_utilisateur, mot_de_passe):
    if not os.path.exists("utilisateurs.csv"):
        return False, "Fichier utilisateurs.csv introuvable."

    with open("utilisateurs.csv", "r") as f:
        lecteur = csv.DictReader(f)
        for utilisateur in lecteur:
            if utilisateur["nom_utilisateur"] == nom_utilisateur:
                if utilisateur["mot_de_passe"] == hash_password(mot_de_passe):
                    return True, "Connexion réussie."
                else:
                    return False, "Mot de passe incorrect."
        return False, "Nom d'utilisateur non trouvé."

# Interface Streamlit
def afficher_connexion():
    st.title("Connexion utilisateur")
    st.write("Répertoire courant :", os.getcwd())
    st.write("Fichiers présents :", os.listdir())

    nom_utilisateur = st.text_input("Nom d'utilisateur")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        reussi, message = verifier_identifiants(nom_utilisateur, mot_de_passe)
        if reussi:
            st.success(message)
            st.session_state["utilisateur"] = nom_utilisateur
        else:
            st.error(message)
