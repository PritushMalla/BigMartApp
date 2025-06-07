import customtkinter as ctk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar # To get month names

class ProfitCalculator(ctk.CTk):
    def __init__(self, db_path="neworder6.db"): # Make db_path a parameter with default
        super().__init__()

        # Database connection
        self.conn = sqlite3.connect("neworder6.db")
        self.cur = self.conn.cursor()

        # Window setup
        self.geometry("800x600") # Make window larger for graph
        self.title("Profit Calculator & Trend")

        # Create a tabview for organization
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        # Tab 1: Current Profit
        self.tabview.add("Current Profit")
        self.tabview.set("Current Profit") # Set default tab

        # Monthly profit label
        self.monthly_profit_label = ctk.CTkLabel(self.tabview.tab("Current Profit"), text="Monthly Profit: Rs. 0.00", font=("Arial", 16))
        self.monthly_profit_label.pack(pady=20)

        # Yearly profit label
        self.yearly_profit_label = ctk.CTkLabel(self.tabview.tab("Current Profit"), text="Yearly Profit: Rs. 0.00", font=("Arial", 16))
        self.yearly_profit_label.pack(pady=20)

        # Buttons for current profit


        # Tab 2: Profit Trend Graph
        self.tabview.add("Profit Trend Graph")

        # Frame to embed the Matplotlib graph
        self.graph_frame = ctk.CTkFrame(self.tabview.tab("Profit Trend Graph"))
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button to generate graph (placed within the graph tab for clarity)
        self.btn_show_graph = ctk.CTkButton(self.tabview.tab("Profit Trend Graph"), text="Generate Profit Graph", command=self.show_profit_graph)
        self.btn_show_graph.pack(pady=10)


        # Update profit on startup
        self.update_monthly_profit()
        self.update_yearly_profit()

    def get_monthly_profit(self, year, month):
        # Adjusted query to handle potential NULL results from SUM
        query = """
        SELECT SUM((price - cost_price) * ItemNo) FROM order_table
        WHERE strftime('%Y', order_date) = ? AND strftime('%m', order_date) = ?
        """
        self.cur.execute(query, (str(year), f"{month:02d}"))
        result = self.cur.fetchone()
        return result[0] if result and result[0] is not None else 0.0 # Ensure float 0.0

    def get_yearly_profit(self, year):
        # Adjusted query to handle potential NULL results from SUM
        query = """
        SELECT SUM((price - cost_price) * ItemNo) FROM order_table
        WHERE strftime('%Y', order_date) = ?
        """
        self.cur.execute(query, (str(year),))
        result = self.cur.fetchone()
        return result[0] if result and result[0] is not None else 0.0 # Ensure float 0.0

    def update_monthly_profit(self):
        now = datetime.now()
        profit = self.get_monthly_profit(now.year, now.month)
        self.monthly_profit_label.configure(text=f"Monthly Profit ({now.strftime('%B %Y')}): Rs. {profit:.2f}")

    def update_yearly_profit(self):
        now = datetime.now()
        profit = self.get_yearly_profit(now.year)
        self.yearly_profit_label.configure(text=f"Yearly Profit ({now.year}): Rs. {profit:.2f}")

    def show_profit_graph(self):
        # Clear existing graph if any
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Fetch data for the last 12 months (or more, adjust as needed)
        profits_data = []
        labels = []
        current_date = datetime.now()

        # Let's get data for the last 12 months, including the current one
        for i in range(12):
            year = current_date.year
            month = current_date.month

            profit = self.get_monthly_profit(year, month)
            profits_data.append(profit)
            labels.append(f"{calendar.month_abbr[month]} {str(year)[2:]}") # e.g., 'Jan 23'

            # Move to the previous month
            if month == 1:
                current_date = current_date.replace(year=year - 1, month=12)
            else:
                current_date = current_date.replace(month=month - 1)

        # Reverse the lists to show oldest to newest
        profits_data.reverse()
        labels.reverse()

        # Create the Matplotlib figure and axes
        fig, ax = plt.subplots(figsize=(7, 4)) # Adjust size for embedding
        ax.plot(labels, profits_data, marker='o', linestyle='-', color='skyblue')
        ax.set_title('Monthly Profit Trend (Last 12 Months)')
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Profit (Rs.)')
        ax.tick_params(axis='x', rotation=45) # Rotate x-axis labels
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout() # Adjust layout to prevent labels from overlapping

        # Embed the plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()

    def __del__(self):
        # Ensure database connection is closed when the app is closed
        if self.conn:
            self.conn.close()