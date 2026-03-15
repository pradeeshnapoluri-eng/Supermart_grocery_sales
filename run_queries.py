import sqlite3
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

conn = sqlite3.connect("grocery_sales.db")

df = pd.read_csv("grocery_sales_cleaned.csv")
df.columns = df.columns.str.replace(" ", "_")
df.to_sql("grocery_sales", conn, if_exists="replace", index=False)

print("Database created: grocery_sales.db")
print("Total rows loaded:", len(df))
print("Columns:", df.columns.tolist())

with open("sales_queries.sql", "r") as f:
    sql = f.read()

queries = [q.strip() for q in sql.split(";") if q.strip()]

print("\nTotal queries found:", len(queries))
print("=" * 50)

results = {}

for i, query in enumerate(queries):
    try:
        result = pd.read_sql_query(query, conn)
        query_preview = query[:60].replace("\n", " ")
        print("\nQuery", i + 1, ":", query_preview)
        print(result)
        print("-" * 50)
        results[i] = result
    except Exception as e:
        print("Query", i + 1, "skipped:", str(e))

print("=" * 50)
print("Saving key query results...")

try:
    overall_stats = pd.read_sql_query("""
        SELECT
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            ROUND(AVG(Sales), 2)   AS avg_sales,
            ROUND(AVG(Profit), 2)  AS avg_profit,
            ROUND(AVG(Discount), 2) AS avg_discount,
            ROUND(MIN(Sales), 2)   AS min_sales,
            ROUND(MAX(Sales), 2)   AS max_sales
        FROM grocery_sales
    """, conn)
    overall_stats.to_csv("sql_overall_stats.csv", index=False)
    print("Saved: sql_overall_stats.csv")
except Exception as e:
    print("Error saving overall stats:", str(e))

try:
    category_stats = pd.read_sql_query("""
        SELECT
            Category,
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            ROUND(AVG(Sales), 2)   AS avg_sales,
            ROUND(AVG(Profit), 2)  AS avg_profit
        FROM grocery_sales
        GROUP BY Category
        ORDER BY total_sales DESC
    """, conn)
    category_stats.to_csv("sql_category_stats.csv", index=False)
    print("Saved: sql_category_stats.csv")
except Exception as e:
    print("Error saving category stats:", str(e))

try:
    region_stats = pd.read_sql_query("""
        SELECT
            Region,
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            ROUND(AVG(Sales), 2)   AS avg_sales
        FROM grocery_sales
        GROUP BY Region
        ORDER BY total_sales DESC
    """, conn)
    region_stats.to_csv("sql_region_stats.csv", index=False)
    print("Saved: sql_region_stats.csv")
except Exception as e:
    print("Error saving region stats:", str(e))

try:
    yearly_stats = pd.read_sql_query("""
        SELECT
            year,
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            ROUND(AVG(Sales), 2)   AS avg_sales
        FROM grocery_sales
        GROUP BY year
        ORDER BY year
    """, conn)
    yearly_stats.to_csv("sql_yearly_stats.csv", index=False)
    print("Saved: sql_yearly_stats.csv")
except Exception as e:
    print("Error saving yearly stats:", str(e))

try:
    monthly_stats = pd.read_sql_query("""
        SELECT
            month_no,
            Month,
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit
        FROM grocery_sales
        GROUP BY month_no, Month
        ORDER BY month_no
    """, conn)
    monthly_stats.to_csv("sql_monthly_stats.csv", index=False)
    print("Saved: sql_monthly_stats.csv")
except Exception as e:
    print("Error saving monthly stats:", str(e))

try:
    top_cities = pd.read_sql_query("""
        SELECT
            City,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            COUNT(*)               AS total_orders
        FROM grocery_sales
        GROUP BY City
        ORDER BY total_sales DESC
        LIMIT 10
    """, conn)
    top_cities.to_csv("sql_top_cities.csv", index=False)
    print("Saved: sql_top_cities.csv")
except Exception as e:
    print("Error saving top cities:", str(e))

try:
    loss_orders = pd.read_sql_query("""
        SELECT
            Order_ID,
            Customer_Name,
            Category,
            City,
            ROUND(Sales, 2)  AS sales,
            ROUND(Profit, 2) AS profit
        FROM grocery_sales
        WHERE Profit < 0
        ORDER BY Profit ASC
    """, conn)
    loss_orders.to_csv("sql_loss_orders.csv", index=False)
    print("Saved: sql_loss_orders.csv")
except Exception as e:
    print("Error saving loss orders:", str(e))

try:
    top_customers = pd.read_sql_query("""
        SELECT
            Customer_Name,
            COUNT(*)               AS total_orders,
            ROUND(SUM(Sales), 2)   AS total_sales,
            ROUND(SUM(Profit), 2)  AS total_profit,
            ROUND(AVG(Sales), 2)   AS avg_order_value
        FROM grocery_sales
        GROUP BY Customer_Name
        ORDER BY total_sales DESC
        LIMIT 15
    """, conn)
    top_customers.to_csv("sql_top_customers.csv", index=False)
    print("Saved: sql_top_customers.csv")
except Exception as e:
    print("Error saving top customers:", str(e))

try:
    profit_rate = pd.read_sql_query("""
        SELECT
            Category,
            SUM(CASE WHEN Profit > 0 THEN 1 ELSE 0 END) AS profitable_orders,
            SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS loss_orders,
            COUNT(*)                                      AS total_orders,
            ROUND(
                SUM(CASE WHEN Profit > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
            ) AS profit_rate_pct
        FROM grocery_sales
        GROUP BY Category
        ORDER BY profit_rate_pct DESC
    """, conn)
    profit_rate.to_csv("sql_profit_rate.csv", index=False)
    print("Saved: sql_profit_rate.csv")
except Exception as e:
    print("Error saving profit rate:", str(e))

conn.close()
print("\nDatabase connection closed!")
print("SQL analysis complete!")