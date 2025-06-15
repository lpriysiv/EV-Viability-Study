import streamlit as st
import pandas as pd
import os

st.title("📊 Data Pipeline Dashboard")

DATA_PATH = "../outputs/summary.csv"
PLOT_PATH = "../outputs/plots.png"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    st.subheader("🔍 Data Summary")
    st.dataframe(df)
else:
    st.warning("No summary data found. Run pipeline first.")

if os.path.exists(PLOT_PATH):
    st.subheader("📈 Visualizations")
    st.image(PLOT_PATH)
else:
    st.warning("No plot image found.")