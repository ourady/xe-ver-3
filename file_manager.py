import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def rename_and_move_files(app):
    app.selected_files = filedialog.askopenfilenames(title="Sélectionner des fichiers", filetypes=[("Tous les fichiers", "*.*")])
    if len(app.selected_files) > 100:
        messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 100 fichiers au maximum.")
        app.selected_files = []
    else:
        target_dir = filedialog.askdirectory(title="Sélectionner le répertoire de destination")
        if not target_dir:
            messagebox.showerror("Erreur", "Aucun répertoire de destination sélectionné.")
            return

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        app.progress['value'] = 0
        app.progress['maximum'] = len(app.selected_files)

        for i, file_path in enumerate(app.selected_files):
            file_name = os.path.basename(file_path)
            new_file_name = f"{os.path.splitext(file_name)[0]}.zip"
            new_file_path = os.path.join(target_dir, new_file_name)
            shutil.copy(file_path, new_file_path)
            app.progress['value'] = i + 1
            app.update_idletasks()

        messagebox.showinfo("Succès", "Les fichiers ont été renommés et déplacés avec succès.")
        app.selected_files = []

def unzip_file(app):
    zip_file = filedialog.askopenfilename(title="Sélectionner un fichier zip", filetypes=[("Zip files", "*.zip")])
    if zip_file:
        target_dir = filedialog.askdirectory(title="Sélectionner le répertoire de destination")
        if not target_dir:
            messagebox.showerror("Erreur", "Aucun répertoire de destination sélectionné.")
            return

        shutil.unpack_archive(zip_file, target_dir)
        messagebox.showinfo("Succès", "Le fichier zip a été décompressé avec succès.")

