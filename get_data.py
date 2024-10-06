import pandas as pd
import requests
import plotly.express as px

data_type = "laps"
drive_number = '55'

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

data_type = "laps"
drive_number = '55'

# Fetch data for a given data type, driver number and session key
def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")
    
def fetch_stint_data(session_key, driver_number):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}&driver_number={driver_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")
    
race_data = fetch_data(data_type, drive_number, session_key)
stint_data = fetch_stint_data(session_key, drive_number)

# data.to_csv('data.csv', index=False)
fig_race = px.scatter(race_data, x='lap_number', y='lap_duration', title=f"Lap times for driver {drive_number}", color='is_pit_out_lap', trendline='ols')
fig_race.show()

fig_stint = px.bar(stint_data, x='stint_number', y='stint_duration', title=f"Stint times for driver {drive_number}")

