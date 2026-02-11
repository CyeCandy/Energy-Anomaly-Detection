import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(page_title="Energy Grid Dashboard", layout="wide")
st.title("⚡ Energy Grid Anomaly & Demand Dashboard")
st.markdown("---")

# Sidebar for User Input
st.sidebar.header("Simulation Settings")
data_points = st.sidebar.slider("Historical Data Points", 30, 150, 60)

# Generate High-Volatility Mock Data
# No seed = New random data every time the button is clicked
load_data = np.random.normal(500, 150, data_points).tolist()
timestamps = pd.date_range(start="2024-01-01", periods=data_points, freq="H").strftime('%Y-%m-%d %H:%M:%S').tolist()
mock_data = {"load": load_data, "timestamp": timestamps}

# Main Execution Button
if st.button("Run Grid Analysis"):
    try:
        # Request data from our FastAPI microservice
        response = requests.post("http://127.0.0.1:8000/analyze", json=mock_data)
        results = response.json()

        # Row 1: Key Performance Indicators (KPIs)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Recommended Action", results["recommendation"])
        with col2:
            st.metric("Projected Savings", f"${results['potential_savings_usd']}", delta="Arbitrage Margin")
        with col3:
            # Check if -1 (anomaly) exists in the results
            has_anomaly = -1 in results["anomalies"]
            status = "⚠️ Anomaly Detected" if has_anomaly else "✅ Healthy"
            st.metric("Grid Asset Health", status)

        # Row 2: Interactive Visualization
        chart_data = pd.DataFrame({
            "Timestamp": pd.to_datetime(mock_data["timestamp"]),
            "Load (MWh)": mock_data["load"],
            "Anomaly": results["anomalies"]
        })
        
        fig = px.line(chart_data, x="Timestamp", y="Load (MWh)", title="Live Grid Load & Anomaly Detection")
        
        # Overlay red markers on anomaly points
        anomalies = chart_data[chart_data['Anomaly'] == -1]
        fig.add_scatter(x=anomalies["Timestamp"], y=anomalies["Load (MWh)"], 
                        mode='markers', name='Anomalies', marker=dict(color='red', size=10))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("Strategy updated based on real-time market volatility.")

    except Exception as e:
        st.error(f"Connection Error: Is the FastAPI server running? (Error: {e})")
else:
    st.info("System Ready. Click the button to start the analysis.")