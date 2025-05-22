import sqlite3
from tkinter import ttk
import customtkinter as ctk
import tkinter as tk



class DataTable(ctk.CTkFrame):
    """
    A reusable component for displaying data from a database table in a Treeview.
    """

    def __init__(self, master, db_path, table_name, columns, inserttableclassname, display_columns, title="", AddButtonname="Add"):
        """
        Initializes the DataTable.

        Args:
            master: The parent widget.
            db_path: The path to the SQLite database.
            table_name: The name of the table to fetch data from.
            columns: A list of all column names in the table.
            display_columns: (Optional) A list of column names to display. If None, all columns are displayed.
            title: Title of the table
        """
        super().__init__(master, fg_color="white")

        def open_add_product():
            popup = ctk.CTkToplevel()
            popup.geometry("900x700")
            inserttableclassname(popup).pack(fill="both", expand=True) # Use ProductForm here

        self.db_path = db_path
        self.table_name = table_name
        self.columns = columns
        self.inserttableclassname = inserttableclassname
        self.display_columns = display_columns
        self.title_text = title
        self.selected_id = tk.StringVar()

        # Grid layout for the entire DataTable
        self.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')
        self.grid_rowconfigure(2, weight=1)  # Make the table_frame expand vertically
        self.grid_columnconfigure(0, weight=1) # Make the table_frame expand horizontally

        def on_row_select(event):
            selected = self.tree.focus()
            if selected:
                values = self.tree.item(selected, 'values')
                if values:
                    self.selected_id.set(values[0])
                    print(f"Selected Product ID: {self.selected_id.get()}")

        def delete_product():
            product_id = self.selected_id.get()
            if not product_id:
                print("No  selected tuple")
                return
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            print("Product deleted.")
            self.refresh_table()

        def open_update_form():
            selected_id = self.selected_id.get()
            if not selected_id:
                tk.messagebox.showerror("Error", "Please select a product in the table to update.")
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (selected_id,))
            data = cursor.fetchone()
            conn.close()

            if data:
                update_popup = ctk.CTkToplevel(self.master)
                update_popup.geometry("800x700")

                update_popup.title("Update")
                inserttableclassname(update_popup, initial_data=data,data_table_instance=self.selected_id).pack(padx=20, pady=20, fill="both", expand=True)
            else:
                tk.messagebox.showerror("Error", "Could not retrieve data for the selected product.")

        # Title label
        title_label = ctk.CTkLabel(self, text=self.title_text, font=("Arial", 24, "bold"), text_color="black")
        title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5))

        self.button_frame = ctk.CTkFrame(self, fg_color="white",)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="e", padx=10)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Add Button
        self.add_button = ctk.CTkButton(self.button_frame, text=AddButtonname, command=open_add_product,
                                        width=100, height=40)
        self.add_button.grid(row=2, column=0, padx=5)

        # Update Button
        self.update_button = ctk.CTkButton(self.button_frame, text="Update", command=open_update_form,
                                           width=100, height=40)
        self.update_button.grid(row=2, column=1, padx=5)

        # Delete Button
        self.delete_btn = ctk.CTkButton(self.button_frame, text="Delete", command=delete_product, width=100, height=40)
        self.delete_btn.grid(row=2, column=2, padx=5)

        # Refresh Table Button
        self.refresh_button = ctk.CTkButton(self.button_frame, text="Refresh Table", command=self.refresh_table,
                                            width=100, height=40,)
        self.refresh_button.grid(row=2, column=3, padx=5)


        # Container frame for Treeview and scrollbar
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=2)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Treeview inside table_frame
        #table heading eta
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show='headings')
        print(f"Display Columns: {self.columns}")
        for cols,displaycol in zip(self.columns,self.display_columns):
            # samplecol=["abc","Aaa"]
            print(cols)
            print(displaycol)
            a = self.tree.heading(cols, text=displaycol, anchor='center', )


            b=self.tree.column(cols, anchor='center', width=120)





        # Vertical scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Horizontal scrollbar (ttk)
        h_scrollbar = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.tree.xview,
                                    style="Horizontal.TScrollbar")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        self.tree.grid(row=4, column=0)
        self.apply_modern_style()


        self.scrollbar.grid(row=4, column=1, sticky='ns')  # Fixing vertical scrollbar position
        h_scrollbar.grid(row=5, column=0, sticky='ew')  # Fixing horizontal scrollbar position

        # Load data
        self.load_data()
        self.tree.bind("<<TreeviewSelect>>", on_row_select)

    def apply_modern_style(self):
        """Applies a modern style to the Treeview."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Treeview.Heading",
                        background="#e0f2fe",
                        foreground="red",
                        font = ('Arial', 13, 'bold'),
                        relief = 'flat',
                        borderwidth = 0,
                         padding = (0, 10))

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=35,
                        fieldbackground="white",
                        anchor='center')
        style.map('Treeview',
                  background=[('selected', '#a7c1e3')],
                  foreground=[('selected', 'black')])

        self.tree.tag_configure('oddrow', background="#ffffff")
        self.tree.tag_configure('evenrow', background="#f0f0f0")

        style.layout("Treeview", [('Treeview.Heading', {'sticky': 'nswe'}),
                                  ('Treeview.Treebody', {'sticky': 'nswe'}),
                                  ('Treeview.Separator', {'sticky': 'es'})])
        style.configure("Treeview.Separator",
                        background="#a0a0a0",
                        thickness=1)

    def load_data(self):
        """Loads data from the specified database table and populates the Treeview."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Construct the SQL query, handling potential differences between table columns and display columns
            select_columns = ', '.join(self.columns)
            query = f"SELECT {select_columns} FROM {self.table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.close()


            for index, row in enumerate(rows):
                display_row = [row[self.columns.index(col)] for col in self.columns]
                tag = 'oddrow' if index % 2 == 0 else 'evenrow'
                self.tree.insert('', 'end', values=display_row, tags=(tag,))
        except Exception as e:
            print(f"Error loading data from {self.table_name}: {e}")
            ctk.CTkLabel(self, text=f"Error loading data from {self.table_name}: {e}", text_color="red").grid(row=3,
                                                                                                              column=0,
                                                                                                              columnspan=3)

    def refresh_table(self):
        """Refreshes the table data from the database."""
        # Clear the existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load the data again
        self.load_data()


def suppliername():
    conn = sqlite3.connect("supplier.db")
    cursor = conn.cursor()
    query = f"SELECT Supplier_name FROM suppliers"
    cursor.execute(query)
    x = cursor.fetchall()
    return x
def productcategory():
    conn = sqlite3.connect("productcategory.db")
    cursor = conn.cursor()
    query = f"SELECT product_name FROM productcat"
    cursor.execute(query)
    y = cursor.fetchall()
    return y

def product():
    conn = sqlite3.connect("myapp.db")
    cursor = conn.cursor()
    query = f"SELECT name FROM product"
    cursor.execute(query)
    productname = cursor.fetchall()
    return productname


