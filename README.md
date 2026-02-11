# ⚡ Energy Grid Anomaly & Demand Dashboard
**An AI-driven Microservices Prototype for Smart Grid Optimization**

## 📖 Project Overview
This project is a functional prototype designed for energy grid operators and asset managers. It demonstrates how to translate complex time-series forecasting and unsupervised machine learning into actionable operational decisions.

By predicting demand cycles and monitoring asset health, the system identifies opportunities for **energy arbitrage** (buying/storing power when demand is low) and **predictive maintenance**, with all financial logic localized to **British Pounds (£)**.

## 🛠 Architecture & Tech Stack
The project follows a decoupled **Microservices Architecture**, separating the heavy computational logic from the user interface.

- **Backend (The Brain):** Developed with **FastAPI**. 
  - **Forecasting:** Uses **SARIMA** (Seasonal Auto-Regressive Integrated Moving Average) to project grid load.
  - **Anomaly Detection:** Uses **Isolation Forest** to identify outliers in sensor data.
- **Frontend (The UI):** Developed with **Streamlit** and **Plotly** for interactive data visualization.
- **Language:** Python 3.9+

## 🚀 Key Features
- **Predictive Buy/Store Logic:** Automatically generates recommendations to charge storage assets when a demand trough is forecasted.
- **Real-Time Health Monitoring:** Flags statistical anomalies in load data that could indicate equipment failure or grid stress.
- **Interactive ROI Metrics:** Calculates potential **GBP (£)** savings based on optimized energy storage decisions.



## 💻 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend (FastAPI):**
   ```bash
   uvicorn main:app --reload
   ```

4. **Run the Frontend (Streamlit):**
   Open a new terminal tab and run:
   ```bash
   streamlit run app.py
   ```
