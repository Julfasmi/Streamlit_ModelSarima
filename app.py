import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

st.title("Strategic Revenue Forecast Simulator")

# Load models
with open("models/traffic_model.pkl", "rb") as f:
    traffic_model = pickle.load(f)

with open("models/basket_model.pkl", "rb") as f:
    basket_model = pickle.load(f)

# Controls
months = st.slider("Forecast Months", 1, 24, 6)
traffic_adj = st.slider("Traffic Growth Adjustment (%)", -30, 30, 0)
basket_adj = st.slider("Basket Growth Adjustment (%)", -20, 20, 0)

# Baseline Forecast
traffic_forecast = traffic_model.get_forecast(steps=months).predicted_mean
basket_forecast = basket_model.get_forecast(steps=months).predicted_mean

# Apply adjustments
traffic_forecast_adj = traffic_forecast * (1 + traffic_adj/100)
basket_forecast_adj = basket_forecast * (1 + basket_adj/100)

# Revenue Simulation
revenue_baseline = traffic_forecast * basket_forecast
revenue_adjusted = traffic_forecast_adj * basket_forecast_adj

# Plot
fig, ax = plt.subplots()
ax.plot(revenue_baseline, label="Baseline")
ax.plot(revenue_adjusted, label="Adjusted Scenario")
ax.legend()
st.pyplot(fig)

st.write("Projected Revenue Impact:",
         round(revenue_adjusted.sum() - revenue_baseline.sum(), 2))