import tkinter as tk
from tkinter import messagebox
from auth.auth_db import register_user

def open_register():
    reg_window = tk.Toplevel()
    reg_window.title("Register")

    tk.Label(reg_window, text="Username").grid(row=0, column=0)
    tk.Label(reg_window, text="Password").grid(row=1, column=0)

    username_entry = tk.Entry(reg_window)
    password_entry = tk.Entry(reg_window, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def register_action():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            reg_window.destroy()
        else:
            messagebox.showerror("Error", "Username already exists!")

    tk.Button(reg_window, text="Register", command=register_action).grid(row=2, columnspan=2)
