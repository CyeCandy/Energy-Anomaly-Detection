import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Energy Grid Dashboard", layout="wide")
st.title("⚡ Energy Grid Anomaly & Demand Dashboard")
st.subheader("Real-time Forecasting & Cost Optimization")

# 2. Sidebar - Simulation Settings
st.sidebar.header("Simulation Settings")
data_points = st.sidebar.slider("Number of Data Points", 20, 100, 50)

# 3. Generate Mock Data
# In a real PM scenario, this would come from a SQL database or IoT sensors
np.random.seed(42)
mock_data = {
    "load": np.random.normal(500, 50, data_points).tolist(),
    "timestamp": pd.date_range(start="2024-01-01", periods=data_points, freq="H").strftime('%Y-%m-%d %H:%M:%S').tolist()
}

# 4. Action Button
if st.button("Run Grid Analysis"):
    try:
        # Send data to the FastAPI "Engine" (Window 1)
        response = requests.post("http://127.0.0.1:8000/analyze", json=mock_data)
        results = response.json()

        # 5. Display Key Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Recommended Action", results["recommendation"])
        
        with col2:
            st.metric("Projected Savings", f"${results['potential_savings_usd']}")
            
        with col3:
            # Check for anomalies (Isolation Forest results)
            status = "⚠️ Issue Detected" if -1 in results["anomalies"] else "✅ Healthy"
            st.metric("Asset Health", status)

        # 6. Visualize the Data
        chart_data = pd.DataFrame({
            "Historical Load": mock_data["load"],
            "Anomaly Score": results["anomalies"]
        })
        
        fig = px.line(chart_data, y="Historical Load", title="Grid Load Over Time")
        # Highlight anomalies in red
        fig.add_scatter(x=chart_data[chart_data['Anomaly Score'] == -1].index, 
                        y=chart_data[chart_data['Anomaly Score'] == -1]['Historical Load'],
                        mode='markers', name='Anomalies', marker=dict(color='red', size=10))
        
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Connection Error: Is the FastAPI server running in Window 1? (Error: {e})")

else:
    st.info("Click the button above to fetch data from the FastAPI engine.")