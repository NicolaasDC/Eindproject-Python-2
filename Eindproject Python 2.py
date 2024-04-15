import requests
import pandas as pd
print('Welke plaats wil je de weer gegevens? Vb. Gent (x: 3.72  en y: 51.05)')
print('Geef de x-coördinaat in:')
x = float(input())
print('Geef de y-coördnaat in:')
y = float(input())

URL = f'https://api.open-meteo.com/v1/forecast?latitude={y}&longitude={x}&hourly=temperature_2m,precipitation_probability,precipitation&timezone=Europe%2FBerlin'

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

URL_hist = f'https://archive-api.open-meteo.com/v1/archive?latitude={y}&longitude={x}6&start_date=2000-01-01&end_date=2024-04-12&daily=temperature_2m_max,temperature_2m_mean,precipitation_sum&timezone=Europe%2FBerlin'

response_hist = requests.get(URL_hist)
json_data_hist = response_hist.json()

time_hist = json_data_hist.get('daily')['time']
temp_max = json_data_hist.get('daily')['temperature_2m_max']
temp_mean = json_data_hist.get('daily')['temperature_2m_mean']
precipitation_hist = json_data_hist.get('daily')['precipitation_sum']

rows = []
for n in range(0, len(time_hist)):
    row = {}
    row['time'] = time_hist[n]
    row['temp_max'] = temp_max[n]
    row['temp_mean'] = temp_mean[n]
    row['precipitation_hist'] = precipitation_hist[n]
    rows.append(row)

df = pd.DataFrame(rows)
print(df)