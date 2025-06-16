
import os
import string
import tkinter as tk
from tkinter import ttk

class FileExplorer:
    def __init__(self, parent, on_file_select):
        self.parent = parent
        self.on_file_select = on_file_select

        self.disk_var = tk.StringVar()
        self.disk_menu = ttk.Combobox(self.parent, textvariable=self.disk_var, state='readonly')
        self.disk_menu.pack(pady=10)
        self.disk_menu.bind('<<ComboboxSelected>>', self.on_disk_selected)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.parent, textvariable=self.search_var)
        self.search_entry.pack(pady=10)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        self.file_tree_scrollbar = tk.Scrollbar(self.parent)
        self.file_tree_scrollbar.pack(side='right', fill='y')

        self.file_tree = ttk.Treeview(self.parent, yscrollcommand=self.file_tree_scrollbar.set)
        self.file_tree.pack(pady=10, fill='both', expand=True)
        self.file_tree.bind('<<TreeviewOpen>>', self.on_treeview_open)
        self.file_tree.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.file_tree_scrollbar.config(command=self.file_tree.yview)

        self.populate_disk_menu()

    def populate_disk_menu(self):
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

        self.disk_menu['values'] = drives
        if drives:
            self.disk_menu.current(0)
            self.load_directory(drives[0])

    def on_disk_selected(self, event):
        selected_disk = self.disk_var.get()
        self.load_directory(selected_disk)

    def load_directory(self, path):
        self.file_tree.delete(*self.file_tree.get_children())
        self.insert_node('', path)

    def insert_node(self, parent, path):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                node = self.file_tree.insert(parent, 'end', text=item, values=[item_path])
                if os.path.isdir(item_path):
                    self.file_tree.insert(node, 'end', text='dummy')
        except PermissionError:
            pass

    def on_treeview_open(self, event):
        node = self.file_tree.focus()
        children = self.file_tree.get_children(node)
        if children and self.file_tree.item(children[0], 'text') == 'dummy':
            self.file_tree.delete(children[0])
            path = self.file_tree.item(node, 'values')[0]
            self.insert_node(node, path)

    def on_treeview_select(self, event):
        node = self.file_tree.focus()
        path = self.file_tree.item(node, 'values')[0]
        if os.path.isfile(path):
            self.on_file_select(path)

    def on_search(self, event):
        search_term = self.search_var.get().lower()
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.insert_node('', self.disk_var.get())
        if search_term:
            for item in self.file_tree.get_children():
                if search_term not in self.file_tree.item(item, 'text').lower():
                    self.file_tree.detach(item)
