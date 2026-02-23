About This Project:
Ever wondered how much a NYC taxi ride would cost before you even hop in? This Streamlit web app brings that to life using machine learning! Pick your pickup and dropoff locations on a live map, choose your passengers, set the date and time, and watch the AI predict your fare in real time—all wrapped in a sleek dark-themed interface.

Why It's Cool:

Click-to-select pickup & dropoff on an interactive map.

Animated fare prediction—watch the price count up smoothly!

Distance & estimated trip time calculated instantly.

Elegant dark mode with metric cards for clean, modern look.

Fully responsive UI, works on desktop and mobile.

Uses LightGBM model trained on NYC Taxi dataset with time and location features.

Tech Stack & Tools:

Python 🐍

Streamlit 🌟

Folium for interactive maps 🗺️

LightGBM / scikit-learn for ML models ⚡

Geopy for distance calculations 📏

Pandas & NumPy for data manipulation 📊

Data Columns Used:

pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
passenger_count, minute, hour, day, weekday, month, year

How to Run:

Clone the repo.

Install dependencies: pip install -r requirements.txt.

Run the app: streamlit run app.py.

Click on the map to select pickup & dropoff, set your trip details, and predict the fare!
