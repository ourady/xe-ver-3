import streamlit as st

def afficher_quiz():
    st.title("Quiz Interactif")

    questions = {
        "Quelle est la capitale de la France?": ["Paris", "Londres", "Berlin", "Madrid"],
        "Quel est le plus grand océan du monde?": ["Atlantique", "Pacifique", "Indien", "Arctique"],
        "Quelle est la planète la plus proche du soleil?": ["Terre", "Mars", "Mercure", "Venus"]
    }

    correct_answers = {
        "Quelle est la capitale de la France?": "Paris",
        "Quel est le plus grand océan du monde?": "Pacifique",
        "Quelle est la planète la plus proche du soleil?": "Mercure"
    }

    if 'responses' not in st.session_state:
        st.session_state['responses'] = {question: None for question in questions}

    for question, options in questions.items():
        st.session_state['responses'][question] = st.radio(question, options, key=question)

    if st.button("Valider mes réponses"):
        score = sum(
            1 for q, a in correct_answers.items()
            if st.session_state['responses'][q] == a
        )
        st.success(f"Votre score final est : {score}/{len(questions)}")

def afficher_apropos():
    st.title("À propos")
    st.write("Cette plateforme de quiz a été développée pour vous offrir une expérience d'apprentissage interactive et amusante.")

def afficher_contact():
    st.title("Contact")
    st.write("Pour toute question ou suggestion, veuillez nous contacter à l'adresse suivante : contact@quizplatform.com")

def afficher_connexion():
    st.title("Connexion")
    st.write("Veuillez entrer vos identifiants pour vous connecter.")

def afficher_resultats():
    st.title("Résultats")
    st.write("Voici vos résultats de quiz.")

# Barre de navigation
onglet = st.sidebar.radio("Navigation", ["Accueil", "Quiz", "À propos", "Contact", "Connexion"])

# Affichage des pages selon l'onglet sélectionné
if onglet == "Accueil":
    st.title("Bienvenue sur la plateforme de quiz !")
    st.write("Choisissez un onglet à gauche pour commencer.")
elif onglet == "Quiz":
    afficher_quiz()
elif onglet == "À propos":
    afficher_apropos()
elif onglet == "Contact":
    afficher_contact()
elif onglet == "Connexion":
    afficher_connexion()
