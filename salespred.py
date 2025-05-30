import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics
from xgboost import XGBRegressor
import customtkinter as ctk

# -------------------- DATA PREPROCESSING --------------------

sales_data = pd.read_csv("archive/Train.csv")

# Fill missing values
sales_data['Item_Weight'] = sales_data['Item_Weight'].fillna(sales_data['Item_Weight'].mean())


mode_of_Outlet_size = sales_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=lambda x: x.mode()[0])
miss_values = sales_data['Outlet_Size'].isnull()
sales_data.loc[miss_values, 'Outlet_Size'] = sales_data.loc[miss_values, 'Outlet_Type'].apply(
    lambda x: mode_of_Outlet_size[x])

# Store original mappings before encoding for dropdowns
# Item_Fat_Content
fat_content_map = {'Low Fat': 0, 'Regular': 1}
sales_data.replace({'Item_Fat_Content': {'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'}}, inplace=True)
original_fat_content_labels = ['Low Fat (0)', 'Regular (1)']

# Item_Type (need to get unique values and their encoding)
original_item_types = sales_data['Item_Type'].unique()
# Sort them to ensure consistent ordering in the dropdown
original_item_types.sort()

# Outlet_Size
original_outlet_sizes = ['Small', 'Medium', 'High'] # Based on common knowledge of BigMart data or observed unique values
# Ensure 'Small', 'Medium', 'High' correspond to 2, 1, 0 respectively after encoding if not already.
# It's better to fit_transform on the known categories to ensure consistency.
le_outlet_size = LabelEncoder()
le_outlet_size.fit(['High', 'Medium', 'Small']) # Fit on all possible categories in desired order
sales_data['Outlet_Size'] = le_outlet_size.transform(sales_data['Outlet_Size'])
outlet_size_map = {label: le_outlet_size.transform([label])[0] for label in le_outlet_size.classes_}
# Invert the map for dropdown labels: {encoded_value: original_label}
inverted_outlet_size_map = {v: k for k, v in outlet_size_map.items()}
dropdown_outlet_sizes = [f"{inverted_outlet_size_map[i]} ({i})" for i in sorted(inverted_outlet_size_map.keys())]

# Outlet_Location_Type
original_outlet_location_types = sales_data['Outlet_Location_Type'].unique()
original_outlet_location_types.sort() # Ensure consistent order

# Outlet_Type
original_outlet_types = sales_data['Outlet_Type'].unique()
original_outlet_types.sort() # Ensure consistent order


# Label Encoding
encoder = LabelEncoder()
cols_to_encode = ['Item_Identifier', 'Item_Fat_Content', 'Item_Type',
                  'Outlet_Identifier', 'Outlet_Location_Type', 'Outlet_Type']

# Item_Fat_Content is handled separately with a fixed map
sales_data['Item_Fat_Content'] = sales_data['Item_Fat_Content'].map(fat_content_map)


# Apply LabelEncoder for others
item_type_encoder = LabelEncoder()
sales_data['Item_Type'] = item_type_encoder.fit_transform(sales_data['Item_Type'])
# Create dropdown options for Item_Type
item_type_dropdown_options = [f"{label} ({item_type_encoder.transform([label])[0]})" for label in item_type_encoder.classes_]

outlet_id_encoder = LabelEncoder()
sales_data['Outlet_Identifier'] = outlet_id_encoder.fit_transform(sales_data['Outlet_Identifier'])
# Create dropdown options for Outlet_Identifier
outlet_id_dropdown_options = [f"{label} ({outlet_id_encoder.transform([label])[0]})" for label in outlet_id_encoder.classes_]


outlet_location_type_encoder = LabelEncoder()
sales_data['Outlet_Location_Type'] = outlet_location_type_encoder.fit_transform(sales_data['Outlet_Location_Type'])
# Create dropdown options for Outlet_Location_Type
outlet_location_dropdown_options = [f"{label} ({outlet_location_type_encoder.transform([label])[0]})" for label in outlet_location_type_encoder.classes_]


outlet_type_encoder = LabelEncoder()
sales_data['Outlet_Type'] = outlet_type_encoder.fit_transform(sales_data['Outlet_Type'])
# Create dropdown options for Outlet_Type
outlet_type_dropdown_options = [f"{label} ({outlet_type_encoder.transform([label])[0]})" for label in outlet_type_encoder.classes_]


# Splitting data into features and target
X = sales_data.drop(columns=['Item_Outlet_Sales', 'Item_Identifier'])
Y = sales_data['Item_Outlet_Sales']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Train the model
regressor = XGBRegressor()
regressor.fit(X_train, Y_train)


# -------------------- GUI CLASS --------------------

class BigMartSalesApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        title_label = ctk.CTkLabel(self, text="📦 BigMart Sales Predictor", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=20)

        # Output Label
        self.result_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18))
        self.result_label.pack(pady=10)

        # Predict Button
        predict_btn = ctk.CTkButton(self, text="Predict Sales", command=self.predict_sales)
        predict_btn.pack(pady=10)

        # Scrollable Frame for Inputs
        scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Define the input fields and their types
        self.input_config = [
            {"label": "Item Weight", "type": "entry"},
            {"label": "Item Fat Content", "type": "dropdown", "options": original_fat_content_labels},
            {"label": "Item Visibility", "type": "entry"},
            {"label": "Item Type", "type": "dropdown", "options": item_type_dropdown_options},
            {"label": "Item MRP", "type": "entry"},
            {"label": "Outlet Identifier", "type": "dropdown", "options": outlet_id_dropdown_options},
            {"label": "Outlet Year", "type": "entry", "placeholder": "e.g., 1987"},
            {"label": "Outlet Size", "type": "dropdown", "options": dropdown_outlet_sizes},
            {"label": "Outlet Location Type", "type": "dropdown", "options": outlet_location_dropdown_options},
            {"label": "Outlet Type", "type": "dropdown", "options": outlet_type_dropdown_options}
        ]

        self.input_widgets = {} # Stores references to the entry/dropdown widgets

        for config in self.input_config:
            field_label = config["label"]
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(pady=5, fill="x", padx=10)
            label = ctk.CTkLabel(frame, text=field_label, anchor="w")
            label.pack(side="top", anchor="w")

            if config["type"] == "entry":
                entry = ctk.CTkEntry(frame, placeholder_text=config.get("placeholder", "Enter value"))
                entry.pack(side="top", fill="x")
                self.input_widgets[field_label] = entry
            elif config["type"] == "dropdown":
                dropdown = ctk.CTkOptionMenu(frame, values=config["options"])
                dropdown.pack(side="top", fill="x")
                # Set default value to the first option
                if config["options"]:
                    dropdown.set(config["options"][0])
                self.input_widgets[field_label] = dropdown

    def predict_sales(self):
        try:
            # Map GUI field labels to the actual feature names expected by the model
            gui_to_model_map = {
                "Item Weight": 'Item_Weight',
                "Item Fat Content": 'Item_Fat_Content',
                "Item Visibility": 'Item_Visibility',
                "Item Type": 'Item_Type',
                "Item MRP": 'Item_MRP',
                "Outlet Identifier": 'Outlet_Identifier',
                "Outlet Year": 'Outlet_Establishment_Year',
                "Outlet Size": 'Outlet_Size',
                "Outlet Location Type": 'Outlet_Location_Type',
                "Outlet Type": 'Outlet_Type'
            }

            # Dictionaries to store selected values (parsed)
            input_values = {}

            for config in self.input_config:
                field_label = config["label"]
                model_feature_name = gui_to_model_map.get(field_label)
                if not model_feature_name:
                    continue # Skip if no mapping found

                widget = self.input_widgets[field_label]
                value = widget.get()

                if config["type"] == "entry":
                    input_values[model_feature_name] = float(value)
                elif config["type"] == "dropdown":
                    # Extract the numerical code from the dropdown string
                    # e.g., "Low Fat (0)" -> 0
                    #       "OUT010 (3)" -> 3
                    numeric_code = int(value.split('(')[-1].replace(')', ''))
                    input_values[model_feature_name] = numeric_code

            # Ensure inputs are in the exact order the model expects
            ordered_inputs = [input_values[feature] for feature in X_train.columns]

            # --- ADDED PRINT STATEMENT HERE ---
            print("\n--- Input Features Being Sent to Model ---")
            print(f"Feature Order: {list(X_train.columns)}")
            print(f"Input Values:  {ordered_inputs}")
            print("------------------------------------------\n")
            # ----------------------------------

            input_array = np.array(ordered_inputs).reshape(1, -1)

            prediction = regressor.predict(input_array)[0]
            self.result_label.configure(text=f"💰 Predicted Sales over the next few months are:\n ₹{round(prediction, 2)}", text_color="green")
        except ValueError:
            self.result_label.configure(text=f"❌ Error: Please ensure all inputs are valid numbers or selections.", text_color="red")
        except Exception as e:
            self.result_label.configure(text=f"❌ An unexpected error occurred: {str(e)}", text_color="red")

# -------------------- RUN APP --------------------
