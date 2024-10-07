import pandas as pd
import requests
import plotly.express as px


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


country = "Italy"
session_type = "Race"
year = "2023"

session_key = fetch_session_key(country, session_type, year)

data_type = "laps"
driver_number = "55"


# Fetch data for a given data type, driver number and session key
def fetch_data(data_type, drive_number, session_key):
    url = f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")


def fetch_stint_data(session_key):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        raise ValueError(f"Error fetching data. Status code {response.status_code}")


# race_data = fetch_data(data_type, driver_number, session_key)

stint_data = fetch_stint_data(session_key)
stint_data["stint_duration"] = stint_data["lap_end"] - stint_data["lap_start"]
stint_data["driver_number"] = stint_data["driver_number"].astype(str)
stint_data["stint_number"] = stint_data["stint_number"].astype(str)

stint_data = (
    stint_data.groupby(["driver_number", "stint_number", "compound"])
    .agg({"stint_duration": "sum", "lap_start": "min", "lap_end": "max"})
    .reset_index()
)
stint_data.to_csv("stint_data.csv")

# Plot the data

# fig_race = px.scatter(
#     race_data,
#     x="lap_number",
#     y="lap_duration",
#     title=f"Lap times",
#     color="is_pit_out_lap",
#     trendline="ols",
# )
# fig_race.show()


# Draw the figure using go.Bar to get each stint as a separate bar and color by compound, order by driver and stint number
# This is a bit more complex than using px.bar but gives more control over the plot
# First loop over each driver, then each stint for that driver
# Add a bar for each stint with the compound color and the hover text
from plotly import graph_objects as go

fig_stint = go.Figure()
# compound_colors = {"SOFT": "green", "MEDIUM": "blue", "HARD": "red"}
# Use the qualitative color swatch from plotly express for the compounds
color_swatch = px.colors.qualitative.G10
# Create a dictionary with the compound as the key and the color as the value
compound_colors = {compound: color_swatch[i] for i, compound in enumerate(stint_data["compound"].unique())}
for driver in stint_data["driver_number"].unique():
    # Get the data for the driver and loop over each stint
    driver_data = stint_data[stint_data["driver_number"] == driver]
    for stint_number in driver_data["stint_number"].unique():
        # Get the data for the stint and add a bar to the figure
        stint_info = driver_data[driver_data["stint_number"] == stint_number]
        fig_stint.add_trace(
            go.Bar(
                x=stint_info["driver_number"],
                y=stint_info["stint_duration"],
                # Select the color based on the compound and the color dictionary using the first value in the compound column
                marker_color=compound_colors[stint_info["compound"].iloc[0]],
                # Add the hover text with the stint information
                hovertext=f"Duration: {stint_info['stint_duration'].values[0]} laps<br>Start: {stint_info['lap_start'].values[0]}<br>End: {stint_info['lap_end'].values[0]}<br>Compound: {stint_info['compound'].values[0]}<br>Driver: {stint_info['driver_number'].values[0]}",
                # Display only the custom text on hover
                hoverinfo="text",
            )
        )
# Update the layout with the title and axis labels and show the figure
fig_stint.update_layout(
    title="Stint Durations",
    xaxis_title="Driver",
    yaxis_title="Laps",
    showlegend=False,
    barmode="stack",
    hovermode="x",
)
fig_stint.show()
