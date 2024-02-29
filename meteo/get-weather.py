import requests
import json
from matplotlib import pyplot as plt
import pandas as pd
import sys

city='beijing' # replace any city of country
if len(sys.argv) > 1:
    city = sys.argv[1]
result_city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city)
location = result_city.json()

longitude=str(location['results'][0]['longitude'])
latitude=str(location['results'][0]['latitude'])

print('city: ' + city)
print('longitude: ' + str(longitude))
print('latitude: ' + str(latitude))

result_weather = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=16')
data = result_weather.json()

times = data['hourly']['time']
dates = pd.to_datetime(times, format='%Y-%m-%dT%H:%M')

values = data['hourly']['temperature_2m']

#print(dates.to_list())
#print(values)
#print(len(data['hourly']['time']))

plt.plot(dates.to_list(), values)
plt.title(city + " temperature ")
plt.xlabel("hourly")
plt.ylabel("temperature")
plt.show()
