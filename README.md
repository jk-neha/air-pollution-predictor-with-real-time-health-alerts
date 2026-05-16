# PolluCast — Air Pollution Predictor with Real-Time Health Alerts

> An end-to-end IoT + Machine Learning system that monitors air quality, predicts AQI, and delivers real-time health alerts via SMS, WhatsApp, and Email.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![Twilio](https://img.shields.io/badge/Twilio-Alerts-red?style=flat-square&logo=twilio)
![IoT](https://img.shields.io/badge/IoT-NodeMCU%20ESP8266-green?style=flat-square)
![Cloud](https://img.shields.io/badge/Cloud-Thinger.io-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [ML Model Performance](#ml-model-performance)
- [AQI Classification](#aqi-classification)
- [Alert System](#alert-system)
- [Results](#results)
- [Setup & Usage](#setup--usage)
- [Security](#security)
- [Future Work](#future-work)
- [Author](#author)

---

## Overview

**PolluCast** is a full-stack air quality monitoring solution that bridges hardware sensing, cloud data pipelines, and machine learning to deliver actionable pollution insights.

It uses an MQ135 gas sensor and DHT22 temperature/humidity sensor connected to a NodeMCU (ESP8266), feeds live readings into a cloud dashboard (Thinger.io), runs an ML model to predict AQI, and automatically dispatches health alerts when pollution crosses unsafe thresholds.

---

## System Architecture

```
IoT Sensors (MQ135 + DHT22)
        │
        ▼
NodeMCU ESP8266 (Data Collection)
        │
        ▼
Cloud Dashboard (Thinger.io) ──► Real-time Visualization
        │
        ▼
Python Pipeline (Data Preprocessing + Feature Engineering)
        │
        ▼
ML Model (Random Forest / Gradient Boosting) ──► AQI Prediction
        │
        ▼
Alert Engine ──► SMS / WhatsApp / Email (Twilio + SMTP)
```

---

## Features

- **Real-time sensor data collection** via MQ135 (gas) and DHT22 (temperature + humidity)
- **Machine learning AQI prediction** using Random Forest and Gradient Boosting
- **Multi-channel alert system** — SMS, WhatsApp, and Email triggered on threshold breach
- **Cloud dashboard** with live sensor visualization on Thinger.io
- **WHO-standard AQI classification** across 6 health risk categories
- **Model comparison** with performance metrics for both ML approaches
- **Secure credential management** via `.env` file

---

## Tech Stack

| Category | Tools / Libraries |
|---|---|
| Language | Python 3.10 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (Random Forest, Gradient Boosting) |
| Alerts | Twilio API (SMS & WhatsApp), SMTP (Email) |
| IoT Hardware | MQ135, DHT22, NodeMCU ESP8266 |
| Cloud Platform | Thinger.io |
| Env Management | python-dotenv |

---

## Project Structure

```
air-pollution-predictor/
│
├── 1AQI/
│   ├── codingfiles/          # Data collection, preprocessing, feature engineering
│   ├── datasets/             # Raw and processed air quality data
│   ├── modelsrfgb/           # Trained ML model files (.pkl)
│   ├── alerts/               # SMS, WhatsApp, and Email alert scripts
│   └── Results/              # Output visuals, graphs, and screenshots
│
├── .env.example              # Template for API keys and credentials
├── requirements.txt          # Python dependencies
└── README.md
```

---

## How It Works

**Step 1 — Sensor Data Collection**
MQ135 and DHT22 sensors collect real-time air quality parameters (CO₂, temperature, humidity) via NodeMCU ESP8266.

**Step 2 — Cloud Upload**
Sensor readings are pushed to the Thinger.io cloud platform for live monitoring and storage.

**Step 3 — Data Preprocessing**
Python scripts clean the raw data, handle missing values, and engineer features for model input.

**Step 4 — AQI Prediction**
A trained Random Forest or Gradient Boosting model predicts the AQI value from the processed features.

**Step 5 — Classification**
The predicted AQI is mapped to a WHO health category (Good → Hazardous).

**Step 6 — Alert Dispatch**
If AQI exceeds a defined threshold, the system automatically sends health warnings via SMS, WhatsApp, and Email.

---

## ML Model Performance

Two models were trained and compared for AQI prediction:

| Model | Notes |
|---|---|
| Random Forest | Ensemble of decision trees; robust to noise and overfitting |
| Gradient Boosting | Sequential boosting; high accuracy on structured tabular data |

> See `Results/AQI_prediction_ML_models.png` for full performance metrics.

---

## AQI Classification

| AQI Range | Category | Health Implication |
|---|---|---|
| 0 – 50 | Good | Air quality is satisfactory |
| 51 – 100 | Moderate | Acceptable; some risk for sensitive individuals |
| 101 – 150 | Unhealthy for Sensitive Groups | Sensitive groups may experience effects |
| 151 – 200 | Unhealthy | Everyone may begin to experience effects |
| 201 – 300 | Very Unhealthy | Health alert — serious effects for everyone |
| 301+ | Hazardous | Emergency conditions; entire population affected |

Standards based on [WHO Air Quality Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health).

---

## Alert System

Alerts are automatically triggered when AQI exceeds the safe threshold.

| Channel | Tool | Trigger |
|---|---|---|
| SMS | Twilio API | AQI > threshold |
| WhatsApp | Twilio WhatsApp API | AQI > threshold |
| Email | SMTP (Gmail) | AQI > threshold |

Sample alert screenshots are available in the `Results/` folder:
- `Results/AQI_Email_Alert.png`
- `Results/AQI_SMS_Alert.png` *(if available)*

---

## Results

| Output | Preview |
|---|---|
| AQI Prediction (ML Models) | `Results/AQI_prediction_ML_models.png` |
| Email Alert | `Results/AQI_Email_Alert.png` |
| IoT Sensor Setup | `Results/IoT_Sensor_Components.png` |
| Cloud Dashboard | `Results/Thinger_io_Dashboard.png` *(if available)* |

---

## Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/jk-neha/air-pollution-predictor-with-real-time-health-alerts.git
cd air-pollution-predictor-with-real-time-health-alerts
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials
```bash
cp .env.example .env
# Fill in your Twilio SID, Auth Token, phone numbers, and SMTP credentials
```

### 4. Run the pipeline
```bash
# Preprocess data
python 1AQI/codingfiles/preprocess.py

# Train / load ML model and predict AQI
python 1AQI/codingfiles/predict_aqi.py

# Run alert system
python 1AQI/alerts/send_alerts.py
```

---

## Security

All API keys, credentials, and tokens are managed through a `.env` file and are **never committed to the repository**.

A `.env.example` template is provided with placeholder values. Never share your actual `.env` file.

---

## Future Work

- [ ] Deploy as a live REST API using FastAPI
- [ ] Build a mobile-friendly dashboard
- [ ] Improve prediction accuracy with LSTM / deep learning models
- [ ] Add real-time geographic pollution map visualization
- [ ] Docker containerization for easy deployment

---

## Author

**Neha Vardhini J K**  
M.Sc. Computer Science — Loyola College, Chennai  
[GitHub](https://github.com/jk-neha)

---

*If this project was useful or interesting, consider giving it a star — it helps others discover it.*
