# Retry saving the enhanced Streamlit app to a file


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AirTeq CO₂ Dashboard", layout="centered")
st.title(" AirTeq – CO₂ Monitoring Dashboard ")

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

# Threshold configuration
st.sidebar.header("⚙️ CO₂ Threshold Settings")
green_max = st.sidebar.slider("Upper limit for Green (Good)", 300, 1000, 550)
orange_max = st.sidebar.slider("Upper limit for Orange (Moderate)", green_max + 1, 1500, 700)
red_min = orange_max + 1

# Suggestions dictionary
def suggest_action(avg_co2):
    if avg_co2 <= green_max:
        return "✅ Air quality is good. No immediate action needed."
    elif avg_co2 <= orange_max:
        return "⚠️ Consider opening windows or reducing room activity."
    else:
        return "🚨 High CO₂ levels! Immediate ventilation recommended."

# Display results
st.subheader(f"Hourly CO₂ Comparison – {selected_date}")
fig, ax = plt.subplots(figsize=(10, 4))

for room in selected_rooms:
    df_room = df_all[df_all["Naam"] == room].copy()
    df_room = df_room.set_index("Tijd")
    df_day = df_room[df_room.index.date == selected_date]
    df_hourly = df_day["CO2"].resample("H").mean().dropna()
    avg_co2 = df_hourly.mean()
    
    ax.plot(df_hourly.index, df_hourly.values, marker='o', label=f"{room} (avg: {avg_co2:.0f} ppm)")
    
    with st.expander(f"ℹ️ Recommendation for {room}"):
        st.write(f"**Average CO₂:** {avg_co2:.0f} ppm")
        st.write(suggest_action(avg_co2))

# Threshold display
ax.axhspan(300, green_max, color='green', alpha=0.1, label=f'Green (≤ {green_max} ppm)')
ax.axhspan(green_max, orange_max, color='orange', alpha=0.1, label=f'Orange ({green_max+1}–{orange_max} ppm)')
ax.axhspan(orange_max, 1800, color='red', alpha=0.1, label=f'Red (> {orange_max} ppm)')
ax.set_ylim(300, 1800)
ax.set_ylabel("CO₂ (ppm)")
ax.set_xlabel("Hour")
ax.grid(True)
ax.legend()
st.pyplot(fig)

