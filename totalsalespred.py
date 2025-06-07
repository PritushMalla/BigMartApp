import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Assuming load_order_data is correctly implemented in Orders/Addorder.py
from Orders.Addorder import load_order_data


# --- Configuration ---
TRAIN_DATA_PATH = 'archive/Train.csv'
TEST_DATA_PATH = 'archive/Test.csv'
MERGED_TRAIN_DATA_OUTPUT_PATH = "merged_train_data.csv"

# --- Inventory Parameters (Hypothetical - adjust as needed) ---
LEAD_TIME_DAYS = 7
SAFETY_STOCK_PERCENT = 0.15
FORECAST_PERIOD_DAYS = 30
PREDICTION_BASE_YEAR = 2013
FUTURE_PREDICTION_YEAR = datetime.now().year


class BigMartForecastingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BigMart Sales & Stock Forecasting")
        self.geometry("1000x700")

        # Global variables for model and data (now class attributes)
        self.model = None
        self.X_train_cols = None
        self.imputation_means = None
        self.imputation_modes = None
        self.all_categories = None
        self.df_train_base = None
        self.df_stock_recommendations_global = None # To store stock data for detailed view

        self._create_widgets()

    def _create_widgets(self):
        # Frame for buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.prepare_model_button = ttk.Button(button_frame, text="1. Prepare & Train Model", command=self._prepare_and_train_model)
        self.prepare_model_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.predict_button = ttk.Button(button_frame, text="2. Generate Forecast & Stock", command=self._run_forecasting_and_stock, state=tk.DISABLED)
        self.predict_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.show_stock_button = ttk.Button(button_frame, text="3. Show Detailed Stock", command=self._show_detailed_stock, state=tk.DISABLED)
        self.show_stock_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Scrolled Text for main output
        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=30, padx=10, pady=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.output_text.insert(tk.END, "Welcome to BigMart Sales & Stock Forecasting!\n")
        self.output_text.insert(tk.END, "1. Click 'Prepare & Train Model' to load data and train the prediction model.\n")
        self.output_text.insert(tk.END, "2. After model training, click 'Generate Forecast & Stock' to see sales predictions and a stock summary.\n")
        self.output_text.insert(tk.END, "3. Click 'Show Detailed Stock' for a comprehensive table of recommended quantities.\n")

    def _load_and_prepare_data(self):
        # Load existing merged data or original train data
        if os.path.exists(MERGED_TRAIN_DATA_OUTPUT_PATH):
            print(f"Loading existing merged data from: {MERGED_TRAIN_DATA_OUTPUT_PATH}")
            self.df_train_base = pd.read_csv(MERGED_TRAIN_DATA_OUTPUT_PATH)
        else:
            print(f"No existing merged data found. Loading original training data from: {TRAIN_DATA_PATH}")
            try:
                self.df_train_base = pd.read_csv(TRAIN_DATA_PATH)
            except FileNotFoundError:
                messagebox.showerror("File Error", f"Error: {TRAIN_DATA_PATH} not found. Please ensure it exists for the first run.")
                return None, None, None, None, None

        print(f"Base training DataFrame shape for current run: {self.df_train_base.shape}")

        # Load New Order Data
        print("\nLoading new order data...")
        df_new_raw = load_order_data()

        if df_new_raw.empty:
            print("No new orders to process. Skipping merge and using existing merged data for training.")
            df_train = self.df_train_base
        else:
            print("Processing new order data...")
            df_new = df_new_raw.rename(columns={
                'Product_name': 'Item_Identifier', 'prod_type': 'Item_Type', 'Price': 'Item_MRP',
                'prod_weight': 'Item_Weight', 'Item_Fatcont': 'Item_Fat_Content',
                'Outlet_Size': 'Outlet_Size', 'Outlet_Location': 'Outlet_Location_Type',
                'Outlet_Type': 'Outlet_Type', 'Outlet': 'Outlet_Identifier',
                'outletyear': 'Outlet_Establishment_Year', 'itemvis': 'Item_Visibility',
                'Sales': 'Item_Outlet_Sales'
            })

            if 'Item_Visibility' not in df_new.columns:
                df_new['Item_Visibility'] = 0.0
                print("Added 'Item_Visibility' column to df_new with default 0.0.")

            df_new['Item_Outlet_Sales'] = pd.to_numeric(df_new['Item_Outlet_Sales'], errors='coerce')
            nan_sales_count = df_new['Item_Outlet_Sales'].isna().sum()
            if nan_sales_count > 0:
                print(f"Warning: {nan_sales_count} non-numeric sales values coerced to NaN in df_new. Filling with 0.0.")
                df_new['Item_Outlet_Sales'].fillna(0.0, inplace=True)

            if df_new.empty:
                print("New orders DataFrame became empty after processing. Skipping merge.")
                df_train = self.df_train_base
            else:
                df_new_agg = df_new.groupby(['Item_Identifier', 'Outlet_Identifier']).agg({
                    'Item_Outlet_Sales': 'sum', 'Item_Weight': 'first', 'Item_Fat_Content': 'first',
                    'Item_Visibility': 'first', 'Item_Type': 'first', 'Item_MRP': 'first',
                    'Outlet_Establishment_Year': 'first', 'Outlet_Size': 'first',
                    'Outlet_Location_Type': 'first', 'Outlet_Type': 'first',
                }).reset_index()

                df_merged_for_save = self.df_train_base.merge(df_new_agg, on=['Item_Identifier', 'Outlet_Identifier'], how='outer',
                                                         suffixes=('', '_new'))

                df_merged_for_save['Item_Outlet_Sales'] = df_merged_for_save['Item_Outlet_Sales_new'].combine_first(
                    df_merged_for_save['Item_Outlet_Sales'])

                for col in df_new_agg.columns:
                    if col not in ['Item_Identifier', 'Outlet_Identifier', 'Item_Outlet_Sales']:
                        df_merged_for_save[col] = df_merged_for_save[f'{col}_new'].combine_first(df_merged_for_save[col])

                df_merged_for_save.drop(columns=[col for col in df_merged_for_save.columns if '_new' in col], inplace=True)
                df_merged_for_save.to_csv(MERGED_TRAIN_DATA_OUTPUT_PATH, index=False)
                print(f"Updated merged dataset saved to: {MERGED_TRAIN_DATA_OUTPUT_PATH}")
                df_train = df_merged_for_save
                print(f"Training DataFrame for current run shape after merge: {df_train.shape}")

        # Data Cleaning and Feature Engineering for Training Data
        print("\n--- Cleaning and Engineering Features for Training Data ---")
        _imputation_means = {
            'Item_Weight': df_train['Item_Weight'].mean(),
            'Item_Visibility': df_train['Item_Visibility'].mean()
        }
        _imputation_modes = {
            'Outlet_Size': df_train['Outlet_Size'].mode()[0]
        }

        df_train['Item_Weight'].fillna(_imputation_means['Item_Weight'], inplace=True)
        df_train['Outlet_Size'].fillna(_imputation_modes['Outlet_Size'], inplace=True)
        df_train['Item_Visibility'] = df_train['Item_Visibility'].replace(0, _imputation_means['Item_Visibility'])
        df_train['Item_Fat_Content'] = df_train['Item_Fat_Content'].replace(
            {'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'})
        df_train['Outlet_Establishment_Year'] = pd.to_numeric(df_train['Outlet_Establishment_Year'], errors='coerce')
        df_train['Outlet_Years'] = datetime.now().year - df_train['Outlet_Establishment_Year']

        categorical_cols = [
            "Item_Fat_Content", "Item_Type", "Outlet_Size",
            "Outlet_Location_Type", "Outlet_Type"
        ]

        _all_categories = {}
        for col in categorical_cols:
            dummies_df = pd.get_dummies(df_train[col], prefix=col, drop_first=True, prefix_sep='_')
            _all_categories[f'{col}_dummies'] = dummies_df.columns.tolist()

        df_train_encoded = pd.get_dummies(df_train, columns=categorical_cols, drop_first=True, prefix_sep='_')

        X_train = df_train_encoded.drop([
            "Item_Outlet_Sales", "Item_Identifier", "Outlet_Identifier",
            "Outlet_Establishment_Year"
        ], axis=1)
        y_train = df_train_encoded["Item_Outlet_Sales"]
        X_train.columns = X_train.columns.astype(str)

        print(f"X_train shape: {X_train.shape}")
        print(f"y_train shape: {y_train.shape}")

        return X_train, y_train, _imputation_means, _imputation_modes, _all_categories

    def _prepare_forecast_data(self, df_raw_forecast, training_features, target_year,
                               imputation_means, imputation_modes, all_categories):
        df = df_raw_forecast.copy()

        df['Item_Weight'].fillna(imputation_means['Item_Weight'], inplace=True)
        df['Outlet_Size'].fillna(imputation_modes['Outlet_Size'], inplace=True)
        df['Item_Visibility'] = df['Item_Visibility'].replace(0, imputation_means['Item_Visibility'])
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({'low fat': 'Low Fat', 'LF': 'Low Fat', 'reg': 'Regular'})

        df['Outlet_Establishment_Year'] = pd.to_numeric(df['Outlet_Establishment_Year'], errors='coerce')
        df['Outlet_Years'] = target_year - df['Outlet_Establishment_Year']

        categorical_cols_prep = [
            "Item_Fat_Content", "Item_Type", "Outlet_Size",
            "Outlet_Location_Type", "Outlet_Type"
        ]

        df_encoded_categorical = pd.DataFrame(index=df.index)

        for col in categorical_cols_prep:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, prefix_sep='_')
            known_categories_cols = all_categories.get(f'{col}_dummies', [])

            aligned_dummies = pd.DataFrame(0, index=dummies.index, columns=known_categories_cols)
            for d_col in dummies.columns:
                if d_col in aligned_dummies.columns:
                    aligned_dummies[d_col] = dummies[d_col]
            df_encoded_categorical = pd.concat([df_encoded_categorical, aligned_dummies], axis=1)

        non_categorical_cols = [col for col in df.columns if
                                col not in categorical_cols_prep and col not in ['Item_Identifier', 'Outlet_Identifier',
                                                                                 'Outlet_Establishment_Year', 'Item_Outlet_Sales']]
        df_encoded_numerical = df[non_categorical_cols].copy()

        df_final_encoded = pd.concat([df_encoded_numerical, df_encoded_categorical], axis=1)

        X_aligned = pd.DataFrame(0, index=df_final_encoded.index, columns=training_features)
        for col in X_aligned.columns:
            if col in df_final_encoded.columns:
                X_aligned[col] = df_final_encoded[col]
        X_aligned.columns = X_aligned.columns.astype(str)

        return X_aligned

    def _prepare_and_train_model(self):
        self.prepare_model_button.config(state=tk.DISABLED)
        self.predict_button.config(state=tk.DISABLED)
        self.show_stock_button.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Preparing data and training model...\n")
        self.update_idletasks()

        try:
            X_train, y_train, _imputation_means, _imputation_modes, _all_categories = self._load_and_prepare_data()

            if X_train is None:
                messagebox.showerror("Initialization Error", "Data loading failed. Check console for details.")
                self.prepare_model_button.config(state=tk.NORMAL)
                return

            self.imputation_means = _imputation_means
            self.imputation_modes = _imputation_modes
            self.all_categories = _all_categories

            self.model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            X_train_eval, X_test_eval, y_train_eval, y_test_eval = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
            self.model.fit(X_train_eval, y_train_eval)
            y_pred_eval = self.model.predict(X_test_eval)
            mae_eval = mean_absolute_error(y_test_eval, y_pred_eval)
            r2_eval = r2_score(y_test_eval, y_pred_eval)

            self.X_train_cols = X_train.columns.tolist()

            self.output_text.insert(tk.END, "Model trained successfully!\n")
            self.output_text.insert(tk.END, f"MAE on evaluation test set: {mae_eval:.2f}\n")
            self.output_text.insert(tk.END, f"R2 on evaluation test set: {r2_eval:.2f}\n")
            messagebox.showinfo("Success", "Model prepared and trained!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during model preparation: {e}")
            self.output_text.insert(tk.END, f"Error: {e}\n")
        finally:
            self.prepare_model_button.config(state=tk.NORMAL)
            self.predict_button.config(state=tk.NORMAL)
            self.show_stock_button.config(state=tk.NORMAL)

    def _run_forecasting_and_stock(self):
        if self.model is None:
            messagebox.showwarning("Model Not Prepared", "Please click 'Prepare & Train Model' first!")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Running sales forecasting and stock calculations...\n")

        try:
            df_forecast_raw = pd.read_csv(TEST_DATA_PATH)
            self.output_text.insert(tk.END, "Test data for forecasting loaded successfully.\n")

            X_forecast_future_year = self._prepare_forecast_data(
                df_forecast_raw, self.X_train_cols, FUTURE_PREDICTION_YEAR,
                self.imputation_means, self.imputation_modes, self.all_categories
            )

            forecasted_sales_future_year = self.model.predict(X_forecast_future_year)

            df_predictions_future_year = df_forecast_raw.copy()
            df_predictions_future_year["Predicted_Item_Outlet_Sales"] = forecasted_sales_future_year

            total_future_year_sales = df_predictions_future_year['Predicted_Item_Outlet_Sales'].sum()
            self.output_text.insert(tk.END, f"\n--- Total Forecasted Sales for {FUTURE_PREDICTION_YEAR}: Rs.{total_future_year_sales:,.2f} ---\n")

            self.output_text.insert(tk.END, "\n--- Forecasted Sales by Item Type ---\n")
            forecast_by_item_type = df_predictions_future_year.groupby('Item_Type')['Predicted_Item_Outlet_Sales'].sum().sort_values(ascending=False)
            for item_type, sales in forecast_by_item_type.items():
                self.output_text.insert(tk.END, f"{item_type:<25} Rs.{sales:,.2f}\n")

            self.output_text.insert(tk.END, "\n--- Forecasted Sales by Outlet Type ---\n")
            forecast_by_outlet_type = df_predictions_future_year.groupby('Outlet_Type')['Predicted_Item_Outlet_Sales'].sum().sort_values(ascending=False)
            for outlet_type, sales in forecast_by_outlet_type.items():
                self.output_text.insert(tk.END, f"{outlet_type:<25} Rs.{sales:,.2f}\n")

            # --- Stock Calculation ---
            self.df_stock_recommendations_global = df_predictions_future_year[[
                'Item_Identifier', 'Outlet_Identifier', 'Predicted_Item_Outlet_Sales'
            ]].copy()

            self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales'] = np.round(
                self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales']
            ).astype(int)
            self.df_stock_recommendations_global.loc[self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales'] < 0, 'Predicted_Item_Outlet_Sales'] = 0

            self.df_stock_recommendations_global['Avg_Daily_Sales'] = self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales'] / FORECAST_PERIOD_DAYS
            self.df_stock_recommendations_global['Safety_Stock_Units'] = np.round(
                self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales'] * SAFETY_STOCK_PERCENT
            ).astype(int)
            self.df_stock_recommendations_global['Demand_During_Lead_Time'] = np.round(
                self.df_stock_recommendations_global['Avg_Daily_Sales'] * LEAD_TIME_DAYS
            ).astype(int)
            self.df_stock_recommendations_global['Reorder_Point'] = self.df_stock_recommendations_global['Demand_During_Lead_Time'] + self.df_stock_recommendations_global['Safety_Stock_Units']
            self.df_stock_recommendations_global['Recommended_Order_Quantity'] = self.df_stock_recommendations_global['Predicted_Item_Outlet_Sales'] + self.df_stock_recommendations_global['Safety_Stock_Units']

            self.output_text.insert(tk.END, "\n--- Stock Calculation Summary ---\n")
            self.output_text.insert(tk.END, f"Total Recommended Stock Quantity: {self.df_stock_recommendations_global['Recommended_Order_Quantity'].sum():,.0f} units\n")
            self.output_text.insert(tk.END, "\nDetailed stock recommendations can be viewed by clicking 'Show Detailed Stock'.\n")
            messagebox.showinfo("Forecasting Complete", "Sales forecasting and stock calculations finished!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during forecasting: {e}")
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def _show_detailed_stock(self):
        if self.df_stock_recommendations_global is None or self.df_stock_recommendations_global.empty:
            messagebox.showwarning("No Data", "Please run 'Generate Forecast & Stock' first to get stock recommendations.")
            return

        stock_window = tk.Toplevel(self)
        stock_window.title("Detailed Stock Recommendations")
        stock_window.geometry("800x600")

        tree_frame = ttk.Frame(stock_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = list(self.df_stock_recommendations_global.columns)
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        for index, row in self.df_stock_recommendations_global.iterrows():
            tree.insert("", tk.END, values=list(row))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        def save_stock_data():
            try:
                self.df_stock_recommendations_global.to_csv("detailed_stock_recommendations.csv", index=False)
                messagebox.showinfo("Saved", "Detailed stock recommendations saved to detailed_stock_recommendations.csv")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save stock data: {e}")

        save_button = ttk.Button(stock_window, text="Save to CSV", command=save_stock_data)
        save_button.pack(pady=5)


