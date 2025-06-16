import os
import tkinter as tk
from tkinter import messagebox
import webbrowser

class HTMLViewer:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Explorateur HTML")

        # Label pour afficher le chemin du fichier ouvert
        self.path_label = tk.Label(self.parent, text="Sélectionnez un fichier HTML à ouvrir", fg="blue")
        self.path_label.pack(pady=5)

        # Liste des fichiers HTML
        html_files = [
            ("Ouvrir user_management.html", "user_management.html"),
            ("Ouvrir quiz_user_management.html", "quiz_user_management.html"),
            ("./fichierquizz", "./fichierquizz"),
            ("./fichierquizz/manager.html", "./fichierquizz/manager.html"),
            ("declencheur_auto.html", "declencheur_auto.html")
        ]

        # Boutons pour ouvrir les fichiers
        for label, path in html_files:
            tk.Button(self.parent, text=label, command=lambda p=path: self.open_specific_html(p)).pack(pady=5)

    def open_specific_html(self, filename):
        authorized_path = os.path.abspath(filename)
        if os.path.exists(authorized_path) and authorized_path.endswith(".html"):
            webbrowser.open_new_tab(f"file://{authorized_path}")
            self.path_label.config(text=f"Ouverture de : {authorized_path}")
        else:
            messagebox.showwarning("Fichier non trouvé", f"Le fichier {filename} est introuvable ou n'est pas un fichier HTML.")

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLViewer(root)
    root.mainloop()
