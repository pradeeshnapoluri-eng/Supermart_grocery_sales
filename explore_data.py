import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("grocery_sales_cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df = df.sort_values("Order Date").reset_index(drop=True)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("=" * 50)
print("Step 1: Basic Statistics")
print("=" * 50)
print(df.describe())

print("=" * 50)
print("Step 2: Sales by Category")
print("=" * 50)
sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print(sales_by_category)

print("=" * 50)
print("Step 3: Profit by Category")
print("=" * 50)
profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print(profit_by_category)

print("=" * 50)
print("Step 4: Sales by Region")
print("=" * 50)
sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print(sales_by_region)

print("=" * 50)
print("Step 5: Profit by Region")
print("=" * 50)
profit_by_region = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
print(profit_by_region)

print("=" * 50)
print("Step 6: Sales by Year")
print("=" * 50)
sales_by_year = df.groupby("year")["Sales"].sum().sort_values(ascending=False)
print(sales_by_year)

print("=" * 50)
print("Step 7: Sales by Month")
print("=" * 50)
sales_by_month = df.groupby("month_no")["Sales"].sum().reset_index()
sales_by_month = sales_by_month.sort_values("month_no")
print(sales_by_month)

print("=" * 50)
print("Step 8: Top 10 Cities by Sales")
print("=" * 50)
top_cities = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10)
print(top_cities)

print("=" * 50)
print("Step 9: Top 10 Cities by Profit")
print("=" * 50)
top_cities_profit = df.groupby("City")["Profit"].sum().sort_values(ascending=False).head(10)
print(top_cities_profit)

print("=" * 50)
print("Step 10: Sales by Sub Category")
print("=" * 50)
sales_by_subcat = df.groupby("Sub Category")["Sales"].sum().sort_values(ascending=False)
print(sales_by_subcat)

print("=" * 50)
print("Step 11: Profit by Sub Category")
print("=" * 50)
profit_by_subcat = df.groupby("Sub Category")["Profit"].sum().sort_values(ascending=False)
print(profit_by_subcat)

print("=" * 50)
print("Step 12: Average Discount by Category")
print("=" * 50)
avg_discount = df.groupby("Category")["Discount"].mean().sort_values(ascending=False)
print(avg_discount)

print("=" * 50)
print("Step 13: Average Profit Margin by Category")
print("=" * 50)
avg_margin = df.groupby("Category")["Profit Margin"].mean().sort_values(ascending=False)
print(avg_margin)

print("=" * 50)
print("Step 14: Sales and Profit by Region and Category")
print("=" * 50)
region_category = df.groupby(["Region", "Category"])[["Sales", "Profit"]].sum()
print(region_category)

print("=" * 50)
print("Step 15: Yearly Growth")
print("=" * 50)
yearly_sales = df.groupby("year")["Sales"].sum().reset_index()
yearly_sales["Growth"] = yearly_sales["Sales"].pct_change() * 100
yearly_sales["Growth"] = yearly_sales["Growth"].round(2)
print(yearly_sales)

print("=" * 50)
print("Step 16: Monthly Average Sales")
print("=" * 50)
monthly_avg = df.groupby("month_no")["Sales"].mean().reset_index()
monthly_avg.columns = ["month_no", "avg_sales"]
monthly_avg["avg_sales"] = monthly_avg["avg_sales"].round(2)
print(monthly_avg)

print("=" * 50)
print("Step 17: Order Count by Category")
print("=" * 50)
order_count = df.groupby("Category")["Order ID"].count().sort_values(ascending=False)
print(order_count)

print("=" * 50)
print("Step 18: Order Count by Region")
print("=" * 50)
order_count_region = df.groupby("Region")["Order ID"].count().sort_values(ascending=False)
print(order_count_region)

print("=" * 50)
print("Step 19: Correlation Matrix")
print("=" * 50)
numeric_cols = ["Sales", "Discount", "Profit", "Profit Margin", "Discount Amount"]
corr_matrix = df[numeric_cols].corr().round(4)
print(corr_matrix)

print("=" * 50)
print("Step 20: High Profit Orders")
print("=" * 50)
high_profit = df[df["Profit"] > df["Profit"].quantile(0.90)]
print("High profit orders count:", len(high_profit))
print(high_profit[["Order ID", "Category", "City", "Sales", "Profit"]].head(10))

print("=" * 50)
print("Step 21: Loss Making Orders")
print("=" * 50)
loss_orders = df[df["Profit"] < 0]
print("Loss making orders count:", len(loss_orders))
print(loss_orders[["Order ID", "Category", "City", "Sales", "Profit"]].head(10))

print("=" * 50)
print("Step 22: Best Performing Sub Categories")
print("=" * 50)
best_subcat = df.groupby("Sub Category").agg(
    total_sales   = ("Sales",  "sum"),
    total_profit  = ("Profit", "sum"),
    order_count   = ("Order ID", "count"),
    avg_discount  = ("Discount", "mean")
).sort_values("total_sales", ascending=False).round(2)
print(best_subcat)

corr_matrix.to_csv("correlation_matrix.csv")
print("\nSaved: correlation_matrix.csv")

summary = df.groupby("Category").agg(
    total_sales   = ("Sales",         "sum"),
    total_profit  = ("Profit",        "sum"),
    order_count   = ("Order ID",      "count"),
    avg_discount  = ("Discount",      "mean"),
    avg_margin    = ("Profit Margin", "mean")
).round(2).reset_index()
summary.to_csv("category_summary.csv", index=False)
print("Saved: category_summary.csv")

region_summary = df.groupby("Region").agg(
    total_sales  = ("Sales",    "sum"),
    total_profit = ("Profit",   "sum"),
    order_count  = ("Order ID", "count")
).round(2).reset_index()
region_summary.to_csv("region_summary.csv", index=False)
print("Saved: region_summary.csv")

monthly_sales = df.groupby(["year", "month_no", "Month"])["Sales"].sum().reset_index()
monthly_sales.to_csv("monthly_sales.csv", index=False)
print("Saved: monthly_sales.csv")

top_cities.reset_index().to_csv("top_cities.csv", index=False)
print("Saved: top_cities.csv")

print("\nEDA complete!")