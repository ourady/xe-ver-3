
import tkinter as tk
from tkinter import filedialog, messagebox

def save_quiz(app):
    quiz_content = app.quiz_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(quiz_content)
        messagebox.showinfo("Succès", "Le quiz a été enregistré avec succès.")

def clear_quiz(app):
    app.quiz_text.delete("1.0", tk.END)

def select_json_file(app):
    json_file = filedialog.askopenfilename(title="Sélectionner un fichier JSON", filetypes=[("JSON files", "*.json")])
    if json_file:
        if app.quiz_text.get("1.0", tk.END).strip():
            if not messagebox.askyesno("Confirmation", "La zone de quiz contient du texte. Voulez-vous sauvegarder avant de charger le fichier JSON ?"):
                return
            save_quiz(app)
        with open(json_file, 'r') as file:
            json_content = file.read()
            app.quiz_text.delete("1.0", tk.END)
            app.quiz_text.insert(tk.END, json_content)
        messagebox.showinfo("Fichier sélectionné", f"Fichier JSON sélectionné : {json_file}")

def open_json_editor(app):
    if app.quiz_text.get("1.0", tk.END).strip():
        if not messagebox.askyesno("Confirmation", "La zone de quiz contient du texte. Voulez-vous sauvegarder avant d'ouvrir l'éditeur JSON ?"):
            return
        save_quiz(app)
    app.quiz_text.delete("1.0", tk.END)
    json_file = filedialog.askopenfilename(title="Sélectionner un fichier JSON", filetypes=[("JSON files", "*.json")])
    if json_file:
        with open(json_file, 'r') as file:
            json_content = file.read()
            app.quiz_text.insert(tk.END, json_content)
        messagebox.showinfo("Fichier sélectionné", f"Fichier JSON sélectionné : {json_file}")
