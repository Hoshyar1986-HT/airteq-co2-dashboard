# Updated app.py for better mobile display (centered layout and smaller figure)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AirTeq CO₂ Dashboard", layout="centered")
st.title(" AirTeq – CO₂ Monitoring Dashboard (Mobile-Friendly)")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("airteq_subset.csv")
    df["Tijd"] = pd.to_datetime(df["Tijd"])
    return df

df_all = load_data()

# Room and date selection
rooms = sorted(df_all["Naam"].unique())
default_rooms = ["0.14 Baby 1", "1.02 Peuter+", "0.08 Slaapkamer Baby's"]
selected_rooms = st.multiselect("Select Room(s)", options=rooms, default=default_rooms)

selected_date = st.date_input("Select Date", value=pd.to_datetime("2024-05-21").date())

st.subheader(f"Hourly CO₂ Comparison – {selected_date}")

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
for room in selected_rooms:
    df_room = df_all[df_all["Naam"] == room].copy()
    df_room = df_room.set_index("Tijd")
    df_day = df_room[df_room.index.date == selected_date]
    df_hourly = df_day["CO2"].resample("H").mean().dropna()
    ax.plot(df_hourly.index, df_hourly.values, marker='o', label=room)

# Threshold zones
ax.axhspan(300, 550, color='green', alpha=0.1, label='Green (≤ 550 ppm)')
ax.axhspan(550, 700, color='orange', alpha=0.1, label='Orange (550–700 ppm)')
ax.axhspan(700, 1800, color='red', alpha=0.1, label='Red (> 700 ppm)')
ax.set_ylim(300, 1800)
ax.set_ylabel("CO₂ (ppm)")
ax.set_xlabel("Hour")
ax.grid(True)
ax.legend()
st.pyplot(fig)
