import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import IsolationForest

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Grid Analysis API is running"}

@app.post("/analyze")
def analyze_grid(data: dict):
    df = pd.DataFrame(data)
    
    # 1. Forecasting Logic (SARIMA)
    model = SARIMAX(df['load'], order=(1, 1, 1))
    res = model.fit(disp=False)
    forecast_values = res.forecast(steps=3)
    avg_forecast = forecast_values.mean()

    # 2. Anomaly Detection (Isolation Forest)
    iso = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = iso.fit_predict(df[['load']])
    
    # 3. Arbitrage Logic (Updated for GBP)
    baseline_load = df['load'].mean()
    
    # Updated price to reflect typical UK Day-Ahead prices (e.g., £65/MWh)
    price_per_mwh_gbp = 65 
    
    if avg_forecast < baseline_load:
        action = "BUY & STORE (Low Demand)"
        savings = (baseline_load - avg_forecast) * price_per_mwh_gbp * 1.5
    else:
        action = "DISCHARGE / SELL (Peak Demand)"
        savings = (avg_forecast - baseline_load) * price_per_mwh_gbp * 1.5

    return {
        "forecast": forecast_values.tolist(),
        "anomalies": df['anomaly'].tolist(),
        "recommendation": action,
        "currency": "GBP",
        "potential_savings_gbp": round(abs(savings), 2)
    }