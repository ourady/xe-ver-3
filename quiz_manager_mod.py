import os
import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser
import json
import requests
import subprocess

class QuizApp(tk.Frame):
    def __init__(self, parent, quiz_folder="fichierquizz"):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.quiz_folder = quiz_folder

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.quiz_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.quiz_frame, text='Quiz')

        self.lancer_quiz_button = tk.Button(self.quiz_frame, text="Charger les quiz", command=self.lancer_quiz)
        self.lancer_quiz_button.pack(pady=10)

        self.lancer_serveur_button = tk.Button(self.quiz_frame, text="Lancer le serveur Flask", command=self.lancer_serveur_flask)
        self.lancer_serveur_button.pack(pady=10)

        # Champs de saisie pour le nom du quiz, l'utilisateur et le score
        self.quiz_name_var = tk.StringVar()
        self.user_name_var = tk.StringVar()
        self.score_var = tk.StringVar()

        tk.Label(self.quiz_frame, text="Nom du quiz:").pack(pady=5)
        self.quiz_name_entry = tk.Entry(self.quiz_frame, textvariable=self.quiz_name_var)
        self.quiz_name_entry.pack(pady=5)

        tk.Label(self.quiz_frame, text="Nom de l'utilisateur:").pack(pady=5)
        self.user_name_entry = tk.Entry(self.quiz_frame, textvariable=self.user_name_var)
        self.user_name_entry.pack(pady=5)

        tk.Label(self.quiz_frame, text="Score:").pack(pady=5)
        self.score_entry = tk.Entry(self.quiz_frame, textvariable=self.score_var)
        self.score_entry.pack(pady=5)

        self.envoyer_score_button = tk.Button(self.quiz_frame, text="Envoyer le score", command=self.envoyer_score)
        self.envoyer_score_button.pack(pady=10)

        self.admin_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.admin_frame, text='Administration')
        self.admin_label = tk.Label(self.admin_frame, text="Espace Administration", bg='white')
        self.admin_label.pack(pady=10)

        self.local_html_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.local_html_frame, text='HTML Locaux')
        self.select_folder_button = tk.Button(self.local_html_frame, text="Choisir un dossier", command=self.choisir_dossier)
        self.select_folder_button.pack(pady=10)
        self.html_buttons_frame = tk.Frame(self.local_html_frame, bg='white')
        self.html_buttons_frame.pack(fill='both', expand=True)

        self.results_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.results_frame, text='Résultats')
        self.results_label = tk.Label(self.results_frame, text="Résultats des Quiz", bg='white')
        self.results_label.pack(pady=10)

        # Ajout de la barre de défilement
        self.results_scrollbar = tk.Scrollbar(self.results_frame)
        self.results_scrollbar.pack(side='right', fill='y')

        self.results_table = ttk.Treeview(self.results_frame, columns=("Quiz", "Utilisateur", "Score"), show='headings', yscrollcommand=self.results_scrollbar.set)
        self.results_table.heading("Quiz", text="Quiz")
        self.results_table.heading("Utilisateur", text="Utilisateur")
        self.results_table.heading("Score", text="Score")
        self.results_table.pack(expand=True, fill='both')

        self.results_scrollbar.config(command=self.results_table.yview)

        self.refresh_button = tk.Button(self.results_frame, text="Rafraîchir", command=self.load_results)
        self.refresh_button.pack(pady=5)

        self.load_results()

    def lancer_quiz(self):
        self.quiz_app = QuizLoader(self.quiz_frame, self.quiz_folder)

    def choisir_dossier(self):
        dossier = filedialog.askdirectory()
        if dossier:
            for widget in self.html_buttons_frame.winfo_children():
                widget.destroy()
            for filename in os.listdir(dossier):
                if filename.endswith(".html"):
                    full_path = os.path.abspath(os.path.join(dossier, filename))
                    bouton = tk.Button(self.html_buttons_frame, text=f"Ouvrir {filename}",
                                       command=lambda p=full_path: webbrowser.open(f"file://{p}"))
                    bouton.pack(pady=5)

    def load_results(self):
        try:
            for row in self.results_table.get_children():
                self.results_table.delete(row)

            results_file = "quiz_results.json"
            if os.path.exists(results_file):
                with open(results_file, 'r', encoding='utf-8') as file:
                    results = json.load(file)
                    if isinstance(results, list):
                        for result in results:
                            quiz = result.get("quiz_name", "N/A")
                            user = result.get("user", "N/A")
                            score = result.get("score", "N/A")
                            self.results_table.insert("", "end", values=(quiz, user, score))
                        self.results_table.update_idletasks()  # ← force l'affichage
                    else:
                        print("Le fichier JSON ne contient pas une liste.")
            else:
                print("Fichier quiz_results.json introuvable.")
        except Exception as e:
            print(f"Erreur lors du chargement des résultats : {e}")

    def lancer_serveur_flask(self):
        try:
            subprocess.Popen(["python", "serveur_quiz.py"])
            print("Serveur Flask lancé.")
        except Exception as e:
            print(f"Erreur lors du lancement du serveur Flask : {e}")

    def envoyer_score(self):
        quiz_name = self.quiz_name_var.get()
        user_name = self.user_name_var.get()
        score = self.score_var.get()

        try:
            response = requests.post('http://127.0.0.1:5000/submit_score', json={
                'quiz_name': quiz_name,
                'user': user_name,
                'score': score
            })
            if response.status_code == 200:
                print(f"Score envoyé avec succès pour {quiz_name}")
            else:
                print(f"Erreur lors de l'envoi du score pour {quiz_name}: {response.text}")
        except Exception as e:
            print(f"Erreur de connexion au serveur Flask: {e}")

class QuizLoader:
    def __init__(self, parent_frame, quiz_folder):
        self.parent_frame = parent_frame
        self.quiz_folder = quiz_folder
        self.quiz_buttons = []
        self.load_quizzes()

    def load_quizzes(self):
        for filename in os.listdir(self.quiz_folder):
            if filename.endswith(".html"):
                button = tk.Button(self.parent_frame, text=f"Ouvrir {filename}", command=lambda f=filename: self.open_quiz(f))
                button.pack(pady=5)
                self.quiz_buttons.append(button)

    def open_quiz(self, filename):
        path = os.path.abspath(os.path.join(self.quiz_folder, filename))
        if os.path.exists(path):
            webbrowser.open(f"file://{path}")
            # self.envoyer_score(filename, "user1", 100)  # Commenté pour éviter l'envoi automatique

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Gestionnaire de Quiz")
    app = QuizApp(root)
    root.mainloop()

