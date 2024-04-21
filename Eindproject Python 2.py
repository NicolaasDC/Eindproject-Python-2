import matplotlib.pyplot as plt
import pandas as pd
import requests
import datetime
from tabulate import tabulate

print('Welke plaats wil je de weer gegevens? Vb. Gent (x: 3.72  en y: 51.05)')
print('Geef de x-coördinaat in:')
# x = float(input())
x = 3.72
print('Geef de y-coördnaat in:')
# y = float(input())
y = 51.05

now = datetime.date.today()
actual_year = now.year

while True:
  try:
    year = input(f'Vanaf welk jaar wil je de historische gegevens? (Vanaf 1940 tot {actual_year}):')
    if year.isdigit():
       year = int(year)
    else:
       raise ValueError()
    if 1940 <= year <= actual_year:
        break
    raise ValueError()
  except ValueError:
    print(f"Input moet een integer zijn tussen 1940 en {actual_year}.")

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

week_ago = datetime.date.today() - datetime.timedelta(days=7)

URL_hist = f'https://archive-api.open-meteo.com/v1/archive?latitude={y}&longitude={x}6&start_date={year}-01-01&end_date={week_ago}&daily=temperature_2m_max,temperature_2m_mean,precipitation_sum&timezone=Europe%2FBerlin'

response_hist = requests.get(URL_hist)
json_data_hist = response_hist.json()

time_hist = json_data_hist.get('daily')['time']
temp_max_hist = json_data_hist.get('daily')['temperature_2m_max']
temp_mean_hist = json_data_hist.get('daily')['temperature_2m_mean']
precipitation_hist = json_data_hist.get('daily')['precipitation_sum']

rows = []
for n in range(0, len(time_hist)):
    row = {}
    row['time'] = time_hist[n]
    row['month_day'] = time_hist[n][5:10]
    row['temp_max'] = temp_max_hist[n]
    row['temp_mean'] = temp_mean_hist[n]
    row['precipitation_hist'] = precipitation_hist[n]
    rows.append(row)

df_hist = pd.DataFrame(rows)

today = time[0][5:10]

result = df_hist[df_hist['month_day'] == today][['time', 'temp_max', 'temp_mean', 'precipitation_hist']]
print(tabulate(result, headers = 'keys', tablefmt = 'pretty'))

dates_next_week = []
mean_temp_daily = []
hist_temp_mean = []
max_temp_daily = []
hist_max_temp = []
daily_precipitation = []
hist_precipitation = []

for n in range(0, 7):
    dates_next_week.append(time[24*n][0:10])
    mean_temp_daily.append(round(sum(temp[24*n:24*(n+1)])/24, 1))
    max_temp_daily.append(max(temp[24*n:24*(n+1)]))
    daily_precipitation.append(round(sum(precipitation[24*n:24*(n+1)]), 1))


for n in dates_next_week:
    result = df_hist[df_hist['month_day'] == n[5:10]][['time', 'temp_max', 'temp_mean', 'precipitation_hist']]
    hist_temp_mean.append(round(result['temp_mean'].sum() / result['temp_mean'].count(), 1))
    hist_max_temp.append(round(result['temp_max'].sum() / result['temp_max'].count(), 1))
    hist_precipitation.append(round(result['precipitation_hist'].sum() / result['precipitation_hist'].count(), 1))


data_next_week = {
    'date': dates_next_week,
    'mean_temp_prediction': mean_temp_daily,
    'mean_temp_hist': hist_temp_mean,
    'max_temp_prediction': max_temp_daily,
    'max_temp_hist': hist_max_temp,
    'precipitation_prediction': daily_precipitation,
    'precipitation_hist': hist_precipitation
}
df_next_week = pd.DataFrame(data_next_week)
print(tabulate(df_next_week, headers = 'keys', tablefmt = 'pretty'))

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