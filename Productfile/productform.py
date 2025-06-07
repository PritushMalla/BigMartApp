import sqlite3
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.messagebox as tkmessagebox

import Listtables
from input import inputclass
from datetime import datetime,timedelta


class ProductForm(ctk.CTkFrame):
    ctk.set_appearance_mode("light")

    def __init__(self, parent, data_table_instance=None, initial_data=None):

        # Receive DataTable instance and initial data
        super().__init__(parent)

        self.data_table_instance = data_table_instance
        self.initial_data = initial_data
        # Data of the product being updated




        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2, fg_color='#EAF0F1', bg_color="white")

        card.place(relx=0.5, rely=0.5,anchor="center" )

        scrollable_frame = ctk.CTkScrollableFrame(card,width=600,height=700 ,bg_color="white" ,fg_color="#EAF0F1")
        scrollable_frame.grid(row=0, column=0, padx=10, pady=10)


        # Header
        header_text = "Add Product" if self.initial_data is None else "Update Product"
        header = ctk.CTkLabel(scrollable_frame, text=header_text, font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(25, 10))

        # Reusable input method
        def create_input(parent, label_text, placeholder, row, column, colspan=1):
            label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), text_color="black")
            label.grid(row=row, column=column, sticky="w", padx=20, pady=(10, 2))
            entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=250, height=35)
            entry.grid(row=row + 1, column=column, columnspan=colspan, padx=20, pady=(0, 10))
            return entry

        def datepicking(datename, rowlabelno, collabelno, rowno, colno):
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Custom.DateEntry', fieldbackground='white', background='white', foreground='black',
                            bordercolor='black', lightcolor='white', darkcolor='white', arrowcolor='black')
            date_label = ctk.CTkLabel(scrollable_frame, text=datename, font=("Arial", 12))
            date_label.grid(row=rowlabelno, column=collabelno, sticky="w", padx=20, pady=(10, 2))
            tk_container = ctk.CTkFrame(master=scrollable_frame, fg_color="white")
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
        item_type=["Snack Foods","Dairy","Fruits and Vegetables","Baking Goods","Health and Hygiene","Breads","Seafood", "Soft Drinks","Hard Drinks","Household", "Meat", "Canned","Frozen Foods","Starchy Foods",
"Others"]
        item_fatcontent=["Low Fat", "Regular","High Fat"]
        Outlet_Identifier="OUT010"
        Outlet_Size="High"
        Outlet_Type="Supermarket Type 1 "





        # Input fields

        self.Batch_entry = create_input(scrollable_frame, "Product Batch", "Enter product name", 1, 0)
        self.name_entry = create_input(scrollable_frame, "Product Name", "Enter category", 1, 1)
        self.desc_label = ctk.CTkLabel(scrollable_frame, text="Product Description", font=("Arial", 12), text_color="black")
        self.desc_label.grid(row=3, column=0, columnspan=1, sticky="w", padx=20, pady=(0, 10))
        self.desc_textbox = ctk.CTkTextbox(scrollable_frame, width=250, height=100, corner_radius=10)
        self.desc_textbox.grid(row=4, column=0, columnspan=1, padx=20, pady=(0, 10))
        self.supplier_var = ctk.StringVar()
        self.supplier = inputclass.create_dropdown(scrollable_frame, "Supplier", finalsuppliernames, 7, 1,self.supplier_var)
        self.category_var = ctk.StringVar()
        self.category = inputclass.create_dropdown(scrollable_frame, "Product Brand ", finalcategorynames, 3, 1,self.category_var),



        self.cost_price = inputclass.create_number_input(scrollable_frame, "Cost Price", "Enter cost", 5, 0)
        self.sale_price = inputclass.create_number_input(scrollable_frame, "Sales Price", "Enter price", 5, 1)
        self.quantity_entry = inputclass.create_number_input(scrollable_frame, "Quantity", "Enter quantity", 7, 0)
        self.producttype_var = ctk.StringVar()
        self.product_type=inputclass.create_dropdown(scrollable_frame,"Product Type",item_type,9,0,self.producttype_var)
        self.fatcontentvar = ctk.StringVar()
        self.fatcontent=inputclass.create_dropdown(scrollable_frame,"Fat Content",item_fatcontent,9,1,self.fatcontentvar)

        self.product_weight=inputclass.create_number_input(scrollable_frame,"Product Weight","Enter Weight of Product",13,0)

        # self.Outlet_identifier_var = ctk.StringVar()
        # self.outlet=inputclass.create_dropdown(scrollable_frame,"Fat Content",Outlet_Identifier,11,1,self.Outlet_identifier_var)
        # self.Outlet_identifier_var = ctk.StringVar()
        # self.outlet=inputclass.create_dropdown(scrollable_frame,"Fat Content",Outlet_Identifier,11,1,self.Outlet_identifier_var)

        self.mfg_date = datepicking("Manufacturing date", 9+3, 0, 10+3, 0)
        self.exp_date = datepicking("Expiry date", 9+3, 1, 10+3, 1)


        # Populate form if initial data is provided
        if self.initial_data:
            self.populate_form()

        # Submit button
        submit_button_text = "Add Product" if self.initial_data is None else "Update Product"
        submit_button = ctk.CTkButton(scrollable_frame, text=submit_button_text, command=self.submit_data, width=200, height=40)
        submit_button.grid(row=13+3, column=0, columnspan=2, pady=(30, 25))

        self._create_product_table() # Ensure table exists

    def _create_product_table(self):
        conn = sqlite3.connect('producttable.db')
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
            Status TEXT,
            Outlet TEXT,
            prod_type TEXT,
            prod_weight INT,
            Outlet_Size TEXT,
            Item_Fatcont TEXT,
            Outlet_Location TEXT,
            Outlet_Type TEXT
            
            
            
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

    def validate_dates(self):
        try:
            mfg_str = self.mfg_date.get()
            exp_str = self.exp_date.get()

            mfg_date = datetime.strptime(mfg_str, "%Y-%m-%d")
            exp_date = datetime.strptime(exp_str, "%Y-%m-%d")
            today = datetime.today()

            if mfg_date > today:
                messagebox.showerror("Invalid MFG Date", "Manufacturing date cannot be in the future.")
                return False

            if exp_date <= mfg_date:
                messagebox.showerror("Invalid EXP Date", "Expiry date must be after manufacturing date.")
                return False

            if exp_date < today:
                messagebox.showerror("Expired Product", "Expiry date cannot be in the past.")
                return False
            min_shelf_life = timedelta(days=30)
            if (exp_date - today) < min_shelf_life:
                messagebox.showerror("Invalid Expiry Date", "Product expiry date must be at least 1 month from today.")
                return False

            shelf_life = exp_date.year - mfg_date.year
            if shelf_life > 5:
                messagebox.showerror("Invalid Shelf Life", "Shelf life exceeds 5 years.")
                return False

            messagebox.showinfo("Valid", "Dates are valid!")
            return True

        except ValueError:
            messagebox.showerror("Invalid Format", "Please enter dates in YYYY-MM-DD format.")
            return False
    def submit_data(self):
        batch = self.Batch_entry.get()
        if not batch.startswith("INV-"):
            batch = f"INV-{batch}"

        batch = self.Batch_entry.get().strip()
        name = self.name_entry.get().strip()
        description = self.desc_textbox.get("1.0", "end").strip()
        cost_price = self.cost_price.get().strip()
        sale_price = self.sale_price.get().strip()
        quantity = self.quantity_entry.get().strip()
        supplier = self.supplier.get().strip()
        category = self.category[0].get().strip()  # because it's a tuple
        product_type = self.product_type.get().strip()
        fat_content = self.fatcontent.get().strip()
        product_weight = self.product_weight.get().strip()
        mfg_date = self.mfg_date.get().strip()
        exp_date = self.exp_date.get().strip()



        # Check for empty fields
        required_fields = {
            "Batch": batch,
            "Name": name,
            "Cost Price": cost_price,
            "Sale Price": sale_price,
            "Quantity": quantity,
            "Supplier": supplier,
            "Category": category,
            "Product Type": product_type,
            "Fat Content": fat_content,
            "Product Weight": product_weight,
            "Mfg Date": mfg_date,
            "Exp Date": exp_date
        }

        missing_fields = [key for key, value in required_fields.items() if not value]

        if missing_fields:
            tkmessagebox.showerror("Validation Error",
                                   f"Please fill in the following fields:\n- " + "\n- ".join(missing_fields))
            return
        if not self.validate_dates():
            # Validation failed, stop here
            return

        # Determine stock status
        try:
            quantity_value = int(quantity)
        except ValueError:
            tkmessagebox.showerror("Invalid Input", "Quantity must be a number.")
            return
        if (int(quantity))<=0:
            tkmessagebox.showerror("Invalid Input", "Quantity must be greater than 0 ")
            return
        if (int(cost_price))<=0:
            tkmessagebox.showerror("Invalid Input", "Cost Price must be greater than 0 ")
            return
        if (int(sale_price))<=0:
            tkmessagebox.showerror("Invalid Input", "Selling price  must be greater than 0 ")
            return


        status = "Out of Stock" if quantity_value < 1 else "In Stock"

        # Prepare data for database
        data = (
        batch, name, description, cost_price, sale_price, quantity, supplier, mfg_date, exp_date, category, status,fat_content,product_type,product_weight,)

        conn = sqlite3.connect('producttable.db')
        cursor = conn.cursor()
        quantity=int(self.quantity_entry.get())
        status = "Out of Stock" if  quantity< 1 else "In Stock"
        Outlet_Identifier="OUT010"
        Outlet_Size="High"
        Outlet_Type="Supermarket Type 1 "
        Outlet_Location="Tier 1"
        data = (
            self.Batch_entry.get(), self.name_entry.get(), self.desc_textbox.get("1.0", "end"),
            self.cost_price.get(), self.sale_price.get(), self.quantity_entry.get(),
            self.supplier.get(), self.mfg_date.get(), self.exp_date.get(),self.category[0].get(),status,self.fatcontent.get(),self.product_type.get(),self.product_weight.get(),Outlet_Identifier,Outlet_Size,Outlet_Type,Outlet_Location
        )
        # Status
        # TEXT,
        # Outlet
        # TEXT,
        # prod_type
        # TEXT
        # Outlet_Size
        # TEXT,
        # Item_Fatcont
        # TEXT,
        # Outlet_Location
        # TEXT,
        # Outlet_Type
        # TEXT

        if self.initial_data:  # It's an update
            product_id = self.initial_data[0]
            cursor.execute('''
                UPDATE product SET
                    batch=?, name=?, description=?, cost_price=?, sales_price=?,
                    quantity=?, supplier=?, mfg_date=?, exp_date=?,category=?,Status=?,Item_Fatcont=?,prod_type=?,prod_weight=?,Outlet=?,Outlet_Size=?,Outlet_Type=?,Outlet_Location=?,
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
                    batch, name, description, cost_price, sales_price, quantity, supplier, mfg_date, exp_date,category,Status,
                    Item_Fatcont,prod_type,prod_weight,Outlet,Outlet_Size,Outlet_Type,Outlet_Location
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?)
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

