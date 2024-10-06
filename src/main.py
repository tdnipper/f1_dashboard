from urllib.request import urlopen
import pandas as pd
import json
import streamlit as st
import requests

data_type = "laps"
drive_number = '55'
session_key = "9159"

# response = urlopen(
#     f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
# )
# data_json = json.loads(response.read().decode("utf-8"))
# data = pd.json_normalize(data_json)

def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")
    
data = fetch_data(data_type, drive_number, session_key)
st.write(data)


