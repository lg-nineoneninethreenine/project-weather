import sys
import time

import requests

api_key = "12383b48d66ef5a9ab3d48e9b393fdba"

city:str = input("Enter city name: ")

resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")

if resp.status_code == 200:
    pass
else:
    print(f"Error, API response code: {resp.status_code}. Program terminates in 3 seconds.")
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

def kelvin_to_celsius(temp:float):
    return round(temp - 273.16, 1)
def cel2f(temp:float):
    return round(((temp * 9/5) + 32),1)

# TODO: use f-strings to format strings into displaying like tables
# TODO: add sunrise and sunset time
# ref: https://www.geeksforgeeks.org/python/how-to-make-a-table-in-python/#using-string-formatting
def display(city, desc_title, desc_desc,
            temp_curr, feels_like, temp_min,
            temp_max, humidity, pressure,
            windspeed, vis, vis_km, tempunit, winddir):
    print(f"{city:-^40}")
    print(f"Weather: {desc_title}: {desc_desc}")
    print(f"Temperature: {temp_curr}{tempunit}")
    print(f"Feels like: {feels_like}{tempunit}")
    print(f"Minimum Temperature: {temp_min}{tempunit}")
    print(f"Maximum Temperature: {temp_max}{tempunit}")
    print(f"Humidity: {humidity}%")
    print(f"Pressure: {pressure} hPa") # (1 hPa = 1 mBar)
    print(f"Wind Speed: {windspeed} m/s")
    print(f"Wind Direction: {winddir}")
    print(f"Visibility: {vis} m (or) {vis_km} km")

def wind_direction(wind_deg:int):
    if ((360 - 22.5) <= wind_deg <= (0 + 22.5)):
        return "North (N)"
    elif ((0 + 22.5) <= wind_deg <= (90 - 22.5)):
        return "North-East (NE)"
    elif ((90 - 22.5) <= wind_deg <= (90 + 22.5)):
        return "East (E)"
    elif ((90 + 22.5) <= wind_deg <= (180 - 22.5)):
        return "South-East (SE)"
    elif ((180 - 22.5) <= wind_deg <= (180 + 22.5)):
        return "South (S)"
    elif ((180 - 22.5) <= wind_deg <= (270 - 22.5)):
        return "South-West (SW)"
    elif ((270 - 22.5) <= wind_deg <= (270 + 22.5)):
        return "West (W)"
    elif ((270 + 22.5) <= wind_deg <= (360 - 22.5)):
        return "North-West (NW)"
    else:
        return "???"


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

temp_curr = kelvin_to_celsius(main["temp"])
feels_like = kelvin_to_celsius(main["feels_like"])
temp_min = kelvin_to_celsius(main["temp_min"])
temp_max = kelvin_to_celsius(main["temp_max"])

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
    temp_curr = cel2f(temp_curr)
    feels_like = cel2f(feels_like)
    temp_min = cel2f(temp_min)
    temp_max = cel2f(temp_max)
else:
    pass
def temp_unit(temp_curr, feels_like, temp_min, temp_max):
    if corf == "C" or corf == "c":
        return "°C"
    if corf == "F" or corf == "f":
        return "°F"

tempunit = temp_unit(temp_curr, feels_like, temp_min, temp_max)

winddir = wind_direction(wind_deg)
display(city, desc_title, desc_desc,
            temp_curr, feels_like, temp_min,
            temp_max, humidity, pressure,
            windspeed, vis, vis_km, tempunit, winddir)
