import sys
import time

import requests

import modules

api_key = "12383b48d66ef5a9ab3d48e9b393fdba"

city: str = input("Enter city name: ")

corf = input("\nCelsius or Fahrenheit? (Reply with C or F only. Not case-sensitive.)\n")
print("\n")

if corf.upper() == "C" or corf.upper() == "F":
    tempunit = modules.temp_unit(corf)
else:
    print(
        f'You entered "{corf}", which is an invalid response. Program terminates in 3 seconds.'
    )
    time.sleep(3)
    sys.exit(1)

modules.datadef(modules.city_search(city, api_key, requests, time, sys))

if city == modules.cityname:
    country_code = modules.loc["country"]
    city += f", {country_code}"
else:
    city = modules.cityname
    country_code = modules.loc["country"]
    city += f", {country_code}"

if corf == "F" or corf == "f":
    temp_curr = modules.cel2f(modules.temp_curr)
    feels_like = modules.cel2f(modules.feels_like)
    temp_min = modules.cel2f(modules.temp_min)
    temp_max = modules.cel2f(modules.temp_max)
else:
    pass

winddir = modules.wind_direction(modules.wind_deg)
modules.display(
    city,
    modules.desc_title,
    modules.desc_desc,
    modules.temp_curr,
    modules.feels_like,
    modules.temp_min,
    modules.temp_max,
    modules.humidity,
    modules.pressure,
    modules.windspeed,
    modules.vis,
    modules.vis_km,
    tempunit,
    winddir,
)
