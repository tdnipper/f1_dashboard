from urllib.request import urlopen
import pandas as pd
import json

response = urlopen('https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159')
data_json = json.loads(response.read().decode("utf-8"))
data = pd.json_normalize(data_json)
data.to_excel("test.xlsx")