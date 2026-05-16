# ================= 7_model_comparison_clean.py =================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns


# ================= LOAD DATA =================
DATA_PATH = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets\4.0nungambakkam_features.csv"
df = pd.read_csv(DATA_PATH)
print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ================= CLEAN FEATURES =================
# Drop timestamps and AQI_Category (to avoid leakage)
drop_cols = ["timestamp_unix", "timestamp_utc", "timestamp_ist", "AQI_Category"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Target
y = df["AQI"]
X = df.drop(columns=["AQI"])

# PM features
pm_features = ["pm2_5", "pm10"]

# ================= SPLIT DATA =================
# Keep same indices for all models
X_train_full, X_test_full, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Versions with and without PM
X_train_with_pm = X_train_full.copy()
X_test_with_pm = X_test_full.copy()

X_train_without_pm = X_train_full.drop(columns=pm_features)
X_test_without_pm = X_test_full.drop(columns=pm_features)

# ================= AQI CATEGORY FUNCTION =================
def aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

# ================= EVALUATION FUNCTION =================
# def evaluate_model(model, X_train, y_train, X_test, y_test, name):
#     y_pred_train = model.predict(X_train)
#     y_pred_test = model.predict(X_test)

#     rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
#     rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

#     print(f"\n📊 {name}")
#     print(f"Train -> MAE: {mean_absolute_error(y_train, y_pred_train):.2f}, "
#           f"RMSE: {rmse_train:.2f}, R2: {r2_score(y_train, y_pred_train):.2f}")
#     print(f"Test  -> MAE: {mean_absolute_error(y_test, y_pred_test):.2f}, "
#           f"RMSE: {rmse_test:.2f}, R2: {r2_score(y_test, y_pred_test):.2f}")

#     # Confusion Matrix on AQI categories
#     y_test_cat = y_test.apply(aqi_category)
#     y_pred_cat = pd.Series(y_pred_test).apply(aqi_category)

#     labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
#     cm = confusion_matrix(y_test_cat, y_pred_cat, labels=labels)
#     cm_df = pd.DataFrame(cm, index=labels, columns=labels)

#     print("🧩 Confusion Matrix:")
#     print(cm_df)
def evaluate_model(model, X_train, y_train, X_test, y_test, name):
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

    print(f"\n📊 {name}")
    print(f"Train -> MAE: {mean_absolute_error(y_train, y_pred_train):.2f}, "
          f"RMSE: {rmse_train:.2f}, R2: {r2_score(y_train, y_pred_train):.2f}")
    print(f"Test  -> MAE: {mean_absolute_error(y_test, y_pred_test):.2f}, "
          f"RMSE: {rmse_test:.2f}, R2: {r2_score(y_test, y_pred_test):.2f}")

    # ================= AQI CATEGORY =================
    y_test_cat = y_test.apply(aqi_category)
    y_pred_cat = pd.Series(y_pred_test).apply(aqi_category)

    # ✅ ACCURACY
    acc = accuracy_score(y_test_cat, y_pred_cat)
    print(f"🎯 AQI Category Accuracy (Test): {acc*100:.2f}%")

    # ================= CONFUSION MATRIX =================
    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    cm = confusion_matrix(y_test_cat, y_pred_cat, labels=labels)

    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print("🧩 Confusion Matrix:")
    print(cm_df)

    # ================= PLOT ONLY =================
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix – {name}")
    plt.xlabel("Predicted AQI Category")
    plt.ylabel("Actual AQI Category")
    plt.tight_layout()
    plt.show()


# ================= RANDOM FOREST MODELS =================
print("\n🌲 Training Random Forest models...")

rf_with_pm = RandomForestRegressor(n_estimators=200, random_state=42)
rf_with_pm.fit(X_train_with_pm, y_train)

rf_without_pm = RandomForestRegressor(n_estimators=200, random_state=42)
rf_without_pm.fit(X_train_without_pm, y_train)

# Save models (optional)
joblib.dump(rf_with_pm, "rf_model_with_pm_no_aqi_category.pkl")
joblib.dump(rf_without_pm, "rf_model_without_pm_no_aqi_category.pkl")

# Evaluate RF models
evaluate_model(rf_with_pm, X_train_with_pm, y_train, X_test_with_pm, y_test, "RF with PM")
evaluate_model(rf_without_pm, X_train_without_pm, y_train, X_test_without_pm, y_test, "RF without PM")

# ================= GRADIENT BOOSTING MODELS =================
print("\n⚡ Training Gradient Boosting models with median imputer...")

def train_gb_pipeline():
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("gb", GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        ))
    ])

# GB with PM
gb_with_pm = train_gb_pipeline()
gb_with_pm.fit(X_train_with_pm, y_train)

# GB without PM
gb_without_pm = train_gb_pipeline()
gb_without_pm.fit(X_train_without_pm, y_train)

# Evaluate GB models
evaluate_model(gb_with_pm, X_train_with_pm, y_train, X_test_with_pm, y_test, "GB with PM")
evaluate_model(gb_without_pm, X_train_without_pm, y_train, X_test_without_pm, y_test, "GB without PM")


