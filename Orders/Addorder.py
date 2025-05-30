import os
import sqlite3
import subprocess
from datetime import datetime
import platform
from tkinter import ttk
import customtkinter as ctk
import tkinter as tk

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

import Listtables
from checkbox import CheckboxTreeviewHelper
from input import inputclass
from tkinter import messagebox
from datetime import date

class AddOrder(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent, data_table_instance=None, initial_data=None):
        super().__init__(parent)
        self.price = None
        self.selling_price = None
        self.data_table_instance = data_table_instance
        self.initial_data = initial_data
        self.cart_items = []  # ✅ FIXED: Initialize cart_items

        self.order_card = ctk.CTkFrame(self, width=1000, corner_radius=5, border_width=2,
                                       fg_color='#EAF0F1', bg_color="white")
        self.order_card.place(relx=0.5, rely=0.5, anchor="center")

        self.header_label = ctk.CTkLabel(self.order_card,
                                         text="Add Order" if self.initial_data is None else "Update Order",
                                         font=("Helvetica", 24, "bold"), text_color="black")
        self.header_label.grid(row=0, column=0, columnspan=2, pady=(25, 10))

        self.product_names = [item[0] for item in Listtables.product()]
        self.Customer_name_entry = inputclass.create_input(self.order_card, "Customer Name",
                                                           "Enter the Customer's Name", 1, 0)
        self.select_product = inputclass.create_dropdown(self.order_card, "Products", self.product_names, 1, 1)

        self.cart_tree = self.create_cart_tree(self.order_card)
        self.checkbox_helper = CheckboxTreeviewHelper(self.cart_tree)

        # self.quantity_label = ctk.CTkLabel(self.order_card, text="Quantity:", font=("Arial", 12), text_color="black")
        # self.quantity_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        # self.quantity_entry = ctk.CTkEntry(self.order_card, width=100)
        # self.quantity_entry.grid(row=3, column=0, padx=10, pady=5, )
        self.quantity_label = ctk.CTkLabel(self.order_card, text="No. Of Items to Order:", font=("Arial", 12), text_color="black")
        self.quantity_label.grid(row=4, column=0, padx=20, pady=5)

        self.spinbox = tk.Spinbox(self.order_card, from_=0, to=100, width=5, font=("Helvetica", 14))
        self.spinbox.grid(row=4, column=0, columnspan=2)

        self.submit_button = ctk.CTkButton(self.order_card, text="Add  To Cart", command=self.add_to_cart, width=200,
                                           height=40)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=(30, 25))

        self.order_button = ctk.CTkButton(self.order_card, text="Place Order", command=self.place_order, width=200,
                                          height=40)
        self.order_button.grid(row=8, column=0, columnspan=2, pady=(0, 25))


        self.total_label = ctk.CTkLabel(self.order_card, text="Total: $0.00", font=("Arial", 14, "bold"),
                                        text_color="black")
        self.total_label.grid(row=12, column=0, columnspan=2, pady=(10, 0), sticky="e")




    def create_cart_tree(self, parent):
        cart_tree = ttk.Treeview(parent, columns=("Select", "Product", "Price", "Qty","add","Total"), show="headings",
                                 style="Elevated.Treeview")
        cart_tree.heading("Select", text="Select", anchor=tk.CENTER)
        cart_tree.heading("Product", text="Product", anchor=tk.W)
        cart_tree.heading("Price", text="Price", anchor=tk.CENTER)
        cart_tree.heading("Qty", text="Quantity", anchor=tk.CENTER)
        cart_tree.heading("add", text="No. of Items ", anchor=tk.CENTER)
        cart_tree.heading("Total", text="Total", anchor=tk.CENTER)

        cart_tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        cart_tree.column("Select", width=50, anchor=tk.CENTER)
        cart_tree.column("Product", width=300, anchor=tk.W)
        cart_tree.column("Price", width=100, anchor=tk.CENTER)
        cart_tree.column("Qty", width=100, anchor=tk.CENTER)
        cart_tree.column("add", width=100, anchor=tk.CENTER)
        cart_tree.column("Total", width=100, anchor=tk.CENTER)

        self.apply_modern_style(cart_tree)
        return cart_tree

    def apply_modern_style(self, treeview):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Treeview.Heading",
                        background="#e0f2fe",
                        foreground="red",
                        font=('Arial', 13, 'bold'),
                        relief='flat',
                        borderwidth=0,
                        padding=(0, 10))

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=35,
                        relief='flat',
                        borderwidth=0,
                        fieldbackground="white")

        style.map('Treeview',
                  background=[('selected', '#a7c1e3')],
                  foreground=[('selected', 'black')])

        treeview.tag_configure('oddrow', background="#ffffff")
        treeview.tag_configure('evenrow', background="#f0f0f0")

    def add_to_cart(self):
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        self.product_name = self.select_product.get()

        cursor.execute("SELECT * FROM product WHERE name = ?", (self.product_name,))
        product_data = cursor.fetchone()
        print(product_data)
        conn.close()

        if product_data:
            self.costprice=product_data[4]
            self.price = product_data[5]
            quantity = product_data[6]
            print(quantity)


            # if not quantity.isdigit():
            #     messagebox.showerror("Error", "Please enter a valid quantity.")
            #     return

            item = self.spinbox.get()
            print(item)
            totalprice=int(item)*self.price


            # Check if product already in cart
            self.existing_item = next((itemname for itemname in self.cart_items if itemname["name"] == self.product_name), None)


            if self.existing_item:
                print(self.existing_item)
                print(self.price)

                # Update quantity and 'add' value

                self.existing_item["add"] = int(self.existing_item["add"]) + int(item)
                print("new existing item is ",self.existing_item["add"])
                total = int(self.price) * int (self.existing_item["add"])
                print("total is ",total)



                # Also update the Treeview row
                self.cart_tree.item(self.existing_item["item_id"], values=("⬜",self.product_name, self.price, quantity, self.existing_item["add"],total))

            else:
                # Insert new item
                item_id = self.checkbox_helper.insert_with_checkbox("", "end",
                                                                    values=(self.product_name, self.price, quantity, item,totalprice))
                self.cart_items.append({
                    "item_id": item_id,
                    "name": self.product_name,
                    "price": self.price,
                    "costprice" : self.costprice,
                    "quantity": quantity,
                    "add": item,
                    "Total" :totalprice
                })
                print("cartitems",self.cart_items)

            self.select_product.set("Select a product")
            # self.quantity_entry.delete(0, tk.END)
            # self.update_total()

    # def update_total(self):
    #
    #     total = sum(item["price"] * item["quantity"] for item in self.cart_items)
    #     self.total_label.configure(text=f"Total: ${total:.2f}")

    def place_order(self):



        wanteditem = (item["add"] for item in self.cart_items)

        checked_items = self.checkbox_helper.get_checked_items()
        print("checked item: ",checked_items)

        if not checked_items:
            messagebox.showinfo("Info", "No items selected to order.")
            return


        # Compare with available stock
        for i in range(len(self.cart_items)):

            for check in checked_items:
                matched_item = next((item for item in self.cart_items if item["item_id"] == check), None)
                customer_name = self.Customer_name_entry.get()
                if not customer_name:
                    messagebox.showerror("Error", "Please enter customer name.")
                    return
                if matched_item:
                    available = int(matched_item["quantity"])
                    requested = int(matched_item["add"])
                    print("len",(self.cart_items[i]))
                    print(f"\n🛒 Product: {matched_item['name']}"),
                    print(f"Available: {available}, Requested: {requested}")

                    if requested > available:
                        messagebox.showinfo("Info", f"Not Enough Stock for {matched_item['name']} ")

                        print(f"⚠️ Not enough stock for ")
                        return
                    else:
                        print(f"✅ Order is valid for {matched_item['name']}")
                        self.place_order_db(matched_item["item_id"],
                                            matched_item["name"], matched_item["price"], matched_item["add"],matched_item["costprice"])
                        self.clear_cart()
                        self.generate_receipt(customer_name,matched_item)


                else:
                    print(f"❗ Item with ID {check} not found in cart.")








    def place_order_db(self,batch,product_name,price,quantity_toadd,costprice):
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                BatchNo TEXT,
                Product_name TEXT,
                Price TEXT,
                Cost_Price TEXT,
                ItemNo TEXT,
                order_date TEXT
                )''')

        conn.commit()
        conn.close()

        conn = sqlite3.connect('orders.db')

        cursor = conn.cursor()
        if self.product_exists(product_name):
            cursor.execute('''
                UPDATE order_table
                SET ItemNo = ItemNo + ?
                WHERE Product_name = ?
            ''', (quantity_toadd, product_name))
            self.reduce_cart_quantity(quantity_toadd)
        else :
            cursor.execute('''
                       INSERT INTO order_table (BatchNo,Product_name, Price,Cost_Price, ItemNo,order_date)
                       VALUES (?, ?, ?,?,?,?)
                   ''', (batch,product_name, price,costprice, quantity_toadd,date.today()))
            self.reduce_cart_quantity(quantity_toadd)
        conn.commit()
        conn.close()



        # self.clear_cart()
        #
        # if self.data_table_instance and hasattr(self.data_table_instance, 'refresh_table'):
        #     self.data_table_instance.refresh_table()







    def clear_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.cart_items.clear()
        self.checkbox_helper.clear_checkboxes()
        self.total_label.configure(text="Total: $0.00")
        self.Customer_name_entry.delete(0, tk.END)
        self.select_product.set("Select a product")
        self.spinbox.delete(0, tk.END)
        self.spinbox.insert(0, "0")


    def product_exists(self,name):
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM order_table WHERE Product_name = ?", (name,))
        result = cursor.fetchone()  # Returns None if no result

        conn.close()

        return result is not None
    def reduce_cart_quantity(self,additem):
        conn = sqlite3.connect('myapp.db')
        cursor = conn.cursor()
        self.product_names = self.select_product.get()
        print("productname is ",self.product_name)

        cursor.execute("UPDATE product SET quantity=quantity - ? WHERE name = ?", (additem, self.product_name,))
        conn.commit()
        conn.close()

    def generate_receipt(self, customer_name, items,):
        filename = f"invoice_{customer_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        width = 3.1 * inch
        height = 10 * inch
        c = canvas.Canvas(filename, pagesize=(width, height))

        y = height - 20

        c.setFont("Courier-Bold", 12)
        c.drawString(20, y, "XYZ PHARMACY")
        y -= 15
        c.setFont("Courier", 10)
        c.drawString(20, y, "123 Health St.")
        y -= 12
        c.drawString(20, y, "Phone: 555-123456")
        y -= 20

        c.drawString(20, y, f"Customer: {customer_name}")
        y -= 15
        c.drawString(20, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        c.drawString(20, y, "-" * 32)
        y -= 15

        total = 0

        name = items["name"]
        qty = items["add"]
        price = items["price"]
        item_total = int(qty) * int(price)
        total += item_total
        c.drawString(20, y, f"{name[:10]:<10} {qty} x {price:.2f} = {item_total:.2f}")
        y -= 12

        y -= 8
        c.drawString(20, y, "-" * 32)
        y -= 15
        c.setFont("Courier-Bold", 11)
        c.drawString(20, y, f"{'TOTAL:':<20} Rs. {total:.2f}")
        y -= 25
        c.setFont("Courier", 10)
        c.drawString(20, y, "Thank you for your purchase!")
        y -= 15
        c.drawString(20, y, "Get well soon :)")

        c.showPage()
        c.save()

        # Optional: Automatically open the PDF
        system = platform.system()

        if system == "Windows":
            os.startfile(filename)
        elif system == "Darwin":  # macOS
            subprocess.call(["open", filename])
        else:  # Linux
            subprocess.call(["xdg-open", filename])


    # Windows

