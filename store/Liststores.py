

import customtkinter as ctk

from Listtables import DataTable
from store.addnewstore import AddStore


class ListStore(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent):
        super().__init__(parent)


        # Centered card container
        card = ctk.CTkFrame(self, width=800, corner_radius=5, border_width=2,
                            fg_color='#EAF0F1',bg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header = ctk.CTkLabel(card, text="Add Store", font=("Helvetica", 24, "bold"), text_color="black")
        header.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        self.configure(fg_color="white")

        db_path = 'store.db'
        display_columns=["S.No.","Store Name ", "Manager Name", "Phone Number","Location","Status"]
        store_columns = ["id","StoreName","Manager","PhoneNo","Location","Status"]
        self.product_table = DataTable(self, db_path, "store", store_columns, AddStore,display_columns,
                                       title="Store List",AddButtonname="Add Store")  # Removed the frame and added title
        self.product_table.pack(pady=20)
        # Corrected path
