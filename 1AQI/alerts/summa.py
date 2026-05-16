import joblib

model = joblib.load(r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\modelsrfgb\rf_model_with_pm.pkl")

print("Model loaded successfully")
print("Features used in model:")
print(model.feature_names_in_)
