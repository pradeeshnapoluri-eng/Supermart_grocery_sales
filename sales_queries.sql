CREATE TABLE IF NOT EXISTS grocery_sales (
    Order_ID        TEXT,
    Customer_Name   TEXT,
    Category        TEXT,
    Sub_Category    TEXT,
    City            TEXT,
    Order_Date      TEXT,
    Region          TEXT,
    Sales           REAL,
    Discount        REAL,
    Profit          REAL,
    State           TEXT,
    Order_Day       INTEGER,
    Order_Month     INTEGER,
    Order_Year      INTEGER,
    month_no        INTEGER,
    Month           TEXT,
    year            INTEGER,
    Profit_Margin   REAL,
    Discount_Amount REAL,
    Sales_Per_Unit  REAL
);

SELECT COUNT(*) AS total_orders FROM grocery_sales;

SELECT DISTINCT Category FROM grocery_sales ORDER BY Category;

SELECT DISTINCT Region FROM grocery_sales ORDER BY Region;

SELECT DISTINCT year FROM grocery_sales ORDER BY year;

SELECT
    COUNT(*)            AS total_orders,
    ROUND(SUM(Sales),   2) AS total_sales,
    ROUND(SUM(Profit),  2) AS total_profit,
    ROUND(AVG(Sales),   2) AS avg_sales,
    ROUND(AVG(Profit),  2) AS avg_profit,
    ROUND(AVG(Discount),2) AS avg_discount,
    ROUND(MIN(Sales),   2) AS min_sales,
    ROUND(MAX(Sales),   2) AS max_sales
FROM grocery_sales;

SELECT
    Category,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_sales,
    ROUND(AVG(Profit), 2)  AS avg_profit
FROM grocery_sales
GROUP BY Category
ORDER BY total_sales DESC;

SELECT
    Sub_Category,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_sales
FROM grocery_sales
GROUP BY Sub_Category
ORDER BY total_sales DESC
LIMIT 15;

SELECT
    Region,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_sales,
    ROUND(AVG(Profit), 2)  AS avg_profit
FROM grocery_sales
GROUP BY Region
ORDER BY total_sales DESC;

SELECT
    year,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_sales
FROM grocery_sales
GROUP BY year
ORDER BY year;

SELECT
    month_no,
    Month,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_sales
FROM grocery_sales
GROUP BY month_no, Month
ORDER BY month_no;

SELECT
    City,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    COUNT(*)               AS total_orders
FROM grocery_sales
GROUP BY City
ORDER BY total_sales DESC
LIMIT 10;

SELECT
    City,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(SUM(Sales),  2)  AS total_sales,
    COUNT(*)               AS total_orders
FROM grocery_sales
GROUP BY City
ORDER BY total_profit DESC
LIMIT 10;

SELECT
    Category,
    ROUND(AVG(Discount),      4) AS avg_discount,
    ROUND(AVG(Profit_Margin), 2) AS avg_profit_margin,
    ROUND(SUM(Sales),         2) AS total_sales,
    ROUND(SUM(Profit),        2) AS total_profit
FROM grocery_sales
GROUP BY Category
ORDER BY avg_discount DESC;

SELECT
    Order_ID,
    Customer_Name,
    Category,
    City,
    ROUND(Sales,  2) AS sales,
    ROUND(Profit, 2) AS profit
FROM grocery_sales
WHERE Profit < 0
ORDER BY Profit ASC
LIMIT 20;

SELECT
    Category,
    COUNT(*) AS loss_orders
FROM grocery_sales
WHERE Profit < 0
GROUP BY Category
ORDER BY loss_orders DESC;

SELECT
    Order_ID,
    Customer_Name,
    Category,
    City,
    ROUND(Sales,  2) AS sales,
    ROUND(Profit, 2) AS profit
FROM grocery_sales
ORDER BY Profit DESC
LIMIT 20;

SELECT
    Region,
    Category,
    ROUND(SUM(Sales),  2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(*)              AS total_orders
FROM grocery_sales
GROUP BY Region, Category
ORDER BY Region, total_sales DESC;

SELECT
    year,
    Category,
    ROUND(SUM(Sales),  2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM grocery_sales
GROUP BY year, Category
ORDER BY year, total_sales DESC;

SELECT
    year,
    month_no,
    Month,
    ROUND(SUM(Sales),  2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(*)              AS total_orders
FROM grocery_sales
GROUP BY year, month_no, Month
ORDER BY year, month_no;

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
ORDER BY profit_rate_pct DESC;

SELECT
    Region,
    SUM(CASE WHEN Profit > 0 THEN 1 ELSE 0 END) AS profitable_orders,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS loss_orders,
    COUNT(*)                                      AS total_orders,
    ROUND(
        SUM(CASE WHEN Profit > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS profit_rate_pct
FROM grocery_sales
GROUP BY Region
ORDER BY profit_rate_pct DESC;

SELECT
    Customer_Name,
    COUNT(*)               AS total_orders,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(AVG(Sales),  2)  AS avg_order_value
FROM grocery_sales
GROUP BY Customer_Name
ORDER BY total_sales DESC
LIMIT 15;

SELECT
    Discount,
    COUNT(*)               AS total_orders,
    ROUND(AVG(Sales),  2)  AS avg_sales,
    ROUND(AVG(Profit), 2)  AS avg_profit
FROM grocery_sales
GROUP BY Discount
ORDER BY Discount;

SELECT
    Category,
    Sub_Category,
    ROUND(SUM(Sales),  2)  AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    COUNT(*)               AS total_orders
FROM grocery_sales
GROUP BY Category, Sub_Category
ORDER BY Category, total_sales DESC;