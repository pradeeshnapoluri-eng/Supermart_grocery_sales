import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("grocery_sales.csv")

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

before = len(df)
df.dropna(inplace=True)
after = len(df)
print("Rows before dropna:", before)
print("Rows after dropna:", after)

df.columns = df.columns.str.strip()
print("Cleaned column names:", df.columns.tolist())

df.drop_duplicates(inplace=True)
print("Shape after dropping duplicates:", df.shape)

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
print("Order Date dtype:", df["Order Date"].dtype)

df["Sales"]    = pd.to_numeric(df["Sales"],    errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
df["Profit"]   = pd.to_numeric(df["Profit"],   errors="coerce")

df.dropna(subset=["Sales", "Discount", "Profit", "Order Date"], inplace=True)
print("Shape after fixing numeric columns:", df.shape)

df["Order Day"]   = df["Order Date"].dt.day
df["Order Month"] = df["Order Date"].dt.month
df["Order Year"]  = df["Order Date"].dt.year
df["month_no"]    = df["Order Date"].dt.month
df["Month"]       = df["Order Date"].dt.strftime("%B")
df["year"]        = df["Order Date"].dt.year
print("Added columns: Order Day, Order Month, Order Year, month_no, Month, year")

df["Profit Margin"] = round((df["Profit"] / df["Sales"]) * 100, 2)
print("Added column: Profit Margin")

df["Discount Amount"] = round(df["Sales"] * df["Discount"], 2)
print("Added column: Discount Amount")

df["Sales Per Unit"] = round(df["Sales"] / (1 - df["Discount"].replace(1, np.nan)), 2)
df["Sales Per Unit"].fillna(df["Sales"], inplace=True)
print("Added column: Sales Per Unit")

print("\nCategory values:")
print(df["Category"].unique())

print("\nRegion values:")
print(df["Region"].unique())

print("\nYear values:")
print(df["year"].unique())

print("\nFinal Shape:", df.shape)
print("\nFinal Column List:")
print(df.columns.tolist())

print("\nStatistics:")
print(df.describe())

print("\nDuplicate rows:", df.duplicated().sum())
print("Missing values:", df.isnull().sum().sum())

df.to_csv("grocery_sales_cleaned.csv", index=False)
print("Saved: grocery_sales_cleaned.csv")
print("Data cleaning complete!")