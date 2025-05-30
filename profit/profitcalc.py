import customtkinter as ctk
import sqlite3
from datetime import datetime

class ProfitCalculator(ctk.CTk):
    def __init__(self, db_path):
        super().__init__()

        # Database connection
        self.conn = sqlite3.connect("orders.db")
        self.cur = self.conn.cursor()

        # Window setup
        self.geometry("400x250")
        self.title("Profit Calculator")

        # Monthly profit label
        self.monthly_profit_label = ctk.CTkLabel(self, text="Monthly Profit: Rs. 0.00", font=("Arial", 16))
        self.monthly_profit_label.pack(pady=20)

        # Yearly profit label
        self.yearly_profit_label = ctk.CTkLabel(self, text="Yearly Profit: Rs. 0.00", font=("Arial", 16))
        self.yearly_profit_label.pack(pady=20)

        # Buttons
        self.btn_update_month = ctk.CTkButton(self, text="Show Current Month Profit", command=self.update_monthly_profit)
        self.btn_update_month.pack(pady=10)

        self.btn_update_year = ctk.CTkButton(self, text="Show Current Year Profit", command=self.update_yearly_profit)
        self.btn_update_year.pack(pady=10)

        # Update profit on startup
        self.update_monthly_profit()
        self.update_yearly_profit()

    def get_monthly_profit(self, year, month):
        query = """
        SELECT SUM((price - cost_price) * ItemNo) FROM order_table
        WHERE strftime('%Y', order_date) = ? AND strftime('%m', order_date) = ?
        """
        self.cur.execute(query, (str(year), f"{month:02d}"))
        result = self.cur.fetchone()
        return result[0] if result and result[0] else 0

    def get_yearly_profit(self, year):
        query = """
        SELECT SUM((price - cost_price) * ItemNo) FROM order_table
        WHERE strftime('%Y', order_date) = ?
        """
        self.cur.execute(query, (str(year),))
        result = self.cur.fetchone()
        return result[0] if result and result[0] else 0

    def update_monthly_profit(self):
        now = datetime.now()
        profit = self.get_monthly_profit(now.year, now.month)
        self.monthly_profit_label.configure(text=f"Monthly Profit ({now.strftime('%B %Y')}): Rs. {profit:.2f}")

    def update_yearly_profit(self):
        now = datetime.now()
        profit = self.get_yearly_profit(now.year)
        self.yearly_profit_label.configure(text=f"Yearly Profit ({now.year}): Rs. {profit:.2f}")

    def __del__(self):
        self.conn.close()