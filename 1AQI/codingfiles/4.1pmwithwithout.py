# 5aqi_calculation.py
import pandas as pd
import os

# ================= CONFIG =================
DATA_FOLDER = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets"
INPUT_FILE = os.path.join(DATA_FOLDER, "4.0nungambakkam_features.csv")
# =========================================

# ------------------- AQI CALCULATION -------------------
def calculate_aqi(pm25, pm10):
    # CPCB breakpoints for PM2.5
    pm25_bp = [(0,30,0,50),(31,60,51,100),(61,90,101,200),(91,120,201,300),(121,250,301,400),(251,500,401,500)]
    # CPCB breakpoints for PM10
    pm10_bp = [(0,50,0,50),(51,100,51,100),(101,250,101,200),(251,350,201,300),(351,430,301,400),(431,600,401,500)]
    
    def get_aqi(p, bp):
        for (Clow, Chigh, Ilow, Ihigh) in bp:
            if Clow <= p <= Chigh:
                return round((Ihigh-Ilow)/(Chigh-Clow)*(p-Clow)+Ilow)
        return None
    
    aqi_pm25 = get_aqi(pm25, pm25_bp)
    aqi_pm10 = get_aqi(pm10, pm10_bp)
    
    if aqi_pm25 is None and aqi_pm10 is None:
        return None
    elif aqi_pm25 is None:
        return aqi_pm10
    elif aqi_pm10 is None:
        return aqi_pm25
    else:
        return max(aqi_pm25, aqi_pm10)

# ------------------- MAIN -------------------
def main():
    # 1️⃣ Load dataset
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Loaded feature dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 2️⃣ Compute AQI
    df["AQI"] = df.apply(lambda row: calculate_aqi(row["pm2_5"], row["pm10"]), axis=1)
    
    # 3️⃣ Lag features
    df["AQI_lag_1h"] = df["AQI"].shift(1)
    df["AQI_lag_3h"] = df["AQI"].shift(3)
    df["AQI_lag_24h"] = df["AQI"].shift(24)
    
    # Fill missing lag values
    df.fillna(method="bfill", inplace=True)
    
    # 4️⃣ Save final dataset WITH PM features
    output_file_with_pm = os.path.join(DATA_FOLDER, "4.1nungambakkam_aqi_with_pm.csv")
    df.to_csv(output_file_with_pm, index=False)
    print(f"✅ Dataset WITH PM features saved: {output_file_with_pm}")
    
    # 5️⃣ Save dataset WITHOUT PM features (for comparison)
    df_no_pm = df.drop(columns=["pm2_5","pm10"])
    output_file_no_pm = os.path.join(DATA_FOLDER, "4.11nungambakkam_aqi_without_pm.csv")
    df_no_pm.to_csv(output_file_no_pm, index=False)
    print(f"✅ Dataset WITHOUT PM features saved: {output_file_no_pm}")

if __name__ == "__main__":
    main()
