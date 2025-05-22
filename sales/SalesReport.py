import sqlite3
from datetime import date
from tkinter import Tk, Button, Text, END

import customtkinter as ctk

class Salesreport(ctk.CTkFrame):
    ctk.set_appearance_mode("light")
    def __init__(self, parent):
        super().__init__(parent)
        def get_sales_report(start_date, end_date):
            conn = sqlite3.connect("orders.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_table WHERE order_date BETWEEN ? AND ?", (start_date, end_date))
            data = cursor.fetchall()
            conn.close()
            return data

        def display_report(data, title):
            self.output_text.delete(1.0, END)
            self.output_text.insert(END, f"{title} Report\n")
            self.output_text.insert(END, "-"*40 + "\n")
            total = 0
            for row in data:
                # Adjust column indices based on your actual schema
                order_id = row[0]

                date = row[5]
                amount = row[3]
                total += float(amount)
                self.output_text.insert(END, f"Order ID: {order_id}| Date: {date} | Amount: {amount}\n")
            self.output_text.insert(END, "-"*40 + "\n")
            self.output_text.insert(END, f"Total Sales: {total}\n")

        def show_monthly_report():
            today = date.today()
            start_of_month = date(today.year, today.month, 1)
            data = get_sales_report(start_of_month, today)
            display_report(data, "Monthly")

        def show_yearly_report():
            today = date.today()
            start_of_year = date(today.year, 1, 1)
            data = get_sales_report(start_of_year, today)
            display_report(data, "Yearly")

        # GUI Setup
        root = Tk()
        root.title("Sales Report")

        Button(root, text="Monthly Report", command=show_monthly_report, width=20).pack(pady=5)
        Button(root, text="Yearly Report", command=show_yearly_report, width=20).pack(pady=5)

        self.output_text = Text(root, width=80, height=20)
        self.output_text.pack(pady=10)