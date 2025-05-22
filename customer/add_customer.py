import customtkinter as ctk
class AddCustomer:
    @staticmethod
    def open_add_customer_window():

        win = ctk.CTkToplevel()
        win.title("Add Customer")
        win.geometry("350x350")

        ctk.CTkLabel(win, text="Add New Customer", font=("Helvetica", 14)).grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Form Labels and Entries
        ctk.CTkLabel(win, text="Full Name").grid(row=1, column=0, padx=10, pady=5)
        name_entry = ctk.CTkEntry(win, width=100)
        name_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(win, text="Email").grid(row=2, column=0, padx=10, pady=5)
        email_entry = ctk.CTkEntry(win, width=100)
        email_entry.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(win, text="Phone Number").grid(row=3, column=0, padx=10, pady=5)
        phone_entry = ctk.CTkEntry(win, width=100)
        phone_entry.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        ctk.CTkLabel(win, text="Initial Deposit").grid(row=4, column=0, padx=10, pady=5)
        deposit_entry = ctk.CTkEntry(win, width=100)
        deposit_entry.grid(row=4, column=1, sticky="e", padx=10, pady=5)

        def submit_customer():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            deposit = deposit_entry.get()

            # Print data (can be stored in DB later)
            print(f"Name: {name}, Email: {email}, Phone: {phone}, Deposit: {deposit}")
            ctk.CTkLabel(win, text="Customer Added!", text_color="green").grid(row=5, column=1, sticky="e", padx=10, pady=5)

        ctk.CTkButton(win, text="Submit", command=submit_customer).grid(row=6, column=1, sticky="e", padx=10, pady=5)
