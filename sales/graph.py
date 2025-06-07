import sqlite3
from datetime import date, timedelta
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class Salesreportgraph(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # ... Your existing UI initialization code here ...

        # Add new button frame for visualizations
        self.vis_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.vis_button_frame.pack(pady=10)
        self.vis_button_frame.grid_columnconfigure((0, 1), weight=1)

        self.top_products_button = ctk.CTkButton(self.vis_button_frame, text="Top Selling Products",
                                                 command=self.show_top_selling_products,
                                                 width=200, height=50, font=("Arial", 18, "bold"),
                                                 corner_radius=12, fg_color="#4A90E2",
                                                 hover_color="#3A7BD5", text_color="white")
        self.top_products_button.grid(row=0, column=0, padx=20, pady=10)

        self.sales_over_time_button = ctk.CTkButton(self.vis_button_frame, text="Sales Over Time",
                                                    command=self.show_sales_over_time,
                                                    width=200, height=50, font=("Arial", 18, "bold"),
                                                    corner_radius=12, fg_color="#4A90E2",
                                                    hover_color="#3A7BD5", text_color="white")
        self.sales_over_time_button.grid(row=0, column=1, padx=20, pady=10)

    def fetch_top_selling_products(self):
        """Fetch total sales per product, sorted descending."""
        try:
            conn = sqlite3.connect("neworder6.db")
            cursor = conn.cursor()
            # Assuming order_table columns: product_name (index?), amount (index 3)
            # Adjust indices if needed
            cursor.execute("""
                SELECT product_name, SUM(Sales) as total_sales
                FROM order_table
                GROUP BY product_name
                ORDER BY total_sales DESC
                LIMIT 10
            """)
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching top products: {e}")
            return []
        finally:
            conn.close()

    def fetch_sales_over_time(self, days=30):
        """Fetch daily total sales for the last `days` days."""
        try:
            conn = sqlite3.connect("neworder6.db")
            cursor = conn.cursor()
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            cursor.execute("""
                SELECT order_date, SUM(Sales) as daily_total
                FROM order_table
                WHERE order_date BETWEEN ? AND ?
                GROUP BY order_date
                ORDER BY order_date
            """, (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching sales over time: {e}")
            return []
        finally:
            conn.close()

    def show_top_selling_products(self):
        data = self.fetch_top_selling_products()
        if not data:
            messagebox.showinfo("No Data", "No sales data available for top products.")
            return

        products, sales = zip(*data)  # unzip to two lists

        # Plotting in a new popup window
        self.plot_bar_chart(products, sales, title="Top Selling Products", xlabel="Products", ylabel="Total Sales (Rs.)")

    def show_sales_over_time(self):
        data = self.fetch_sales_over_time()
        if not data:
            messagebox.showinfo("No Data", "No sales data available for sales over time.")
            return

        dates, daily_totals = zip(*data)
        # Convert string dates to datetime.date objects for better x-axis formatting
        dates = [date.fromisoformat(d) for d in dates]

        self.plot_line_chart(dates, daily_totals, title="Sales Over Last 30 Days", xlabel="Date", ylabel="Daily Sales (Rs.)")

    def plot_bar_chart(self, categories, values, title="", xlabel="", ylabel=""):
        """Show bar chart in a popup window using Matplotlib embedded in Tkinter."""
        popup = Toplevel(self)
        popup.title(title)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(categories, values, color="#4A90E2")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_line_chart(self, x, y, title="", xlabel="", ylabel=""):
        """Show line chart in a popup window using Matplotlib embedded in Tkinter."""
        popup = Toplevel(self)
        popup.title(title)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, marker='o', linestyle='-', color="#4A90E2")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.autofmt_xdate()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
