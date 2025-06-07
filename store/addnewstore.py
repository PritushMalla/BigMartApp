import sqlite3
from tkinter import ttk

import customtkinter as ctk
import tkinter as tk
from input import inputclass
from tkinter import messagebox
from Listtables import DataTable
class AddStore(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent, data_table_instance=None, initial_data=None):

        super().__init__(parent)
        self.data_table_instance = data_table_instance
        self.initial_data = initial_data
        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                            fg_color='#EAF0F1',bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header_text = "Add Store" if self.initial_data is None else "Update Store"
        header = ctk.CTkLabel(card, text=header_text, font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=1, column=0, columnspan=2, pady=(25, 10))

        # Input fields
        self.name_entry = inputclass.create_input(card,"Name","Store Name",2,0)
        self.manager_entry = inputclass.create_input(card, "Manager", "Manager Name", 4, 0)
        self.number_entry = inputclass.create_number_input(card,"Store Phone Number","Enter Phone Number",6,0)
        self.location_entry = inputclass.create_input(card,"Store Location","Enter Location ",8,0)
        self.status_options = ["Open","Close"]
        self.status_var = ctk.StringVar()
        self.status_entry = inputclass.create_dropdown(card,"Status",self.status_options,10,0,self.status_var)

        # Populate form if initial data is provided
        if self.initial_data:
            self.populate_form()

        self._create_store_table() # Ensure table exists

        # Submit button
        submit_button_text = "Add Store" if self.initial_data is None else "Update Store"
        submit_button = ctk.CTkButton(card, text=submit_button_text, command=self.submit_store, width=200, height=40)
        submit_button.grid(row=12, column=0, columnspan=2, pady=(30, 25))

    def _create_store_table(self):
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        cursor.execute('''
         CREATE TABLE IF NOT EXISTS store (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             StoreName TEXT,
             Manager TEXT,
             PhoneNo TEXT,
             Location TEXT,
             Status TEXT
         )''')
        conn.commit()
        conn.close()

    def populate_form(self):
        if self.initial_data:
            try:
                self.name_entry.insert(0, self.initial_data[1] or "")
                self.manager_entry.insert(0, self.initial_data[2] or "")
                self.number_entry.insert(0, self.initial_data[3] or "")
                self.location_entry.insert(0, self.initial_data[4] or "")
                # Assuming the dropdown's value can be set directly
                self.status_entry.set(self.initial_data[5] or self.status_options[0]) # Set to first option if empty
            except IndexError:
                print("Warning: initial_data doesn't have enough elements.")

    def validate_inputs(self):
        name = self.name_entry.get().strip()
        manager = self.manager_entry.get().strip()
        phone = self.number_entry.get().strip()
        location = self.location_entry.get().strip()
        status = self.status_entry.get().strip()

        if not name:
            messagebox.showerror("Validation Error", "Store Name cannot be empty.")
            return False
        if not manager:
            messagebox.showerror("Validation Error", "Manager Name cannot be empty.")
            return False
        if not phone:
            messagebox.showerror("Validation Error", "Phone Number cannot be empty.")
            return False
        if not phone.isdigit():
            messagebox.showerror("Validation Error", "Phone Number must contain only digits.")
            return False
        if len(phone) < 7 or len(phone) > 15:
            messagebox.showerror("Validation Error", "Phone Number length must be between 7 and 15 digits.")
            return False
        if not location:
            messagebox.showerror("Validation Error", "Store Location cannot be empty.")
            return False
        if status not in self.status_options:
            messagebox.showerror("Validation Error", "Please select a valid Store Status.")
            return False
        return True

    def submit_store(self):
        if not self.validate_inputs():
            return

        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        data = (
            self.name_entry.get(),
            self.manager_entry.get(),
            self.number_entry.get(),
            self.location_entry.get(),
            self.status_entry.get()
        )

        if self.initial_data:  # It's an update
            store_id = self.initial_data[0]
            cursor.execute('''
                UPDATE store SET
                    StoreName=?, Manager=?, PhoneNo=?, Location=?, Status=?
                WHERE id=?
            ''', (*data, store_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Store with ID {store_id} updated successfully.")

            self.data_table_instance.refresh_table()
            self.master.destroy()

            # Close the update form
        else:  # It's a new store
            cursor.execute('''
                INSERT INTO store (
                    StoreName, Manager, PhoneNo, Location, Status
                ) VALUES (?, ?, ?, ?, ?)
            ''', data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Store added successfully.")
            # if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
            self.data_table_instance.refresh_table()
            # Clear input fields
            self.name_entry.delete(0, 'end')
            self.manager_entry.delete(0, "end")
            self.number_entry.delete(0, "end")
            self.location_entry.delete(0, 'end')
            # You might want to reset the dropdown to its default value