import sqlite3
import customtkinter as ctk
from tkcalendar import DateEntry

from tkinter import ttk, messagebox

from input import inputclass


class Addproductcategory(ctk.CTkFrame):
    ctk.set_appearance_mode("light")

    def __init__(self, parent, data_table_instance=None, initial_data=None):  # Receive DataTable instance and initial data
        super().__init__(parent)
        self.data_table_instance = data_table_instance
        self.initial_data = initial_data  # Data of the product being updated

        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2, fg_color='#EAF0F1', bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header_text = "Add Product Category" if self.initial_data is None else "Update Product Category"
        header = ctk.CTkLabel(card, text=header_text, font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(25, 10))

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
            datepicker.delete(0, 'end')

            return datepicker





        self.productcatname=inputclass.create_input(card,"Product Category","Enter Product Category",1,0)
        self.Date=datepicking("Added Date",3,0,4,0)
        self.Status=inputclass.create_dropdown(card,"Status",["Active","Disabled"],6,0)
        self._create_productcat_table()
        submit_button_text = "Add Product Category" if self.initial_data is None else "Update Product Category"
        submit_button = ctk.CTkButton(card, text=submit_button_text, command=self.submit_prodcategory, width=200, height=40)
        submit_button.grid(row=8, column=0, columnspan=2, pady=(30, 25))
        if self.initial_data:
            self.populate_form()


    def _create_productcat_table(self):
        conn = sqlite3.connect('productcategory.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productcat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name,
            added_date,
            status)
        ''')
        conn.commit()
        conn.close()

    def populate_form(self):
        if self.initial_data:
            try:
                self.productcatname.insert(0, self.initial_data[1] or " ")
                self.Date.insert(0, self.initial_data[2] or " ")

            except IndexError:
                print("Warning: initial_data doesn't have enough elements.")
    def submit_prodcategory(self):
        conn = sqlite3.connect('productcategory.db')
        cursor = conn.cursor()
        data = (
            self.productcatname.get(),
            self.Date.get(),
            self.Status.get()


        )
        if self.initial_data:
            productcat_id = self.initial_data[0]
            cursor.execute('''
                 UPDATE productcat SET
                 product_name=? ,
                 added_date=? ,
                 status=?
                     WHERE id=?''',(*data,productcat_id)
                           )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product Category has been  updated successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()
            self.master.destroy()
        else:
            cursor.execute('''
                    INSERT INTO productcat(product_name,added_date,status)
                    VALUES (?, ?, ?)
                    ''', data)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product Cateogry added successfully.")
            if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
                self.data_table_instance.refresh_table()
            self.productcatname.delete(0,'end')
            self.Date.delete(0,'end')

















