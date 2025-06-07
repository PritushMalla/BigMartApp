import tkinter as tk
from tkinter import messagebox
from auth.auth_db import validate_login
from auth.register import open_register

def open_login(main_app_callback):
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username").grid(row=0, column=0)
    tk.Label(login_window, text="Password").grid(row=1, column=0)

    username_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        if validate_login(username, password):
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            login_window.destroy()
            main_app_callback(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login_window, text="Login", command=login_action).grid(row=2, column=0)
    tk.Button(login_window, text="Register", command=open_register).grid(row=2, column=1)

    login_window.mainloop()
