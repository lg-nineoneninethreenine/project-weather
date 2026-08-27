import sys
import time

import requests

import modules

api_key = "12383b48d66ef5a9ab3d48e9b393fdba"

city:str = input("Enter city name: ")

resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")

try:
    if resp.status_code == 200:
        pass
    else:
        print(f"Error, API response code: {resp.status_code}. Program terminates in 3 seconds.")
        time.sleep(3)
        sys.exit(1)
except requests.exceptions.ConnectionError:
        print("Error, unsuccessful connection to OpenWeatherMap. Program terminates in 3 seconds.")
        time.sleep(3)
        sys.exit(1)

corf = input("\nCelsius or Fahrenheit? (Reply with C or F only. Not case-sensitive.)\n")
print("\n")

if corf == "C" or corf == "F" or corf == "c" or corf == "f":
    pass
else:
    print(f"You entered \"{corf}\", which is an invalid response. Program terminates in 3 seconds.")
    time.sleep(3)
    sys.exit(1)

data = resp.json()
main = data["main"]
desc = data["weather"]
vis = data["visibility"]
wind = data["wind"]
loc = data["sys"]
cityname = data["name"]

vis_km = round(vis / 1000, 1)
windspeed = wind["speed"]
wind_deg = wind["deg"]

temp_curr = modules.kelvin_to_celsius(main["temp"])
feels_like = modules.kelvin_to_celsius(main["feels_like"])
temp_min = modules.kelvin_to_celsius(main["temp_min"])
temp_max = modules.kelvin_to_celsius(main["temp_max"])

pressure = main["pressure"]
humidity = main["humidity"]

desc_title = desc[0]["main"]
desc_desc = desc[0]["description"]

if city == cityname:
    country_code = loc["country"]
    city += f", {country_code}"
else:
    city = cityname
    country_code = loc["country"]
    city += f", {country_code}"

if corf == "F" or corf == "f":
    temp_curr = modules.cel2f(temp_curr)
    feels_like = modules.cel2f(feels_like)
    temp_min = modules.cel2f(temp_min)
    temp_max = modules.cel2f(temp_max)
else:
    pass

tempunit = modules.temp_unit(corf)

winddir = modules.wind_direction(wind_deg)
modules.display(city, desc_title, desc_desc,
            temp_curr, feels_like, temp_min,
            temp_max, humidity, pressure,
            windspeed, vis, vis_km, tempunit, winddir)
