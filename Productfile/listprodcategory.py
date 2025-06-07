import customtkinter as ctk


from Listtables import  DataTable
from Productfile.addproductcategory import Addproductcategory

class ListProductCategories(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent):
        super().__init__(parent)


        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                            fg_color='#EAF0F1',bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header = ctk.CTkLabel(card, text="Add Supplier", font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.configure(fg_color="white")
        db_path ="productcategory.db"
        category_columns=["id","product_name","added_date","status"]
        display_category_columns=["S.No.","Product Name", "Added Date","Status"]
        self.category_table = DataTable(self, db_path, "productcat", category_columns, Addproductcategory,
                                        display_category_columns,
                                       title="Brand List",
                                       AddButtonname="Add Category")  # Removed the frame and added title
        self.category_table.pack(pady=20)
