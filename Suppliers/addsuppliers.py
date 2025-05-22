import sqlite3
from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
from input import inputclass
from tkinter import messagebox

class AddSuppliers(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent, data_table_instance=None, initial_data=None):
        super().__init__(parent)
        self.data_table_instance = data_table_instance
        self.initial_data = initial_data

        # Centered supplier card container
        supplier_card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                                    fg_color='#EAF0F1', bg_color="white")
        supplier_card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header_text = "Add Supplier" if self.initial_data is None else "Update Supplier"
        header = ctk.CTkLabel(supplier_card, text=header_text, font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=1, column=0, columnspan=2, pady=(25, 10))

        # Input fields
        self.suppliername_entry = inputclass.create_input(supplier_card, "Supplier Name", "Enter the Supplier's Name", 2, 0)
        self.productname_entry = inputclass.create_input(supplier_card, "Product Name", "Enter the Product Name", 4, 0)
        self.supplieremail_entry = inputclass.create_email_input(supplier_card, "Email", "Enter the Supplier's Email", 6, 0)
        self.supplierphone_entry = inputclass.create_number_input(supplier_card, "Phone Number", "Enter the Supplier's Phone Number", 8, 0)
        self.supplieraddress_entry = inputclass.create_input(supplier_card, "Address", "Enter the Address of the Supplier", 10, 0)

        self._create_suppliers_table()  # Ensure table exists

        # Submit button
        submit_button_text = "Add Supplier" if self.initial_data is None else "Update Supplier"
        submit_button = ctk.CTkButton(supplier_card, text=submit_button_text, command=self.submit_suppliers, width=200, height=40)
        submit_button.grid(row=13, column=0, columnspan=2, pady=(30, 25))

        if self.initial_data:
            self.populate_form()

    def _create_suppliers_table(self):
        conn = sqlite3.connect('supplier.db')
        cursor = conn.cursor()
        cursor.execute('''
             CREATE TABLE IF NOT EXISTS suppliers (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             Supplier_name TEXT,
             Product_name TEXT,
             Supplier_mail TEXT,
             Supplier_phone TEXT,
             Supplier_address TEXT)''')
        conn.commit()
        conn.close()

    def populate_form(self):
        if self.initial_data:
            try:
                self.suppliername_entry.insert(0, self.initial_data[1] or "")
                self.productname_entry.insert(0, self.initial_data[2] or "")
                self.supplieremail_entry.insert(0, self.initial_data[3] or "")
                self.supplierphone_entry.insert(0, self.initial_data[4] or "")
                self.supplieraddress_entry.insert(0, self.initial_data[5] or "")
            except IndexError:
                print("Warning: initial_data doesn't have enough elements.")

    def submit_suppliers(self):
        conn = sqlite3.connect('supplier.db')
        cursor = conn.cursor()
        data = (
            self.suppliername_entry.get(),
            self.productname_entry.get(),
            self.supplieremail_entry.get(),
            self.supplierphone_entry.get(),
            self.supplieraddress_entry.get()
        )

        if self.initial_data:  # It's an update
            supplier_id = self.initial_data[0]
            cursor.execute('''
                    UPDATE suppliers SET
                    Supplier_name=?, Product_name=?, Supplier_mail=?, Supplier_phone=?, Supplier_address=?
                    WHERE id=?
                    ''', (*data, supplier_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Supplier updated successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()
            self.master.destroy() # Close the form
        else:
            cursor.execute('''
                    INSERT INTO suppliers (Supplier_name,Product_name,Supplier_mail,Supplier_phone,Supplier_address)
                    VALUES (?, ?, ?, ?, ?)
                    ''', data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Supplier added successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()

            # Clear input fields after successful addition.
            self.suppliername_entry.delete(0, 'end')
            self.productname_entry.delete(0, 'end')
            self.supplieremail_entry.delete(0, 'end')
            self.supplierphone_entry.delete(0, 'end')
            self.supplieraddress_entry.delete(0, 'end')


