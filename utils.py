import os
import fnmatch
import tkinter as tk
from tkinter import filedialog
import webbrowser

def search_files(app):
    search_term = app.search_file_var.get().lower()
    results = []
    for root, dirs, files in os.walk(app.disk_var.get()):
        for file in files:
            if fnmatch.fnmatch(file.lower(), f"*{search_term}*"):
                results.append(os.path.join(root, file))
    app.quiz_text.delete("1.0", tk.END)
    if results:
        app.quiz_text.insert(tk.END, "\n".join(results))
    else:
        app.quiz_text.insert(tk.END, "Aucun fichier trouvé.")

def search_text(app):
    search_term = app.search_text_var.get().lower()
    content = app.quiz_text.get("1.0", tk.END).lower()
    start = 1.0
    while True:
        start = app.quiz_text.search(search_term, start, stopindex=tk.END)
        if not start:
            break
        end = f"{start}+{len(search_term)}c"
        app.quiz_text.tag_add("highlight", start, end)
        app.quiz_text.tag_config("highlight", background="yellow")
        start = end

def open_html_in_browser():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers HTML", "*.html")])
    if file_path:
        webbrowser.open_new_tab(f"file://{file_path}")
