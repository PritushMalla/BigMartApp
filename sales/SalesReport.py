import sqlite3
from datetime import date
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt

class Salesreport(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  # Make main frame transparent to show app background
        self.parent = parent

        # Store latest report data for plotting
        self.latest_data = []
        self.latest_report_title = ""

        # Configure grid layout for the main frame (if needed)
        self.grid_columnconfigure(0, weight=1)

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Sales Report", font=("Arial", 32, "bold"), text_color="#E0E0E0")
        self.title_label.pack(pady=(30, 20))  # Increased padding for title

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")  # Transparent background for buttons frame
        self.button_frame.pack(pady=10)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.monthly_button = ctk.CTkButton(
            self.button_frame, text="Monthly Report", command=self.show_monthly_report,
            width=200, height=50, font=("Arial", 18, "bold"), corner_radius=12,
            fg_color="#4A90E2", hover_color="#3A7BD5", text_color="white"
        )
        self.monthly_button.grid(row=0, column=0, padx=20, pady=10)

        self.yearly_button = ctk.CTkButton(
            self.button_frame, text="Yearly Report", command=self.show_yearly_report,
            width=200, height=50, font=("Arial", 18, "bold"), corner_radius=12,
            fg_color="#4A90E2", hover_color="#3A7BD5", text_color="white"
        )
        self.yearly_button.grid(row=0, column=1, padx=20, pady=10)

        # New plot button spanning both columns
        self.plot_button = ctk.CTkButton(
            self.button_frame, text="Show Graph", command=self.show_plot,
            width=420, height=50, font=("Arial", 18, "bold"), corner_radius=12,
            fg_color="#4A90E2", hover_color="#3A7BD5", text_color="white"
        )
        self.plot_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Text output area
        self.output_textbox = ctk.CTkTextbox(
            self, width=800, height=400, corner_radius=15,
            font=("Consolas", 14),
            fg_color="#2B2B2B",  # Dark background for textbox content
            text_color="#E0E0E0",  # Light text for readability
            border_color="#4A90E2",  # Blue border
            border_width=2,
            wrap="word"  # Wrap long lines
        )
        self.output_textbox.pack(pady=25, padx=30, fill="both", expand=True)

        # Initial message in textbox
        self.output_textbox.insert("end", "Select a report type to view sales data.\n\n")
        self.output_textbox.insert("end", "-" * 60 + "\n")
        self.output_textbox.insert("end", "Report will appear here after selection.")

    def get_sales_report(self, start_date, end_date):
        """Fetches sales data from the database within a specified date range."""
        conn = None
        try:
            conn = sqlite3.connect("neworder6.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM order_table WHERE order_date BETWEEN ? AND ?",
                (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            )
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred while fetching data: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def display_report(self, data, title):
        """Displays the sales report in the text output area."""
        self.output_textbox.delete("0.0", "end")
        self.output_textbox.insert("end", f"{title} Report\n")
        self.output_textbox.insert("end", "=" * 60 + "\n\n")

        if not data:
            self.output_textbox.insert("end", "No sales data available for this period.\n")
            self.output_textbox.insert("end", "\n" + "-" * 60 + "\n")
            self.output_textbox.insert("end", "Total Sales: Rs. 0.00\n")
            return

        total = 0
        # Headers for better readability
        self.output_textbox.insert("end", f"{'Order ID':<10} | {'Date':<12} | {'Amount':>15}\n")
        self.output_textbox.insert("end", "-" * 40 + "\n")

        for row in data:
            order_id = row[0]
            amount = float(row[15])
            order_date = row[6]
            total += amount
            self.output_textbox.insert("end", f"{order_id:<10} | {order_date:<12} | {amount:>15.2f}\n")

        self.output_textbox.insert("end", "\n" + "=" * 60 + "\n")
        self.output_textbox.insert("end", f"Total Sales: Rs. {total:.2f}\n")
        self.output_textbox.insert("end", "=" * 60 + "\n")

    def show_monthly_report(self):
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        data = self.get_sales_report(start_of_month, today)
        self.latest_data = data
        self.latest_report_title = "Monthly"
        self.display_report(data, "Monthly")

    def show_yearly_report(self):
        today = date.today()
        start_of_year = date(today.year, 1, 1)
        data = self.get_sales_report(start_of_year, today)
        self.latest_data = data
        self.latest_report_title = "Yearly"
        self.display_report(data, "Yearly")

    def show_plot(self):
        if not self.latest_data:
            messagebox.showinfo("No Data", "Please generate a report first before viewing the graph.")
            return
        self.plot_report(self.latest_data, self.latest_report_title)

    def plot_report(self, data, title):
        """Plot a bar chart of sales amounts by Order ID."""
        if not data:
            messagebox.showinfo("No Data", "No sales data available to plot.")
            return

        order_ids = [row[0] for row in data]
        amounts = [float(row[15]) for row in data]

        plt.figure(figsize=(10, 6))
        plt.bar(order_ids, amounts, color="#4A90E2")
        plt.title(f"{title} Sales Report")
        plt.xlabel("Order ID")
        plt.ylabel("Amount (Rs.)")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()
