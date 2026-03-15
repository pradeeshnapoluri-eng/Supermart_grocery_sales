from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

CSV_PATH = "grocery_sales_cleaned.csv"
ML_PATH  = "ml_model_results.csv"

def load_data():
    df = pd.read_csv(CSV_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values("Order Date").reset_index(drop=True)
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/summary")
def summary():
    try:
        df = load_data()
        return jsonify({
            "total_orders"  : int(len(df)),
            "total_sales"   : round(float(df["Sales"].sum()),    2),
            "total_profit"  : round(float(df["Profit"].sum()),   2),
            "avg_sales"     : round(float(df["Sales"].mean()),   2),
            "avg_profit"    : round(float(df["Profit"].mean()),  2),
            "avg_discount"  : round(float(df["Discount"].mean()), 4),
            "total_cities"  : int(df["City"].nunique()),
            "total_cats"    : int(df["Category"].nunique())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/category_sales")
def category_sales():
    try:
        df     = load_data()
        result = df.groupby("Category").agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count"),
            avg_sales    = ("Sales",    "mean"),
            avg_profit   = ("Profit",   "mean"),
            avg_discount = ("Discount", "mean")
        ).round(2).reset_index()
        result = result.sort_values("total_sales", ascending=False)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/region_sales")
def region_sales():
    try:
        df     = load_data()
        result = df.groupby("Region").agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count"),
            avg_sales    = ("Sales",    "mean")
        ).round(2).reset_index()
        result = result.sort_values("total_sales", ascending=False)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/yearly_sales")
def yearly_sales():
    try:
        df     = load_data()
        result = df.groupby("year").agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count"),
            avg_sales    = ("Sales",    "mean")
        ).round(2).reset_index()
        result["year"] = result["year"].astype(int)
        result = result.sort_values("year")
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/monthly_sales")
def monthly_sales():
    try:
        df     = load_data()
        result = df.groupby(["month_no", "Month"]).agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count")
        ).round(2).reset_index()
        result["month_no"] = result["month_no"].astype(int)
        result = result.sort_values("month_no")
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/top_cities")
def top_cities():
    try:
        df     = load_data()
        result = df.groupby("City").agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count")
        ).round(2).reset_index()
        result = result.sort_values("total_sales", ascending=False).head(10)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/subcategory_sales")
def subcategory_sales():
    try:
        df     = load_data()
        result = df.groupby("Sub Category").agg(
            total_sales  = ("Sales",    "sum"),
            total_profit = ("Profit",   "sum"),
            total_orders = ("Order ID", "count")
        ).round(2).reset_index()
        result = result.sort_values("total_sales", ascending=False).head(10)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/discount_analysis")
def discount_analysis():
    try:
        df = load_data()
        if "Profit Margin" not in df.columns:
            df["Profit Margin"] = (df["Profit"] / df["Sales"].replace(0, np.nan)) * 100
        result = df.groupby("Category").agg(
            avg_discount      = ("Discount",      "mean"),
            avg_profit_margin = ("Profit Margin", "mean"),
            total_sales       = ("Sales",         "sum"),
            total_profit      = ("Profit",        "sum")
        ).round(4).reset_index()
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/profit_rate")
def profit_rate():
    try:
        df     = load_data()
        result = []
        for cat in df["Category"].unique():
            subset     = df[df["Category"] == cat]
            total      = len(subset)
            profitable = int((subset["Profit"] > 0).sum())
            loss       = int((subset["Profit"] < 0).sum())
            rate       = round(profitable / total * 100, 2) if total > 0 else 0
            result.append({
                "category"          : cat,
                "profitable_orders" : profitable,
                "loss_orders"       : loss,
                "total_orders"      : total,
                "profit_rate_pct"   : rate
            })
        result = sorted(result, key=lambda x: x["profit_rate_pct"], reverse=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/top_customers")
def top_customers():
    try:
        df     = load_data()
        result = df.groupby("Customer Name").agg(
            total_orders    = ("Order ID", "count"),
            total_sales     = ("Sales",    "sum"),
            total_profit    = ("Profit",   "sum"),
            avg_order_value = ("Sales",    "mean")
        ).round(2).reset_index()
        result = result.sort_values("total_sales", ascending=False).head(15)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sales_over_time")
def sales_over_time():
    try:
        df     = load_data()
        result = df.groupby("Order Date").agg(
            total_sales  = ("Sales",  "sum"),
            total_profit = ("Profit", "sum")
        ).round(2).reset_index()
        result["Order Date"] = result["Order Date"].dt.strftime("%Y-%m-%d")
        return jsonify({
            "dates"  : result["Order Date"].tolist(),
            "sales"  : result["total_sales"].tolist(),
            "profit" : result["total_profit"].tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ml_results")
def ml_results():
    try:
        if not os.path.exists(ML_PATH):
            return jsonify({"error": "ml_model_results.csv not found — run predict_sales.py first"}), 404
        ml = pd.read_csv(ML_PATH)
        return jsonify(ml.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/loss_orders")
def loss_orders():
    try:
        df   = load_data()
        loss = df[df["Profit"] < 0].copy()
        loss = loss.sort_values("Profit", ascending=True).head(20)
        cols = ["Order ID", "Customer Name", "Category", "City", "Sales", "Profit"]
        return jsonify(loss[cols].round(2).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/yearly_category")
def yearly_category():
    try:
        df     = load_data()
        result = df.groupby(["year", "Category"]).agg(
            total_sales  = ("Sales",  "sum"),
            total_profit = ("Profit", "sum")
        ).round(2).reset_index()
        result["year"] = result["year"].astype(int)
        return jsonify(result.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Checking required files...")
    if not os.path.exists(CSV_PATH):
        print("ERROR: " + CSV_PATH + " not found — run clean_data.py first")
    else:
        print("OK: " + CSV_PATH + " found")
    if not os.path.exists(ML_PATH):
        print("WARNING: " + ML_PATH + " not found — run predict_sales.py first")
    else:
        print("OK: " + ML_PATH + " found")
    print("Starting Flask server...")
    app.run(debug=True, port=5000)