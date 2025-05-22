

import customtkinter as ctk

from Productfile.productform import ProductForm
from Listtables import  DataTable
class Listproduct(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent):
        super().__init__(parent)


        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                            fg_color='#EAF0F1',bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header = ctk.CTkLabel(card, text="Add Product", font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.configure(fg_color="white")

        db_path = 'myapp.db'  # Corrected path

        # Example usage:
        product_columns = ["id","batch", "name", "description", "cost_price", "sales_price", "quantity", "supplier", "mfg_date", "exp_date","category","Status"]
        display_columns= ["id","Batch","Name","Description","Cost Price","Sales Price ","Quantity","Supplier","MFG Date","EXP Date","Category","Status"]
        self.product_table = DataTable(self, db_path, "product", product_columns, ProductForm, display_columns,title="Product List", AddButtonname="Add Product") # Removed the frame and added title
        self.product_table.pack(pady=20)




