import os
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import webbrowser
import json
import threading
from flask import Flask, request, jsonify

class QuizApp(tk.Frame):
    def __init__(self, parent, quiz_folder="fichierquizz"):
        super().__init__(parent)
        self.pack(fill='both', expand=True)
        self.quiz_folder = quiz_folder

        # Onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Onglet Quiz
        self.quiz_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.quiz_frame, text='Quiz')
        self.lancer_quiz_button = tk.Button(self.quiz_frame, text="Charger les quiz", command=self.lancer_quiz)
        self.lancer_quiz_button.pack(pady=10)

        # Onglet Administration
        self.admin_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.admin_frame, text='Administration')
        self.admin_label = tk.Label(self.admin_frame, text="Espace Administration", bg='white')
        self.admin_label.pack(pady=10)

        # Onglet HTML Locaux
        self.local_html_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.local_html_frame, text='HTML Locaux')
        self.select_folder_button = tk.Button(self.local_html_frame, text="Choisir un dossier", command=self.choisir_dossier)
        self.select_folder_button.pack(pady=10)
        self.html_buttons_frame = tk.Frame(self.local_html_frame, bg='white')
        self.html_buttons_frame.pack(fill='both', expand=True)

        # Onglet Résultats
        self.results_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.results_frame, text='Résultats')
        self.results_label = tk.Label(self.results_frame, text="Résultats des Quiz", bg='white')
        self.results_label.pack(pady=10)
        self.results_table = ttk.Treeview(self.results_frame, columns=("Quiz", "Utilisateur", "Score"), show='headings')
        self.results_table.heading("Quiz", text="Quiz")
        self.results_table.heading("Utilisateur", text="Utilisateur")
        self.results_table.heading("Score", text="Score")
        self.results_table.pack(expand=True, fill='both')
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
        for row in self.results_table.get_children():
            self.results_table.delete(row)

        results_file = "quiz_results.json"
        if os.path.exists(results_file):
            with open(results_file, 'r') as file:
                results = json.load(file)
                for result in results:
                    self.results_table.insert("", "end", values=(result["quiz_name"], result["user"], result["score"]))

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
            # Envoi du score fictif au serveur Flask
            self.envoyer_score(filename, "user1", 100)

    def envoyer_score(self, quiz_name, user, score):
        import requests
        try:
            response = requests.post('http://127.0.0.1:5000/submit_score', json={
                'quiz_name': quiz_name,
                'user': user,
                'score': score
            })
            if response.status_code == 200:
                print(f"Score envoyé avec succès pour {quiz_name}")
            else:
                print(f"Erreur lors de l'envoi du score pour {quiz_name}: {response.text}")
        except Exception as e:
            print(f"Erreur de connexion au serveur Flask: {e}")

# Serveur Flask en arrière-plan
app_flask = Flask(__name__)

@app_flask.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    quiz_name = data.get('quiz_name')
    user = data.get('user')
    score = data.get('score')

    if not quiz_name or not user or score is None:
        return jsonify({"error": "Invalid data"}), 400

    result = {"quiz_name": quiz_name, "user": user, "score": score}
    results_file = "quiz_results.json"

    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)
    else:
        results = []

    results.append(result)

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

    return jsonify({"message": "Score submitted successfully"}), 200

def lancer_serveur_flask():
    app_flask.run(debug=False, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=lancer_serveur_flask, daemon=True).start()
    root = tk.Tk()
    root.title("Gestionnaire de Quiz")
    app = QuizApp(root)
    root.mainloop()

