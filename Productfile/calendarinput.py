# date_picker.py
import tkinter as tk
from tkcalendar import DateEntry


class DatePicker(tk.Frame):
    def __init__(self, parent, label_text="Select Date", **kwargs):
        super().__init__(parent, bg="white")

        self.label = tk.Label(self, text=label_text, bg="white", font=("Arial", 12))
        self.label.pack(anchor="w")

        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd', **kwargs)
        self.date_entry.pack(pady=(2, 5))

    def get(self):
        return self.date_entry.get()
