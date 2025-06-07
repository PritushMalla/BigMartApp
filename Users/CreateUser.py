
from tkinter import ttk

import customtkinter as ctk
import tkinter as tk
from input import inputclass



class CreateUser(ctk.CTkFrame):
    ctk.set_appearance_mode("light")

    def __init__(self, parent):
        super().__init__(parent)
        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                            fg_color='#EAF0F1', bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")
        # Header
        header = ctk.CTkLabel(card, text="Add User ", font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=1, column=0, columnspan=2, pady=(25, 10))

        name_entry=inputclass.create_input(card,"FullName","Enter name",2,0)
        username_entry=inputclass.create_input(card,"Username","Enter Username",4,0)
        email_entry=inputclass.create_email_input(card,"E-mail","Enter Email ",6,0),
        password_entry=inputclass.create_password_input(card,"Password","Enter Password",8,0)
        self.role_var = ctk.StringVar()
        role_entry=inputclass.create_dropdown(card,"Role",["Supplier","Admin"],10,0,self.role_var)

