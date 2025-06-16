
import streamlit as st

def afficher_contact():
    st.title("Contactez-nous")
    st.write("Remplissez le formulaire ci-dessous pour nous contacter.")

    with st.form("form_contact"):
        nom = st.text_input("Nom")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Envoyer")

        if submit:
            st.success("Merci pour votre message ! Nous vous répondrons bientôt.")
