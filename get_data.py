import pandas as pd
import requests

# Get the session key for a given country, session type and year
def fetch_session_key(country, session_type, year):
    url = f"https://api.openf1.org/v1/sessions?country_name={country}&session_name={session_type}&year={year}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())["session_key"][0]
    else:
        raise ValueError(
            f"Error fetching session key. Status code {response.status_code}"
        )

# Fetch data for a given data type, driver number and session key
def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")

# Fetch stint data for a given session key
def fetch_stint_data(session_key):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")

# Fetch position data for a given session key
def get_position_data(session_key):
    url= f"https://api.openf1.org/v1/positions?session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")