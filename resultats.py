
import streamlit as st

def afficher_resultats():
    st.title("Résultats du Quiz")
    
    # Données fictives de résultats
    resultats = {
        "Nom": ["Alice", "Bob", "Charlie", "David"],
        "Score": [85, 90, 78, 92],
        "Temps (min)": [15, 12, 20, 10]
    }
    
    # Affichage du tableau de résultats
    st.write("Voici les résultats du quiz :")
    st.table(resultats)
