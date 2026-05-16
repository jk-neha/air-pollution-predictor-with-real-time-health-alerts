# PolluCast FINAL REALTIME ALERT SYSTEM
import pandas as pd
from datetime import datetime
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import os

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_TOKEN")

TWILIO_SMS = "+yout twilio sms no"
TWILIO_WHATSAPP = "your wahtsappa twilio no"

client = Client(ACCOUNT_SID, AUTH_TOKEN)



MY_PHONE = "+your number"
MY_WHATSAPP = "you whatsapp number"

client = Client(ACCOUNT_SID, AUTH_TOKEN)


SENDER_EMAIL = "yoursender-@gmail.com"
APP_PASSWORD = "your mail id password"
# # ==========================================
# FILE PATHS
# ==========================================
AQI_FILE = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\datasets\3nungambakkam_final.csv"
USERS_FILE = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\alerts\9.1PolluCast_Users.csv"
LOG_FILE = r"C:\Users\Neha\Neha's-DESKTOP\pollucast_api_res\1AQI\alerts\10Alerts_log.csv"

# ==============================
# READ AQI
# ==============================
df = pd.read_csv(AQI_FILE)
latest_aqi = df["AQI"].iloc[-1]

def category(aqi):
    if aqi <= 50: return "Good"
    elif aqi <=100: return "Moderate"
    elif aqi <=150: return "Unhealthy for Sensitive"
    elif aqi <=200: return "Unhealthy"
    elif aqi <=300: return "Very Unhealthy"
    else: return "Hazardous"

aqi_status = category(latest_aqi)

msg_text = f"""
⚠ PolluCast Live Alert
AQI Level: {latest_aqi:.2f}
Status: {aqi_status}

Avoid outdoor exposure if unsafe.
- Loyola Research Project
"""

print(msg_text)

# ==============================
# READ USERS
# ==============================
users = pd.read_excel(USERS_FILE)

# ==============================
# ALERT + LOG STORAGE LIST
# ==============================
log_rows = []

# ==============================
# SEND ALERTS
# ==============================
for i in range(len(users)):

    name = str(users.loc[i, "Name"])
    phone = str(users.loc[i, "Phone"]).strip()
    whatsapp = str(users.loc[i, "WhatsApp"]).strip()
    email = str(users.loc[i, "Email"]).strip()

    print(f"\nSending alerts to {name}...")

    if not phone.startswith("+"):
        phone = "+" + phone

    if not whatsapp.startswith("whatsapp:+"):
        whatsapp = "whatsapp:" + whatsapp

    sms_status = "Not Sent"
    wa_status = "Not Sent"
    mail_status = "Not Sent"

    # ===== SMS =====
    try:
        client.messages.create(body=msg_text, from_=TWILIO_SMS, to=phone)
        print("✅ SMS sent")
        sms_status = "Sent"
    except Exception as e:
        print("❌ SMS error:", e)
        sms_status = "Failed"

    # ===== WhatsApp =====
    try:
        client.messages.create(body=msg_text, from_=TWILIO_WHATSAPP, to=whatsapp)
        print("✅ WhatsApp sent")
        wa_status = "Sent"
    except Exception as e:
        print("❌ WhatsApp error:", e)
        wa_status = "Failed"

    # ===== Email =====
    try:
        msg = MIMEText(msg_text)
        msg["Subject"] = "⚠ PolluCast AQI Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg.as_string())
        server.quit()

        print("✅ Email sent")
        mail_status = "Sent"
    except Exception as e:
        print("❌ Email error:", e)
        mail_status = "Failed"

    # ===== SAVE EACH USER LOG =====
    log_rows.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Phone": phone,
        "SMS": sms_status,
        "WhatsApp": wa_status,
        "Email": mail_status,
        "AQI": latest_aqi,
        "Status": aqi_status
    })

# ==============================
# SAVE LOG FILE WITH HEADERS
# ==============================
log_df = pd.DataFrame(log_rows)

if os.path.exists(LOG_FILE):
    log_df.to_csv(LOG_FILE, mode='a', header=False, index=False)
else:
    log_df.to_csv(LOG_FILE, index=False)

print("\n🔥 All alerts sent & logged successfully 🔥")