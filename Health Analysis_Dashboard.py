import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import webbrowser
import threading
import os
import sys
import time
import subprocess

# -------------------------------
# Step 1: Generate / Load Data
# -------------------------------
np.random.seed(42)

patient_id = np.arange(1, 101)
age = np.random.randint(20, 80, size=100)
systolic_bp = np.random.randint(90, 180, size=100)
cholesterol = np.random.randint(150, 300, size=100).astype(float)
heart_rate = np.random.randint(60, 120, size=100)

cholesterol[np.random.choice(100, 5, replace=False)] = np.nan
mean_cholesterol = np.nanmean(cholesterol)
cholesterol = np.where(np.isnan(cholesterol), mean_cholesterol, cholesterol)

data = pd.DataFrame({
    "Patient ID": patient_id,
    "Age": age,
    "Systolic BP": systolic_bp,
    "Cholesterol": cholesterol,
    "Heart Rate": heart_rate
})

# -------------------------------
# Step 2: Streamlit Dashboard
# -------------------------------
st.set_page_config(page_title="Health Data Dashboard", layout="wide")
st.title("🏥 Health Data Analysis Dashboard")
st.markdown("Analyze and visualize patient health records interactively using NumPy and Streamlit.")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
age_filter = st.sidebar.slider("Select Age Range:", int(data["Age"].min()), int(data["Age"].max()), (20, 80))
filtered_data = data[(data["Age"] >= age_filter[0]) & (data["Age"] <= age_filter[1])]

st.subheader("📋 Filtered Patient Records")
st.dataframe(filtered_data)

st.subheader("📊 Summary Statistics")
st.write(filtered_data.describe())

# 1️⃣ Histogram: Age Distribution
st.subheader("📈 Age Distribution")
fig, ax = plt.subplots()
ax.hist(filtered_data["Age"], bins=10, color='skyblue', edgecolor='black')
ax.set_xlabel("Age (years)")
ax.set_ylabel("Number of Patients")
ax.set_title("Patient Age Distribution")
st.pyplot(fig)

# 2️⃣ Bar Chart: Average Metrics
st.subheader("📊 Average Health Metrics")
metrics = ["Age", "Systolic BP", "Cholesterol", "Heart Rate"]
averages = [filtered_data["Age"].mean(), filtered_data["Systolic BP"].mean(),
             filtered_data["Cholesterol"].mean(), filtered_data["Heart Rate"].mean()]
avg_df = pd.DataFrame({"Metric": metrics, "Average Value": averages})
bar_chart = alt.Chart(avg_df).mark_bar(color='teal').encode(
    x='Metric',
    y='Average Value',
    tooltip=['Metric', 'Average Value']
)
st.altair_chart(bar_chart, use_container_width=True)

# 3️⃣ Scatter Plot: Age vs BP
st.subheader("💓 Age vs Systolic Blood Pressure")
scatter_bp = alt.Chart(filtered_data).mark_circle(size=80, color='orange', opacity=0.6).encode(
    x='Age',
    y='Systolic BP',
    tooltip=['Patient ID', 'Age', 'Systolic BP']
)
st.altair_chart(scatter_bp, use_container_width=True)

# 4️⃣ Scatter Plot: Age vs Cholesterol
st.subheader("🩸 Age vs Cholesterol Level")
scatter_chol = alt.Chart(filtered_data).mark_circle(size=80, color='crimson', opacity=0.6).encode(
    x='Age',
    y='Cholesterol',
    tooltip=['Patient ID', 'Age', 'Cholesterol']
)
st.altair_chart(scatter_chol, use_container_width=True)

st.markdown("---")
st.markdown("✅ **Developed with NumPy, Matplotlib & Streamlit for interactive data visualization**")

# -------------------------------
# Step 3: Separate launcher script logic
# -------------------------------
def main():
    """Main function to run the Streamlit app"""
    # Check if we're already running in Streamlit
    if not st.runtime.exists():
        # Start Streamlit as a subprocess
        proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])
        
        # Wait a few seconds to let Streamlit server start
        time.sleep(5)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()

if __name__ == "__main__":
    main()
