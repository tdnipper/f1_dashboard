from urllib.request import urlopen
import pandas as pd
import json
import matplotlib.pyplot as plt

data_type = "laps"
drive_number = '55'
session_key = "9159"

response = urlopen(
    f"https://api.openf1.org/v1/{data_type}?driver_number={drive_number}&session_key={session_key}"
)
data_json = json.loads(response.read().decode("utf-8"))
data = pd.json_normalize(data_json)
data.to_excel("test.xlsx")

plt.plot(data["lap_number"], data["lap_duration"])
plt.tight_layout()
plt.show()
