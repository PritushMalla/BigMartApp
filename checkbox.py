import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter as ctk

import Listtables
from input import inputclass
from tkinter import messagebox

class CheckboxTreeviewHelper:
    def __init__(self, treeview):
        self.treeview = treeview
        self.checked_items = set()
        self.treeview.bind("<Button-1>", self.toggle_checkbox)

        self.treeview.heading("Select", text="Select")
        self.treeview.column("Select", width=50, anchor=tk.CENTER)

    def insert_with_checkbox(self, parent, index, values=None):
        if values is None:
            values = []
        item_id = self.treeview.insert(parent, index, values=("⬜",) + tuple(values))
        return item_id

    def toggle_checkbox(self, event):
        region = self.treeview.identify("region", event.x, event.y)
        column = self.treeview.identify_column(event.x)
        if region == "cell" and column == "#1":  # "#1" is the "Select" column
            item = self.treeview.identify_row(event.y)
            if item:
                current_val = self.treeview.set(item, "Select")
                new_val = "☑️" if current_val == "⬜" else "⬜"
                self.treeview.set(item, "Select", new_val)

                if new_val == "☑️":
                    self.checked_items.add(item)
                else:
                    self.checked_items.discard(item)

    def get_checked_items(self):
        return list(self.checked_items)

    def clear_checkboxes(self):
        for item in self.treeview.get_children():
            self.treeview.set(item, "Select", "⬜")
        self.checked_items.clear()
