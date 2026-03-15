import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("grocery_sales_cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df = df.sort_values("Order Date").reset_index(drop=True)

corr_df      = pd.read_csv("correlation_matrix.csv", index_col=0)
cat_summary  = pd.read_csv("category_summary.csv")
reg_summary  = pd.read_csv("region_summary.csv")
monthly_df   = pd.read_csv("monthly_sales.csv")
top_cities   = pd.read_csv("top_cities.csv")

COLORS = ["#2e86ab", "#a23b72", "#f18f01", "#c73e1d", "#3b1f2b", "#44bba4", "#e94f37"]

print("Data loaded successfully!")
print("Shape:", df.shape)

print("Plotting chart 1 - Sales by Category...")
plt.figure(figsize=(12, 6))
bars = plt.bar(cat_summary["Category"], cat_summary["total_sales"], color=COLORS, edgecolor="black", alpha=0.85)
plt.title("Total Sales by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=30, ha="right")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f"{int(bar.get_height()):,}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("plot_sales_by_category.png", dpi=150)
plt.close()
print("Saved: plot_sales_by_category.png")

print("Plotting chart 2 - Profit by Category...")
plt.figure(figsize=(12, 6))
bars = plt.bar(cat_summary["Category"], cat_summary["total_profit"], color=COLORS, edgecolor="black", alpha=0.85)
plt.title("Total Profit by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=30, ha="right")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
             f"{int(bar.get_height()):,}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("plot_profit_by_category.png", dpi=150)
plt.close()
print("Saved: plot_profit_by_category.png")

print("Plotting chart 3 - Sales by Region...")
plt.figure(figsize=(8, 6))
bars = plt.bar(reg_summary["Region"], reg_summary["total_sales"],
               color=["#2e86ab", "#f18f01", "#44bba4", "#e94f37"], edgecolor="black", alpha=0.85)
plt.title("Total Sales by Region", fontsize=14, fontweight="bold")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
             f"{int(bar.get_height()):,}", ha="center", va="bottom", fontsize=10)
plt.tight_layout()
plt.savefig("plot_sales_by_region.png", dpi=150)
plt.close()
print("Saved: plot_sales_by_region.png")

print("Plotting chart 4 - Sales by Year Pie Chart...")
yearly_sales = df.groupby("year")["Sales"].sum()
plt.figure(figsize=(8, 8))
plt.pie(yearly_sales, labels=yearly_sales.index, autopct="%1.1f%%",
        colors=["#2e86ab", "#f18f01", "#44bba4", "#e94f37"],
        startangle=140, wedgeprops=dict(edgecolor="white", linewidth=2))
plt.title("Sales Distribution by Year", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_sales_by_year.png", dpi=150)
plt.close()
print("Saved: plot_sales_by_year.png")

print("Plotting chart 5 - Monthly Sales Trend...")
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly_agg = df.groupby("month_no")["Sales"].sum().reset_index()
monthly_agg = monthly_agg.sort_values("month_no")
plt.figure(figsize=(12, 6))
plt.plot(monthly_agg["month_no"], monthly_agg["Sales"],
         marker="o", linewidth=2, color="#2e86ab", markersize=8)
plt.fill_between(monthly_agg["month_no"], monthly_agg["Sales"], alpha=0.2, color="#2e86ab")
plt.title("Total Sales by Month", fontsize=14, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(range(1, 13), month_names)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_monthly_sales.png", dpi=150)
plt.close()
print("Saved: plot_monthly_sales.png")

print("Plotting chart 6 - Top 10 Cities by Sales...")
top10_cities = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
bars = plt.bar(top10_cities.index, top10_cities.values,
               color="#2e86ab", edgecolor="black", alpha=0.85)
plt.title("Top 10 Cities by Sales", fontsize=14, fontweight="bold")
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.xticks(rotation=45, ha="right")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
             f"{int(bar.get_height()):,}", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
plt.savefig("plot_top_cities.png", dpi=150)
plt.close()
print("Saved: plot_top_cities.png")

print("Plotting chart 7 - Sales Distribution Boxplot by Category...")
plt.figure(figsize=(12, 6))
categories = df["Category"].unique()
data_to_plot = [df[df["Category"] == cat]["Sales"].values for cat in categories]
bp = plt.boxplot(data_to_plot, labels=categories, patch_artist=True,
                 medianprops=dict(color="black", linewidth=2))
for patch, color in zip(bp["boxes"], COLORS):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
plt.title("Sales Distribution by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=30, ha="right")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
plt.tight_layout()
plt.savefig("plot_sales_boxplot.png", dpi=150)
plt.close()
print("Saved: plot_sales_boxplot.png")

print("Plotting chart 8 - Correlation Heatmap...")
plt.figure(figsize=(8, 6))
sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".3f",
            linewidths=0.5, square=True, annot_kws={"size": 11})
plt.title("Correlation Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_correlation_heatmap.png", dpi=150)
plt.close()
print("Saved: plot_correlation_heatmap.png")

print("Plotting chart 9 - Sales vs Profit Scatter...")
plt.figure(figsize=(10, 6))
for i, cat in enumerate(df["Category"].unique()):
    subset = df[df["Category"] == cat]
    plt.scatter(subset["Sales"], subset["Profit"],
                label=cat, alpha=0.5, s=30, color=COLORS[i % len(COLORS)])
plt.title("Sales vs Profit by Category", fontsize=14, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.legend(fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
plt.axhline(y=0, color="black", linewidth=1)
plt.tight_layout()
plt.savefig("plot_sales_vs_profit.png", dpi=150)
plt.close()
print("Saved: plot_sales_vs_profit.png")

print("Plotting chart 10 - Discount vs Profit Scatter...")
plt.figure(figsize=(10, 6))
plt.scatter(df["Discount"], df["Profit"], alpha=0.4, color="#2e86ab", s=20)
plt.title("Discount vs Profit", fontsize=14, fontweight="bold")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.grid(True, linestyle="--", alpha=0.4)
plt.axhline(y=0, color="red", linewidth=1, linestyle="--")
plt.tight_layout()
plt.savefig("plot_discount_vs_profit.png", dpi=150)
plt.close()
print("Saved: plot_discount_vs_profit.png")

print("Plotting chart 11 - Profit Margin by Category...")
avg_margin = df.groupby("Category")["Profit Margin"].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
bars = plt.bar(avg_margin.index, avg_margin.values, color=COLORS, edgecolor="black", alpha=0.85)
plt.title("Average Profit Margin by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Avg Profit Margin (%)")
plt.xticks(rotation=30, ha="right")
plt.grid(True, linestyle="--", alpha=0.4, axis="y")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("plot_profit_margin.png", dpi=150)
plt.close()
print("Saved: plot_profit_margin.png")

print("Plotting chart 12 - Yearly Sales Trend...")
yearly_trend = df.groupby("year")["Sales"].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(yearly_trend["year"], yearly_trend["Sales"],
         marker="o", linewidth=2.5, color="#f18f01", markersize=10)
plt.fill_between(yearly_trend["year"], yearly_trend["Sales"], alpha=0.2, color="#f18f01")
for i, row in yearly_trend.iterrows():
    plt.text(row["year"], row["Sales"] + 10000, f"{int(row['Sales']):,}",
             ha="center", fontsize=10, fontweight="bold")
plt.title("Yearly Sales Trend", fontsize=14, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.xticks(yearly_trend["year"])
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_yearly_trend.png", dpi=150)
plt.close()
print("Saved: plot_yearly_trend.png")

print("Plotting chart 13 - Sub Category Sales Top 10...")
top_subcat = df.groupby("Sub Category")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.barh(top_subcat.index, top_subcat.values, color="#44bba4", edgecolor="black", alpha=0.85)
plt.title("Top 10 Sub Categories by Sales", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales")
plt.gca().invert_yaxis()
plt.grid(True, linestyle="--", alpha=0.4, axis="x")
plt.tight_layout()
plt.savefig("plot_subcat_sales.png", dpi=150)
plt.close()
print("Saved: plot_subcat_sales.png")

print("Plotting chart 14 - Region Profit Pie Chart...")
region_profit = df.groupby("Region")["Profit"].sum()
plt.figure(figsize=(8, 8))
plt.pie(region_profit, labels=region_profit.index, autopct="%1.1f%%",
        colors=["#2e86ab", "#f18f01", "#44bba4", "#e94f37"],
        startangle=140, wedgeprops=dict(edgecolor="white", linewidth=2))
plt.title("Profit Distribution by Region", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_region_profit_pie.png", dpi=150)
plt.close()
print("Saved: plot_region_profit_pie.png")

print("Plotting chart 15 - Sales Over Time Line Chart...")
sales_over_time = df.groupby("Order Date")["Sales"].sum().reset_index()
plt.figure(figsize=(14, 6))
plt.plot(sales_over_time["Order Date"], sales_over_time["Sales"],
         linewidth=1.5, color="#2e86ab", alpha=0.8)
plt.title("Total Sales Over Time (2015 - 2018)", fontsize=14, fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Daily Sales")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gcf().autofmt_xdate()
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("plot_sales_over_time.png", dpi=150)
plt.close()
print("Saved: plot_sales_over_time.png")

print("\nAll charts saved successfully!")
print("Total charts saved: 15")