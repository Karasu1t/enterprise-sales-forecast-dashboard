import google.auth
import google.auth.transport.requests
import streamlit as st
import requests
import json
import datetime

st.set_page_config(layout="wide")
st.title("Sales Forecast Dashboard (Vertex AI)")

st.write("## Input Parameters")
# Date input as calendar (year/month/day/holiday_flag auto-extracted)
date = st.date_input(
    "Date",
    value=datetime.date.today(),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date(2100, 12, 31),
)
# Extract year, month, day
year = date.year
month = date.month
day = date.day
# Holiday flag: 1 if Saturday or Sunday, else 0
holiday_flag = 1 if date.weekday() >= 5 else 0

is_cup_ramen = st.selectbox(
    "Cup Ramen", [0, 1], format_func=lambda x: "Yes" if x else "No"
)
is_pet_bottle_tea = st.selectbox(
    "Pet Bottle Tea", [0, 1], format_func=lambda x: "Yes" if x else "No"
)
is_chocolate = st.selectbox(
    "Chocolate", [0, 1], format_func=lambda x: "Yes" if x else "No"
)
price = st.number_input("Price", min_value=0, value=150)
sales = st.number_input("Sales", min_value=0, value=1000)
weather_flag = st.selectbox(
    "Weather Flag", [0, 1], format_func=lambda x: "Bad Weather" if x else "Normal"
)


def get_access_token():
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials.token


if st.button("Predict"):
    # Check that at least one product flag is set
    if not (is_cup_ramen or is_pet_bottle_tea or is_chocolate):
        st.error(
            "At least one of Cup Ramen, Pet Bottle Tea, or Chocolate must be selected."
        )
    else:
        # Vertex AI endpoint URL and token
        ENDPOINT_URL = "https://asia-northeast1-aiplatform.googleapis.com/v1/projects/134070188729/locations/asia-northeast1/endpoints/5074538632279228416:predict"
        ACCESS_TOKEN = get_access_token()

        # Prepare input data as list (year, month, day, holiday_flag auto)
        instance = [
            year,
            month,
            day,
            is_cup_ramen,
            is_pet_bottle_tea,
            is_chocolate,
            price,
            sales,
            holiday_flag,
            weather_flag,
        ]
        data = {"instances": [instance]}

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                ENDPOINT_URL, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            result = response.json()
            st.success(f"Prediction: {result['predictions'][0]:.2f}")
        except Exception as e:
            st.error(f"API request error: {e}")
