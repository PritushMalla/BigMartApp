

import customtkinter as ctk

import re
from tkinter import messagebox

class inputclass:
    @staticmethod
    def create_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=0.5)
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=30)
        entry.grid(row=row+1, column=column, columnspan=colspan, padx=20, pady=(5, 10))
        return entry

    def create_number_input(parent, label_text, placeholder, row, column):
        def validate_number(P):
            return P.isdigit() or P == ""

        vcmd = parent.register(validate_number)

        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
        entry.configure(validate="key", validatecommand=(vcmd, "%P"))
        entry.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return entry

    def create_dropdown(parent, label_text, options, row, column):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        dropdown = ctk.CTkOptionMenu(parent, values=options, width=250, height=35)
        dropdown.grid(row=row + 1, column=column, padx=20, pady=(0, 10))

        return dropdown

    @staticmethod
    def create_email_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
        entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))

        def validate_email(event=None):
            email = entry.get()
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.")

        # Run validation when user leaves the email field
        entry.bind("<FocusOut>", validate_email)

        return entry

    @staticmethod
    def create_password_input(parent, label_text, placeholder, row, column, colspan=1):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
        label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, show="*", width=250, height=35)
        entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))

        # Show/hide button
        def toggle_password():
            if entry.cget("show") == "*":
                entry.configure(show="")  # Show text
                toggle_btn.configure(text="Hide")
            else:
                entry.configure(show="*")  # Hide text
                toggle_btn.configure(text="Show")

        toggle_btn = ctk.CTkButton(parent, text="Show", width=60, height=30, command=toggle_password)
        toggle_btn.grid(row=row+1,column=1,sticky='w',padx=30, pady=(0, 10))  # Adjust as needed

        return entry