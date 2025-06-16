import streamlit as st

def afficher_quiz():
    st.title("Quiz Interactif")

    # Questions du quiz
    questions = {
        "Quelle est la capitale de la France?": ["Paris", "Londres", "Berlin", "Madrid"],
        "Quel est le plus grand océan du monde?": ["Atlantique", "Pacifique", "Indien", "Arctique"],
        "Quelle est la planète la plus proche du soleil?": ["Terre", "Mars", "Mercure", "Venus"]
    }

    # Réponses correctes
    correct_answers = {
        "Quelle est la capitale de la France?": "Paris",
        "Quel est le plus grand océan du monde?": "Pacifique",
        "Quelle est la planète la plus proche du soleil?": "Mercure"
    }

    # Initialiser les réponses dans st.session_state
    if 'responses' not in st.session_state:
        st.session_state['responses'] = {question: None for question in questions}

    # Affichage des questions
    for question, options in questions.items():
        st.session_state['responses'][question] = st.radio(question, options, key=question)

    # Bouton pour valider les réponses
    if st.button("Valider mes réponses"):
        score = 0
        for question, correct_answer in correct_answers.items():
            if st.session_state['responses'][question] == correct_answer:
                score += 1
        st.write(f"Votre score final est : {score}/{len(questions)}")


