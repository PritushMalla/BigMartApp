from Dashboard import HomeDashboard
from auth.auth_db import init_user_db
from auth.login import open_login
import tkinter as tk

def launch_main_app(username):
    HomeDashboard()

if __name__ == "__main__":
    init_user_db()  # Ensure user table exists
    open_login(launch_main_app)