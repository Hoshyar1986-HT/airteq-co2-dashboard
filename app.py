
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AirTeq CO₂ Dashboard", layout="wide")

st.title("🌿 AirTeq – CO₂ Monitoring Dashboard (Prototype)")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("airteq_subset.csv")
    df["Tijd"] = pd.to_datetime(df["Tijd"])
    return df

df_all = load_data()

# Room and date selection
rooms = sorted(df_all["Naam"].unique())
selected_room = st.selectbox("Select Room", rooms, index=0)
selected_date = st.date_input("Select Date")

# Filter and process data
df_room = df_all[df_all["Naam"] == selected_room].copy()
df_room = df_room.set_index("Tijd")
df_day = df_room[df_room.index.date == selected_date]
df_hourly = df_day["CO2"].resample("H").mean().dropna()

# Plotting
st.subheader(f"Hourly CO₂ Levels – {selected_room} on {selected_date}")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_hourly.index, df_hourly.values, marker='o', color='black')
ax.axhspan(300, 550, color='green', alpha=0.1, label='Green (≤ 550 ppm)')
ax.axhspan(550, 700, color='orange', alpha=0.1, label='Orange (550–700 ppm)')
ax.axhspan(700, 1800, color='red', alpha=0.1, label='Red (> 700 ppm)')
ax.set_ylim(300, 1800)
ax.set_ylabel("CO₂ (ppm)")
ax.set_xlabel("Hour")
ax.grid(True)
ax.legend()
st.pyplot(fig)
