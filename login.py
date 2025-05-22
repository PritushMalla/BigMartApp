import customtkinter as ctk
from Dashboard import HomeDashboard

class LoginApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Banking System - Login")
        ctk.set_appearance_mode("white")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(self, text="Login to Store Admin", font=("Arial", 20))
        self.label.pack(pady=20)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        self.login_btn = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_btn.pack(pady=20)

    def login(self):
        # For now, skip login validation
        self.destroy()
        dashboard = HomeDashboard()
        dashboard.mainloop()
