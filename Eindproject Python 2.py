import requests
import pandas as pd

URL = 'https://api.open-meteo.com/v1/forecast?latitude=51.05&longitude=3.7167&hourly=temperature_2m,precipitation_probability,precipitation&timezone=Europe%2FBerlin'

response = requests.get(URL)
json_data = response.json()
#print(json_data)
time = json_data.get('hourly')['time']

temp = json_data.get('hourly')['temperature_2m']

precipitation = json_data.get('hourly')['precipitation']

rows = []
for n in range(0, len(time)):
    row = {}
    row['time'] = time[n]
    row['temp'] = temp[n]
    row['precipitation'] = precipitation[n]
    rows.append(row)


df = pd.DataFrame(rows)
print(df)