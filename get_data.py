import pandas as pd
import streamlit as st
import requests

data_type = "laps"
drive_number = '55'
session_key = "9159"

def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")
    
data = fetch_data(data_type, drive_number, session_key)
st.write(data)


