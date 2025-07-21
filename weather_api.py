from ast import dump
import re
from time import sleep
from typing import final
from matplotlib.font_manager import json_dump
import requests
import json

city = input("What city do you want to get the weather for? ")
country_code = input("In which country? ")
state_region = input("And which state or region? ")
api_key = input("Enter your OpenWeatherMap API key:")
scripped_space = api_key.strip()

url_s = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_region},{country_code}&appid={scripped_space}"

find_coord = requests.get(url_s) #q={city},{state_region},{country_code}&appid={scripped_space}")

if find_coord.status_code == 200:
    final_coord = find_coord.json()
    if final_coord:
        print(f'\n===================================================')
        print(f'Coordinates for {city.casefold()}, {state_region.upper()}:')
        print(f'===================================================\n')
        print(f"Latitude: {final_coord[0]['lat']}")
        print(f"Longitude: {final_coord[0]['lon']}\n")


print(f'LOADING WEATHER DATA FOR {city.upper()}, {state_region.upper()}, {country_code.upper()}...')

sleep(5)

url_l = f"http://api.openweathermap.org/data/2.5/weather?lat={final_coord[0]['lat']}&lon={final_coord[0]['lon']}&appid={scripped_space}&units=imperial"

response = requests.get(url_l) #lat={final_coord[0]['lat']}&lon={final_coord[0]['lon']}&appid={scripped_space}&units=imperial")
print(f'response')
if response.status_code == 200:
    # data = response.json()
    print(f'\n===================================================')
    print(f'Weather data for {city.casefold()}, {state_region.upper()}:')
    print(f'===================================================\n')

for k, v in response.json().items():
    if k == "weather":
        print(f"Condition: {v[0]['description']}")
    if k == "main":
        print(f"Temperature: {response.json()['main']['temp']}°F")
        print(f"Feels Like: {response.json()['main']['feels_like']}°F")
        print(f"Humidity: {response.json()['main']['humidity']}%\n")