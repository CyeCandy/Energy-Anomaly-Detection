from fastapi import FastAPI
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import IsolationForest

# 1. Initialize the FastAPI app (This fixes the NameError)
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Grid Analysis API is running"}

@app.post("/analyze")
def analyze_grid(data: dict):
    # Convert incoming JSON data to a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # 2. Forecasting Logic (SARIMA)
    # We use SARIMA to predict the next 3 steps in the energy load
    model = SARIMAX(df['load'], order=(1, 1, 1))
    res = model.fit(disp=False)
    forecast_values = res.forecast(steps=3)
    avg_forecast = forecast_values.mean()

    # 3. Anomaly Detection (Isolation Forest)
    # This identifies if any current data points are statistical outliers
    iso = IsolationForest(contamination=0.1)
    df['anomaly'] = iso.fit_predict(df[['load']])
    
    # 4. Storage & Cost Optimization Logic
    # Scenario: We "save" money by storing energy when demand (and price) is low.
    baseline_load = df['load'].mean()
    price_per_mwh = 50 # Mock market price
    
    if avg_forecast < (baseline_load * 0.9):
        action = "BUY & STORE (Low Demand)"
        # Simple savings math: (Load Difference) * Price * Efficiency Factor
        savings = (baseline_load - avg_forecast) * price_per_mwh * 0.15 
    elif avg_forecast > (baseline_load * 1.1):
        action = "DISCHARGE / SELL (Peak Demand)"
        savings = (avg_forecast - baseline_load) * price_per_mwh * 0.20
    else:
        action = "HOLD / STANDBY"
        savings = 0

    # 5. Return the results as JSON
    return {
        "forecast": forecast_values.tolist(),
        "anomalies": df['anomaly'].tolist(),
        "recommendation": action,
        "potential_savings_usd": round(savings, 2)
    }