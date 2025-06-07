import customtkinter as ctk


from Orders.Addorder import AddOrder
from Productfile.listprodcategory import ListProductCategories
from Productfile.productform import ProductForm
from Suppliers.addsuppliers import AddSuppliers
from Suppliers.listsuppliers import ListSuppliers
from profit.profitcalc import ProfitCalculator
from sales.SalesReport import Salesreport
from sales.graph import Salesreportgraph
from salespred import BigMartSalesApp
from store.Liststores import ListStore
from Productfile.addproductcategory import Addproductcategory
from totalsalespred import BigMartForecastingApp

# Set the appearance mode and theme
ctk.set_appearance_mode("Light")  # Options: "System" / "Dark" / "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
from store.addnewstore import AddStore
from Users.CreateUser import CreateUser
from Productfile.listproduct import Listproduct
# Create the main application window
class HomeDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Shop Management System - Dashboard")
        self.geometry("1000x700")
        self.resizable(False, False)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="SHOP MANAGER", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        # Sidebar buttons
        buttons = [("Add Product", ProductForm),
                   ("Add Store", AddStore),
                   (" Add User", CreateUser),
                   ("List Product", Listproduct),
                   ("List Store ",ListStore),
                   ("Add supplier",AddSuppliers),
                   ("Supplier List",ListSuppliers),
                   ("Add Prod category",Addproductcategory),
                   ("Product Category",ListProductCategories),
                   ("Add Order",AddOrder),
                   ("Sales Report",Salesreport),
                   ("Profit",ProfitCalculator),
                   ("Sales Prediction",BigMartSalesApp),
                   ("Graph",Salesreportgraph),
                   ("Sales forcast",BigMartForecastingApp)
                   ]

        for name, key in buttons:
            btn = ctk.CTkButton(self.sidebar, text=name, command=lambda k=key: self.load_page(k))
            btn.pack(pady=5, padx=10, fill="x")

        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.dashboard_label = ctk.CTkLabel(self.main_frame, text="Welcome to the Shop Dashboard!",
                                            font=ctk.CTkFont(size=24, weight="bold"))
        self.dashboard_label.pack(pady=50)

    def load_page(self, name):
        if name == BigMartForecastingApp:  # Check if it's the specific app
            # Create an instance and show it.
            # This will open a new, independent window.
            new_app_window = name()
            new_app_window.mainloop()  # This will block your dashboard until closed
            # A better approach for a new window would be:
            # new_app_window.focus_force() # Bring it to front
            # new_app_window.grab_set() # Make it modal (optional)
            # self.wait_window(new_app_window) # Wait for it to close (optional)
        else:
        # Clear existing widgets in main_frame
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            frame = name(self.main_frame)
            frame.pack(fill="both", expand=True)

        # Display selected page name


# Run the app
if __name__ == "__main__":
    app = HomeDashboard()
    app.mainloop()
