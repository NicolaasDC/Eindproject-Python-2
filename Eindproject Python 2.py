import requests
import pandas as pd
import matplotlib.pyplot as plt

print('Welke plaats wil je de weer gegevens? Vb. Gent (x: 3.72  en y: 51.05)')
print('Geef de x-coördinaat in:')
# x = float(input())
x= 3.72
print('Geef de y-coördnaat in:')
# y = float(input())
y = 51.05

URL = f'https://api.open-meteo.com/v1/forecast?latitude={y}&longitude={x}&hourly=temperature_2m,precipitation_probability,precipitation&timezone=Europe%2FBerlin'

response = requests.get(URL)
json_data = response.json()
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

dates_next_week = []
mean_temp_daily = []
max_temp_daily = []
daily_precipitation = []
for n in range(0, 7):
    dates_next_week.append(time[24*n][0:10])
    mean_temp_daily.append(round(sum(temp[24*n:24*(n+1)])/24, 1))
    max_temp_daily.append(max(temp[24*n:24*(n+1)]))
    daily_precipitation.append(sum(temp[24*n:24*(n+1)]))



print(dates_next_week)
print(mean_temp_daily)
print(max_temp_daily)
print(daily_precipitation)

x_axis = df['time']
y_axis = df['temp']

plt.plot(x_axis, y_axis)

# Create a scatter plot (bubble chart)
plt.scatter(x_axis, y_axis)

# Customize the plot
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature next week')

plt.show()

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

df_hist = pd.DataFrame(rows)
