# 6gbmodeltraining.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np
import os

# ================= CONFIG =================
DATA_FILE = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets\4.0nungambakkam_features.csv"
MODEL_FOLDER = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\modelsrfgb"
os.makedirs(MODEL_FOLDER, exist_ok=True)
# ==========================================

# ================= LOAD DATA =================
df = pd.read_csv(DATA_FILE)
print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ================= FEATURES =================
# With PM features
# features_with_pm = [c for c in df.columns if c not in ["timestamp_unix", "timestamp_utc", 
#                                                       "timestamp_ist", "AQI"]]
# # Without PM features
# features_without_pm = [c for c in features_with_pm if "pm2_5" not in c and "pm10" not in c]

# X_with_pm = df[features_with_pm]
# X_without_pm = df[features_without_pm]
# y = df["AQI"]
# ================= FEATURES =================
# With PM features
features_with_pm = [c for c in df.columns if c not in ["timestamp_unix", "timestamp_utc", 
                                                      "timestamp_ist", "AQI", "AQI_category"]]
# Without PM features
features_without_pm = [c for c in features_with_pm if "pm2_5" not in c and "pm10" not in c]

# Ensure only numeric columns
X_with_pm = df[features_with_pm].select_dtypes(include="number")
X_without_pm = df[features_without_pm].select_dtypes(include="number")
y = df["AQI"]


# ================= SPLIT DATA =================
X_train_with_pm, X_test_with_pm, y_train, y_test = train_test_split(
    X_with_pm, y, test_size=0.2, random_state=42
)

X_train_without_pm, X_test_without_pm, _, _ = train_test_split(
    X_without_pm, y, test_size=0.2, random_state=42
)

# ================= PIPELINE GB =================
def train_gb_model(X_train, y_train, n_estimators=200, learning_rate=0.1, random_state=42):
    """
    Trains a Gradient Boosting Regressor using median imputation for NaNs
    """
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('model', GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state
        ))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

# ================= TRAIN MODELS =================
print("📊 Training GB with PM features...")
gb_with_pm = train_gb_model(X_train_with_pm, y_train)
print("📊 Training GB without PM features...")
gb_without_pm = train_gb_model(X_train_without_pm, y_train)

# ================= EVALUATION =================
def evaluate_model(model, X, y, name):
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    r2 = r2_score(y, y_pred)
    print(f"\n📊 Model: {name}")
    print(f"MAE : {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2  : {r2:.2f}")
    return mae, rmse, r2

print("\n✅ Evaluating models on test data...")
evaluate_model(gb_with_pm, X_test_with_pm, y_test, "GB with PM")
evaluate_model(gb_without_pm, X_test_without_pm, y_test, "GB without PM")

# ================= SAVE MODELS =================
joblib.dump(gb_with_pm, os.path.join(MODEL_FOLDER, "gb_model_with_pm.pkl"))
joblib.dump(gb_without_pm, os.path.join(MODEL_FOLDER, "gb_model_without_pm.pkl"))
print("\n✅ Models saved successfully.")
