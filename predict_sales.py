import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

df = pd.read_csv("grocery_sales_cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

le = LabelEncoder()

df["Category_enc"]    = le.fit_transform(df["Category"])
df["Sub_Cat_enc"]     = le.fit_transform(df["Sub Category"])
df["City_enc"]        = le.fit_transform(df["City"])
df["Region_enc"]      = le.fit_transform(df["Region"])
df["State_enc"]       = le.fit_transform(df["State"])
df["Month_enc"]       = le.fit_transform(df["Month"])

print("Label encoding done!")

feature_cols = [
    "Category_enc",
    "Sub_Cat_enc",
    "City_enc",
    "Region_enc",
    "State_enc",
    "Month_enc",
    "month_no",
    "year",
    "Order Day",
    "Order Month",
    "Order Year",
    "Discount",
    "Profit",
    "Profit Margin",
    "Discount Amount"
]

X = df[feature_cols]
y = df["Sales"]

print("Features shape:", X.shape)
print("Target shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size :", len(X_test))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("=" * 50)
print("Training Linear Regression...")
print("=" * 50)

lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)

lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
lr_mae  = mean_absolute_error(y_test, lr_pred)
lr_r2   = r2_score(y_test, lr_pred)

print("Linear Regression Results:")
print("RMSE :", round(lr_rmse, 4))
print("MAE  :", round(lr_mae,  4))
print("R2   :", round(lr_r2,   4))

print("=" * 50)
print("Training Random Forest...")
print("=" * 50)

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_mae  = mean_absolute_error(y_test, rf_pred)
rf_r2   = r2_score(y_test, rf_pred)

print("Random Forest Results:")
print("RMSE :", round(rf_rmse, 4))
print("MAE  :", round(rf_mae,  4))
print("R2   :", round(rf_r2,   4))

print("=" * 50)
print("Training XGBoost...")
print("=" * 50)

xgb = XGBRegressor(n_estimators=100, learning_rate=0.1,
                   max_depth=6, random_state=42, verbosity=0)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)

xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
xgb_mae  = mean_absolute_error(y_test, xgb_pred)
xgb_r2   = r2_score(y_test, xgb_pred)

print("XGBoost Results:")
print("RMSE :", round(xgb_rmse, 4))
print("MAE  :", round(xgb_mae,  4))
print("R2   :", round(xgb_r2,   4))

print("=" * 50)
print("Model Comparison Summary")
print("=" * 50)

results = pd.DataFrame({
    "Model" : ["Linear Regression", "Random Forest", "XGBoost"],
    "RMSE"  : [round(lr_rmse, 4), round(rf_rmse, 4), round(xgb_rmse, 4)],
    "MAE"   : [round(lr_mae,  4), round(rf_mae,  4), round(xgb_mae,  4)],
    "R2"    : [round(lr_r2,   4), round(rf_r2,   4), round(xgb_r2,   4)]
})
print(results.to_string(index=False))

results.to_csv("ml_model_results.csv", index=False)
print("Saved: ml_model_results.csv")

print("Plotting Actual vs Predicted - Linear Regression...")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, lr_pred, alpha=0.4, color="#2e86ab", s=20)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], color="red", linewidth=2)
plt.title("Linear Regression - Actual vs Predicted Sales")
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("plot_lr_actual_vs_predicted.png", dpi=150)
plt.close()
print("Saved: plot_lr_actual_vs_predicted.png")

print("Plotting Actual vs Predicted - Random Forest...")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, rf_pred, alpha=0.4, color="#44bba4", s=20)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], color="red", linewidth=2)
plt.title("Random Forest - Actual vs Predicted Sales")
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("plot_rf_actual_vs_predicted.png", dpi=150)
plt.close()
print("Saved: plot_rf_actual_vs_predicted.png")

print("Plotting Actual vs Predicted - XGBoost...")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, xgb_pred, alpha=0.4, color="#f18f01", s=20)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()], color="red", linewidth=2)
plt.title("XGBoost - Actual vs Predicted Sales")
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("plot_xgb_actual_vs_predicted.png", dpi=150)
plt.close()
print("Saved: plot_xgb_actual_vs_predicted.png")

print("Plotting Feature Importance - Random Forest...")
rf_importance = pd.DataFrame({
    "Feature"   : feature_cols,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(rf_importance["Feature"], rf_importance["Importance"],
         color="#2e86ab", edgecolor="black", alpha=0.85)
plt.title("Random Forest - Feature Importance")
plt.xlabel("Importance Score")
plt.gca().invert_yaxis()
plt.grid(True, linestyle="--", alpha=0.4, axis="x")
plt.tight_layout()
plt.savefig("plot_rf_feature_importance.png", dpi=150)
plt.close()
print("Saved: plot_rf_feature_importance.png")

print("Plotting Feature Importance - XGBoost...")
xgb_importance = pd.DataFrame({
    "Feature"   : feature_cols,
    "Importance": xgb.feature_importances_
}).sort_values("Importance", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(xgb_importance["Feature"], xgb_importance["Importance"],
         color="#f18f01", edgecolor="black", alpha=0.85)
plt.title("XGBoost - Feature Importance")
plt.xlabel("Importance Score")
plt.gca().invert_yaxis()
plt.grid(True, linestyle="--", alpha=0.4, axis="x")
plt.tight_layout()
plt.savefig("plot_xgb_feature_importance.png", dpi=150)
plt.close()
print("Saved: plot_xgb_feature_importance.png")

print("Plotting Model Comparison Chart...")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
models = results["Model"].tolist()

axes[0].bar(models, results["R2"],
            color=["#2e86ab", "#44bba4", "#f18f01"],
            edgecolor="black", alpha=0.85)
axes[0].set_title("R2 Score Comparison")
axes[0].set_ylabel("R2 Score")
axes[0].set_ylim(0, 1)
axes[0].grid(True, linestyle="--", alpha=0.4, axis="y")
for i, v in enumerate(results["R2"]):
    axes[0].text(i, v + 0.01, str(v), ha="center", fontsize=10)

axes[1].bar(models, results["RMSE"],
            color=["#2e86ab", "#44bba4", "#f18f01"],
            edgecolor="black", alpha=0.85)
axes[1].set_title("RMSE Comparison")
axes[1].set_ylabel("RMSE")
axes[1].grid(True, linestyle="--", alpha=0.4, axis="y")
for i, v in enumerate(results["RMSE"]):
    axes[1].text(i, v + 1, str(v), ha="center", fontsize=10)

axes[2].bar(models, results["MAE"],
            color=["#2e86ab", "#44bba4", "#f18f01"],
            edgecolor="black", alpha=0.85)
axes[2].set_title("MAE Comparison")
axes[2].set_ylabel("MAE")
axes[2].grid(True, linestyle="--", alpha=0.4, axis="y")
for i, v in enumerate(results["MAE"]):
    axes[2].text(i, v + 1, str(v), ha="center", fontsize=10)

plt.suptitle("Model Performance Comparison", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("plot_model_comparison.png", dpi=150)
plt.close()
print("Saved: plot_model_comparison.png")

rf_importance.to_csv("rf_feature_importance.csv", index=False)
xgb_importance.to_csv("xgb_feature_importance.csv", index=False)
print("Saved: rf_feature_importance.csv")
print("Saved: xgb_feature_importance.csv")

print("\nML model complete!")
print("Best Model by R2:", results.loc[results["R2"].idxmax(), "Model"])
print("Best R2 Score   :", results["R2"].max())