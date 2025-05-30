import sqlite3
from datetime import date
from tkinter import messagebox

import customtkinter as ctk

class Salesreport(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent) # Make main frame transparent to show app background
        self.parent = parent

        # Configure grid layout for the main frame (if needed, though pack is used here)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(2, weight=1) # Not strictly needed with pack, but good practice for future expansion

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Sales Report", font=("Arial", 32, "bold"), text_color="#E0E0E0")
        self.title_label.pack(pady=(30, 20)) # Increased padding for title

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent") # Transparent background for buttons frame
        self.button_frame.pack(pady=10)
        # Configure grid for buttons within their frame
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.monthly_button = ctk.CTkButton(self.button_frame, text="Monthly Report", command=self.show_monthly_report,
                                            width=200, height=50, font=("Arial", 18, "bold"), corner_radius=12,
                                            fg_color="#4A90E2", hover_color="#3A7BD5", text_color="white")
        self.monthly_button.grid(row=0, column=0, padx=20, pady=10) # Increased padx

        self.yearly_button = ctk.CTkButton(self.button_frame, text="Yearly Report", command=self.show_yearly_report,
                                           width=200, height=50, font=("Arial", 18, "bold"), corner_radius=12,
                                           fg_color="#4A90E2", hover_color="#3A7BD5", text_color="white")
        self.yearly_button.grid(row=0, column=1, padx=20, pady=10) # Increased padx

        # Text output area
        self.output_textbox = ctk.CTkTextbox(self, width=800, height=400, corner_radius=15,
                                             font=("Consolas", 14),
                                             fg_color="#2B2B2B", # Dark background for textbox content
                                             text_color="#E0E0E0", # Light text for readability
                                             border_color="#4A90E2", # Blue border
                                             border_width=2,
                                             wrap="word") # Wrap long lines
        self.output_textbox.pack(pady=25, padx=30, fill="both", expand=True) # Increased padding, allow expansion

        # Initial message in textbox
        self.output_textbox.insert("end", "Select a report type to view sales data.\n\n")
        self.output_textbox.insert("end", "-" * 60 + "\n")
        self.output_textbox.insert("end", "Report will appear here after selection.")


    def get_sales_report(self, start_date, end_date):
        """Fetches sales data from the database within a specified date range."""
        conn = None
        try:
            conn = sqlite3.connect("orders.db")
            cursor = conn.cursor()
            # Original query: SELECT * FROM order_table WHERE order_date BETWEEN ? AND ?
            # Assuming order_table has columns: order_id, customer_name, product_name, amount, quantity, order_date
            # The display_report function expects row[0] for order_id, row[3] for amount, row[5] for order_date.
            # No changes to the database query logic as per request.
            cursor.execute("SELECT * FROM order_table WHERE order_date BETWEEN ? AND ?",
                           (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
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
        self.output_textbox.insert("end", "=" * 60 + "\n\n") # Enhanced separator

        if not data:
            self.output_textbox.insert("end", "No sales data available for this period.\n")
            self.output_textbox.insert("end", "\n" + "-" * 60 + "\n")
            self.output_textbox.insert("end", "Total Sales: Rs. 0.00\n")
            return

        total = 0
        # Headers for better readability in the textbox
        self.output_textbox.insert("end", f"{'Order ID':<10} | {'Date':<12} | {'Amount':>15}\n")
        self.output_textbox.insert("end", "-" * 40 + "\n") # Separator for headers

        for row in data:
            order_id = row[0]
            order_date = row[5]
            amount = float(row[3])
            total += amount
            self.output_textbox.insert("end", f"{order_id:<10} | {order_date:<12} | {amount:>15.2f}\n") # Formatted output

        self.output_textbox.insert("end", "\n" + "=" * 60 + "\n") # Enhanced separator
        self.output_textbox.insert("end", f"Total Sales: Rs. {total:.2f}\n")
        self.output_textbox.insert("end", "=" * 60 + "\n")


    def show_monthly_report(self):
        """Generates and displays the sales report for the current month."""
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        data = self.get_sales_report(start_of_month, today)
        self.display_report(data, "Monthly")

    def show_yearly_report(self):
        """Generates and displays the sales report for the current year."""
        today = date.today()
        start_of_year = date(today.year, 1, 1)
        data = self.get_sales_report(start_of_year, today)
        self.display_report(data, "Yearly")
