import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import json

data_type = "laps"
drive_number = '55'
session_key = "9159"

# Get the session key for a given country, session type and year
def fetch_session_key(country, session_type, year):
    url = f"https://api.openf1.org/v1/sessions?country_name={country}&session_name={session_type}&year={year}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())["session_key"][0]
    else:
        raise ValueError(f"Error fetching session key. Status code {response.status_code}")
    

country = 'Italy'
session_type = 'Race'
year = '2023'

session_key = fetch_session_key(country, session_type, year)

def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")
    
# data = fetch_data(data_type, drive_number, session_key)
# # data.to_csv('data.csv', index=False)
# fig = px.line(data, x='lap_number', y='lap_duration', title=f"Lap times for driver {drive_number}")
# fig.show()

