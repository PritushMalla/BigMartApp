import sqlite3
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmessagebox

import Listtables
from input import inputclass


class ProductForm(ctk.CTkFrame):
    ctk.set_appearance_mode("light")

    def __init__(self, parent, data_table_instance=None, initial_data=None):  # Receive DataTable instance and initial data
        super().__init__(parent)
        self.data_table_instance = data_table_instance
        self.initial_data = initial_data  # Data of the product being updated

        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2, fg_color='#EAF0F1', bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header_text = "Add Product" if self.initial_data is None else "Update Product"
        header = ctk.CTkLabel(card, text=header_text, font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(25, 10))

        # Reusable input method
        def create_input(parent, label_text, placeholder, row, column, colspan=1):
            label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 14), text_color="black")
            label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))
            entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
            entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))
            return entry

        def datepicking(datename, rowlabelno, collabelno, rowno, colno):
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Custom.DateEntry', fieldbackground='white', background='white', foreground='black',
                            bordercolor='black', lightcolor='white', darkcolor='white', arrowcolor='black')
            date_label = ctk.CTkLabel(card, text=datename, font=("Arial", 14))
            date_label.grid(row=rowlabelno, column=collabelno, sticky="w", padx=20, pady=(10, 2))
            tk_container = ctk.CTkFrame(master=card, fg_color="white")
            tk_container.grid(row=rowno, column=colno, sticky="w", padx=20, pady=(10, 2))
            datepicker = DateEntry(master=tk_container, background='white', foreground='black', borderwidth=1,
                                   date_pattern='yyyy-mm-dd', style='Custom.DateEntry')
            datepicker.pack()
            return datepicker
        suppliername=Listtables.suppliername()
        categoryname=Listtables.productcategory()

        finalsuppliernames = [item[0] for item in suppliername]
        print(finalsuppliernames)
        finalcategorynames=[item[0] for item in categoryname]
        print(finalcategorynames)

        # Input fields

        self.Batch_entry = create_input(card, "Product Batch", "Enter product name", 1, 0)
        self.name_entry = create_input(card, "Product Name", "Enter category", 1, 1)
        self.desc_label = ctk.CTkLabel(card, text="Product Description", font=("Arial", 14), text_color="black")
        self.desc_label.grid(row=3, column=0, columnspan=1, sticky="w", padx=20, pady=(0, 10))
        self.desc_textbox = ctk.CTkTextbox(card, width=250, height=100, corner_radius=10)
        self.desc_textbox.grid(row=4, column=0, columnspan=1, padx=20, pady=(0, 10))
        self.supplier = inputclass.create_dropdown(card, "Supplier", finalsuppliernames, 7, 1)
        self.category = inputclass.create_dropdown(card, "Category", finalcategorynames, 3, 1)

        self.cost_price = create_input(card, "Cost Price", "Enter cost", 5, 0)
        self.sale_price = create_input(card, "Sales Price", "Enter price", 5, 1)
        self.quantity_entry = inputclass.create_number_input(card, "Quantity", "Enter quantity", 7, 0)
        self.mfg_date = datepicking("Manufacturing date", 9, 0, 10, 0)
        self.exp_date = datepicking("Expiry date", 9, 1, 10, 1)

        # Populate form if initial data is provided
        if self.initial_data:
            self.populate_form()

        # Submit button
        submit_button_text = "Add Product" if self.initial_data is None else "Update Product"
        submit_button = ctk.CTkButton(card, text=submit_button_text, command=self.submit_data, width=200, height=40)
        submit_button.grid(row=13, column=0, columnspan=2, pady=(30, 25))

        self._create_product_table() # Ensure table exists

    def _create_product_table(self):
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch TEXT,
            name TEXT,
            description TEXT,
            cost_price REAL,
            sales_price REAL,
            quantity INTEGER,
            supplier TEXT,
            mfg_date TEXT,
            exp_date TEXT,
            category TEXT,
            Status TEXT
            
        )
        ''')
        conn.commit()
        conn.close()

    def populate_form(self):
        if self.initial_data:
            # Assuming the order of columns in your 'products' table is:
            # id, batch, name, description, cost_price, sales_price, quantity, supplier, mfg_date, exp_date

            # Use try-except blocks to handle potential index errors gracefully
            try:
                self.Batch_entry.insert(0, self.initial_data[1] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 1 (batch)")

            try:
                self.name_entry.insert(0, self.initial_data[2] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 2 (name)")

            try:
                self.desc_textbox.insert("1.0", self.initial_data[3] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 3 (description)")

            try:
                self.cost_price.insert(0, self.initial_data[4] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 4 (cost_price)")

            try:
                self.sale_price.insert(0, self.initial_data[5] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 5 (sales_price)")

            try:
                self.quantity_entry.insert(0, self.initial_data[6] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 6 (quantity)")

            # try:
            #     self.supplier.insert(0, self.initial_data[7] or "")
            # except IndexError:
            #     print("Warning: initial_data doesn't have index 7 (supplier)")

            try:
                self.mfg_date.set_date(self.initial_data[8] or "")
            except AttributeError:
                print("Warning: DateEntry widget might not have 'set_date' method.")
            except IndexError:
                print("Warning: initial_data doesn't have index 8 (mfg_date)")

            try:
                self.exp_date.set_date(self.initial_data[9] or "")

            except AttributeError:
                print("Warning: DateEntry widget might not have 'set_date' method.")
            except IndexError:
                print("Warning: initial_data doesn't have index 9 (exp_date)")
            # try:
            #     self.category.set_date(self.initial_data[10] or "")
            # except IndexError:
            #     print("Warning: initial_data doesn't have index 10 (exp_date)")
            try:
                self.quantity_entry.insert(0, self.initial_data[10] or "")
            except IndexError:
                print("Warning: initial_data doesn't have index 10 (status)")
        else:
            print("Warning: populate_form called with no initial data.")
    def submit_data(self):
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        quantity=int(self.quantity_entry.get())
        status = "Out of Stock" if  quantity< 1 else "In Stock"
        data = (
            self.Batch_entry.get(), self.name_entry.get(), self.desc_textbox.get("1.0", "end"),
            self.cost_price.get(), self.sale_price.get(), self.quantity_entry.get(),
            self.supplier.get(), self.mfg_date.get(), self.exp_date.get(),self.category.get(),status
        )

        if self.initial_data:  # It's an update
            product_id = self.initial_data[0]
            cursor.execute('''
                UPDATE product SET
                    batch=?, name=?, description=?, cost_price=?, sales_price=?,
                    quantity=?, supplier=?, mfg_date=?, exp_date=?,category=?,Status=?
                WHERE id=?
            ''', (*data, product_id))
            conn.commit()
            conn.close()
            tkmessagebox.showinfo("Success", f"Product with ID {product_id} updated successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()
            self.master.destroy() # Close the update form
        else:  # It's a new product
            cursor.execute('''
                INSERT INTO product (
                    batch, name, description, cost_price, sales_price, quantity, supplier, mfg_date, exp_date,category,Status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
            ''', data)
            conn.commit()
            conn.close()
            tkmessagebox.showinfo("Success", "Product added successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()
            # Clear input fields
            self.Batch_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
            self.desc_textbox.delete("1.0", "end")
            self.cost_price.delete(0, 'end')
            self.sale_price.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')

            # Note: Clearing date pickers might require a different method

