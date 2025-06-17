import streamlit as st
from quiz import afficher_quiz
from apropos import afficher_apropos
from contact import afficher_contact
from resultats import afficher_resultats
from auth import afficher_connexion
from inscription_app import afficher_inscription

st.set_page_config(page_title="Bienvenue", page_icon="🎉", layout="wide")

# Barre de navigation en haut
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🎯 Quiz"):
        st.session_state['onglet'] = "Quiz"

with col2:
    if st.button("ℹ️ À propos"):
        st.session_state['onglet'] = "À propos"

with col3:
    if st.button("📬 Contact"):
        st.session_state['onglet'] = "Contact"

with col4:
    if st.button("🔐 Connexion"):
        st.session_state['onglet'] = "Connexion"

with col5:
    if st.button("📝 Inscription"):
        st.session_state['onglet'] = "Inscription"

# Définir l'onglet actif
onglet = st.session_state.get("onglet", "Accueil")

# Affichage du contenu selon l'onglet
if onglet == "Accueil":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Bienvenue sur la plateforme de quiz !</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Explorez, apprenez et testez vos connaissances avec nos quiz interactifs.</p>", unsafe_allow_html=True)
elif onglet == "Quiz":
    afficher_quiz()
elif onglet == "À propos":
    afficher_apropos()
elif onglet == "Contact":
    afficher_contact()
elif onglet == "Connexion":
    afficher_connexion()
elif onglet == "Inscription":
    afficher_inscription()

