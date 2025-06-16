import tkinter as tk
from tkinter import ttk
import os
import webbrowser

# Chemin vers le fichier HTML
CHEMIN_HTML = "html/gestion_utilisateurs.html"

def ouvrir_interface_utilisateur():
    chemin_absolu = os.path.abspath(CHEMIN_HTML)
    webbrowser.open(f"file://{chemin_absolu}")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Application principale")

# Bouton pour ouvrir l'interface HTML
bouton = ttk.Button(fenetre, text="Gérer les utilisateurs", command=ouvrir_interface_utilisateur)
bouton.pack(pady=20)

fenetre.mainloop()
