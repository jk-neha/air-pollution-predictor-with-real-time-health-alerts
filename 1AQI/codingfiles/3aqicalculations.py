import pandas as pd

# Load cleaned data
df = pd.read_csv(r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets\2nungambakkam_cleaned.csv")

# CPCB Breakpoints
PM25_BP = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 350, 401, 500),
]

PM10_BP = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 500, 401, 500),
]

def calc_aqi(conc, breakpoints):
    for bp_low, bp_high, i_low, i_high in breakpoints:
        if bp_low <= conc <= bp_high:
            return ((i_high - i_low)/(bp_high - bp_low)) * (conc - bp_low) + i_low
    return None  # above max breakpoint

# Compute AQI for each row
df['AQI_PM25'] = df['pm2_5'].apply(lambda x: calc_aqi(x, PM25_BP))
df['AQI_PM10'] = df['pm10'].apply(lambda x: calc_aqi(x, PM10_BP))

# Overall AQI = max of PM2.5 and PM10
df['AQI'] = df[['AQI_PM25', 'AQI_PM10']].max(axis=1)

# Optional: AQI Category
def aqi_category(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Satisfactory"
    elif aqi <= 200: return "Moderate"
    elif aqi <= 300: return "Poor"
    elif aqi <= 400: return "Very Poor"
    else: return "Severe"

df['AQI_Category'] = df['AQI'].apply(aqi_category)

# Save final dataset
df.to_csv(r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets\3nungambakkam_final.csv", index=False)

print("✅ AQI calculation completed")
print(df[['timestamp_utc','pm2_5','pm10','AQI','AQI_Category']].head())
