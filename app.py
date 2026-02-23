import streamlit as st
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd
import time

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="NYC Taxi AI Fare", layout="wide")

st.title("🚕 NYC Taxi AI Fare Estimator")

# -----------------------
# Load Model
# -----------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------
# Session State
# -----------------------
if "pickup" not in st.session_state:
    st.session_state.pickup = None
if "dropoff" not in st.session_state:
    st.session_state.dropoff = None

# -----------------------
# Sidebar
# -----------------------
st.sidebar.header("Trip Settings")

passenger_count = st.sidebar.slider("Passenger Count", 1, 6, 1)

pickup_datetime = st.sidebar.datetime_input(
    "Pickup Date & Time",
    pd.Timestamp.now()
)

map_style = st.sidebar.selectbox(
    "Map Style",
    ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"]
)

if st.sidebar.button("Reset Trip"):
    st.session_state.pickup = None
    st.session_state.dropoff = None

# -----------------------
# Map
# -----------------------
center = [40.7580, -73.9855]

m = folium.Map(location=center, zoom_start=12, tiles=map_style)

if st.session_state.pickup:
    folium.Marker(st.session_state.pickup,
                  icon=folium.Icon(color="green"),
                  tooltip="Pickup").add_to(m)

if st.session_state.dropoff:
    folium.Marker(st.session_state.dropoff,
                  icon=folium.Icon(color="red"),
                  tooltip="Dropoff").add_to(m)

if st.session_state.pickup and st.session_state.dropoff:
    folium.PolyLine(
        [st.session_state.pickup, st.session_state.dropoff],
        color="blue",
        weight=5
    ).add_to(m)

map_data = st_folium(m, width=1000, height=500)

# -----------------------
# Click Logic
# -----------------------
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]

    if not st.session_state.pickup:
        st.session_state.pickup = (lat, lng)
    elif not st.session_state.dropoff:
        st.session_state.dropoff = (lat, lng)

# -----------------------
# Prediction
# -----------------------
if st.session_state.pickup and st.session_state.dropoff:

    distance_km = geodesic(
        st.session_state.pickup,
        st.session_state.dropoff
    ).km

    avg_speed = 25
    estimated_time = (distance_km / avg_speed) * 60

    col1, col2 = st.columns(2)
    col1.metric("Distance (km)", f"{distance_km:.2f}")
    col2.metric("Estimated Time (min)", f"{estimated_time:.1f}")

    if st.button("Predict Fare"):

        # Extract time features
        minute = pickup_datetime.minute
        hour = pickup_datetime.hour
        day = pickup_datetime.day
        weekday = pickup_datetime.weekday()
        month = pickup_datetime.month
        year = pickup_datetime.year

        input_data = np.array([[
            st.session_state.pickup[1],   # pickup_longitude
            st.session_state.pickup[0],   # pickup_latitude
            st.session_state.dropoff[1],  # dropoff_longitude
            st.session_state.dropoff[0],  # dropoff_latitude
            passenger_count,
            minute,
            hour,
            day,
            weekday,
            month,
            year
        ]])

        prediction = model.predict(input_data)[0]

        # Animation
        placeholder = st.empty()
        for i in np.linspace(0, prediction, 30):
            placeholder.metric("Estimated Fare ($)", f"{i:.2f}")
            time.sleep(0.02)

        placeholder.metric("Estimated Fare ($)", f"{prediction:.2f}")

else:
    st.info("Click twice on the map to select Pickup and Dropoff.")