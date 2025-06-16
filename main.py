import tkinter as tk
import subprocess
from tkinter import messagebox

def lancer_tkinter(fenetre):
    try:
        from interface_tkinter import QuizApp
        fenetre.destroy()  # Fermer le menu seulement ici
        app = QuizApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lancer l'interface Tkinter : {e}")

def lancer_streamlit():
    try:
        subprocess.Popen(["streamlit", "run", "interface_streamlit.py"])
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Streamlit n'est pas installé ou introuvable.")

def menu():
    fenetre = tk.Tk()
    fenetre.title("Choix de l'interface")

    label = tk.Label(fenetre, text="Choisissez l'interface à lancer :", font=("Arial", 14))
    label.pack(pady=10)

    bouton1 = tk.Button(fenetre, text="Interface Tkinter", command=lambda: lancer_tkinter(fenetre))
    bouton1.pack(pady=5)

    bouton2 = tk.Button(fenetre, text="Interface Streamlit", command=lancer_streamlit)
    bouton2.pack(pady=5)

    bouton3 = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
    bouton3.pack(pady=5)

    fenetre.mainloop()

if __name__ == "__main__":
    menu()
