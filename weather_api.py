from time import sleep
from rich.console import Console
from rich.progress import track
import requests
import json

console = Console()
green_black = Console(style="green on black")
red_black = Console(style="red on black")   
yellow_black = Console(style="yellow on black")

city = green_black.input("What city do you want to get the weather for? ")
country_code = "us"  # Default country code set to 'us'
state_region = green_black.input("And which state or region? ")
api_key = green_black.input("Enter your OpenWeatherMap API key:")
scripped_space = api_key.strip()
url_s = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_region},{country_code}&appid={scripped_space}"

find_coord = requests.get(url_s) #q={city},{state_region},{country_code}&appid={scripped_space}")

if find_coord.status_code == 200:
    final_coord = find_coord.json()
    if not final_coord:
        red_black.print(f"Error: No coordinates found for {city}, {state_region}, {country_code}. Please check your inputs.")
        exit()
   
    green_black.print(f'\n===================================================')
    green_black.print(f'Coordinates for {city.casefold()}, {state_region.upper()}:'.upper())
    green_black.print(f'===================================================\n')
    green_black.print(f"Latitude: {final_coord[0]['lat']}")
    green_black.print(f"Longitude: {final_coord[0]['lon']}\n")



yellow_black.print(f'LOADING WEATHER DATA FOR {city.upper()}, {state_region.upper()}, {country_code.upper()}...'.upper())

url_l = f"http://api.openweathermap.org/data/2.5/weather?lat={final_coord[0]['lat']}&lon={final_coord[0]['lon']}&appid={scripped_space}&units=imperial"
response = requests.get(url_l) #lat={final_coord[0]['lat']}&lon={final_coord[0]['lon']}&appid={scripped_space}&units=imperial")

for i in track(range(100)):
    sleep(0.05)  # Simulate a loading delay

if response.status_code == 200:
    # data = response.json()
    green_black.print(f'\n===================================================')
    green_black.print(f'Weather data for {city.casefold()}, {state_region.upper()}:'.upper())
    green_black.print(f'===================================================\n')

for k, v in response.json().items():
    if k == "weather":
        green_black.print(f"Condition: {v[0]['description']}")
    if k == "main":
        green_black.print(f"Temperature: {response.json()['main']['temp']}°F")
        green_black.print(f"Feels Like: {response.json()['main']['feels_like']}°F")
        green_black.print(f"Humidity: {response.json()['main']['humidity']}%\n")