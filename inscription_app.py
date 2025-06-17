import streamlit as st
import hashlib
import csv

def afficher_inscription():
    st.title("Inscription Utilisateur")

    # Formulaire d'inscription
    with st.form(key='inscription_form'):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type='password')
        submit_button = st.form_submit_button(label="S'inscrire")

    if submit_button:
        # Hacher le mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Vérifier si l'utilisateur est déjà inscrit
        user_exists = False
        with open('nouvel_utilisateur_inscrit.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    user_exists = True
                    break

        if user_exists:
            st.error("Utilisateur déjà inscrit.")
        else:
            # Ajouter le nouvel utilisateur
            with open('nouvel_utilisateur_inscrit.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, hashed_password])
            st.success("Inscription réussie !")
