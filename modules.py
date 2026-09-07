from types import ModuleType

main: dict
desc: dict
vis: int
wind: dict
loc: dict
cityname: str
vis_km: float
windspeed: int
wind_deg: int
temp_curr: float
feels_like: float
temp_min: float
temp_max: float
pressure: float
humidity: float
desc_title: str
desc_desc: str


def kelvin_to_celsius(temp: float):
    """
    Converts temperature values from Kelvin to Celsius.
    Accepts floating points. Rounds off to one decimal point.
    """
    return round(temp - 273.16, 1)


def cel2f(temp: float):
    """
    Converts Celsius temperature values to Fahrenheit values.
    Accepts floating points. Rounds off to one decimal point.
    """
    return round(((temp * 9 / 5) + 32), 1)


# TODO: use f-strings to format strings into displaying like tables
# TODO: add sunrise and sunset time
# ref: https://www.geeksforgeeks.org/python/how-to-make-a-table-in-python/#using-string-formatting
def display(
    city,
    desc_title,
    desc_desc,
    temp_curr,
    feels_like,
    temp_min,
    temp_max,
    humidity,
    pressure,
    windspeed,
    vis,
    vis_km,
    tempunit,
    winddir,
):
    """
    A set of `print()` statements to effectively provide information in one go.
    """
    print(f"{city:-^40}")
    print(f"Weather: {desc_title}: {desc_desc}")
    print(f"Temperature: {temp_curr}{tempunit}")
    print(f"Feels like: {feels_like}{tempunit}")
    print(f"Minimum Temperature: {temp_min}{tempunit}")
    print(f"Maximum Temperature: {temp_max}{tempunit}")
    print(f"Humidity: {humidity}%")
    print(f"Pressure: {pressure} hPa")  # (1 hPa = 1 mBar)
    print(f"Wind Speed: {windspeed} m/s")
    print(f"Wind Direction: {winddir}")
    print(f"Visibility: {vis} m (or) {vis_km} km")


def wind_direction(wind_deg: int):
    """
    Accepts a wind direction degree value and checks if it lies between certain angles to determine the direction.
    Accepts integers, returns strings.
    """
    if (360 - 22.5) <= wind_deg <= (0 + 22.5):
        return "North (N)"
    elif (0 + 22.5) <= wind_deg <= (90 - 22.5):
        return "North-East (NE)"
    elif (90 - 22.5) <= wind_deg <= (90 + 22.5):
        return "East (E)"
    elif (90 + 22.5) <= wind_deg <= (180 - 22.5):
        return "South-East (SE)"
    elif (180 - 22.5) <= wind_deg <= (180 + 22.5):
        return "South (S)"
    elif (180 - 22.5) <= wind_deg <= (270 - 22.5):
        return "South-West (SW)"
    elif (270 - 22.5) <= wind_deg <= (270 + 22.5):
        return "West (W)"
    elif (270 + 22.5) <= wind_deg <= (360 - 22.5):
        return "North-West (NW)"
    else:
        return "???"


def temp_unit(corf):
    """
    Simple function to define the temperature unit, depending on user input.
    """
    if corf.upper() == "C":
        return "°C"
    if corf.upper() == "F":
        return "°F"


def city_search(
    city: str, token: str, requests: ModuleType, time: ModuleType, sys: ModuleType
):
    """
    Conducts an API request to OpenWeatherMap using the `requests` module, with `time` and `sys` helping quit the program in the event of an error.
    """
    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}"
    )
    try:
        if resp.status_code == 200:
            pass
        else:
            print(
                f"Error, API response code: {resp.status_code}. Program terminates in 3 seconds."
            )
            time.sleep(3)
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(
            "Error, unsuccessful connection to OpenWeatherMap. Program terminates in 3 seconds."
        )
        time.sleep(3)
        sys.exit(1)
    return resp.json()


def datadef(data):
    global main, desc, vis, wind, loc, cityname, vis_km, windspeed, wind_deg, temp_curr, feels_like, temp_min, temp_max, pressure, humidity, desc_title, desc_desc
    main = data["main"]
    desc = data["weather"][0]
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

    desc_title = desc["main"]
    desc_desc = desc["description"]
