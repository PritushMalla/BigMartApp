import customtkinter as ctk
from tkinter import Toplevel

class ViewCustomers:
    @staticmethod
    def open_view_customers_window():
        win = Toplevel()
        win.title("All Customers")
        win.geometry("400x300")

        ctk.CTkLabel(win, text="Customer List", font=("Helvetica", 14)).pack(pady=10)

        # Simulate customer data (replace with DB later)
        customers = [
            {"Name": "Alice", "Email": "alice@email.com", "Phone": "1234567890", "Balance": "5000"},
            {"Name": "Bob", "Email": "bob@email.com", "Phone": "0987654321", "Balance": "3000"},
        ]

        for customer in customers:
            info = f"{customer['Name']} | {customer['Email']} | {customer['Phone']} | ₹{customer['Balance']}"
            ctk.CTkLabel(win, text=info, anchor="w").pack(padx=10, pady=2, fill="x")
