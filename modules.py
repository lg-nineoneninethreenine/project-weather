import requests


def kelvin_to_celsius(temperature: float) -> float:
    return round(temperature - 273.16, 1)


def cel2f(temperature: float) -> float:
    return round(temperature * 9 / 5 + 32, 1)


def convert_temperature(temperature: float, unit: str) -> float:
    if unit.upper() == "F":
        return cel2f(temperature)
    if unit.upper() == "C":
        return temperature
    raise ValueError("Temperature unit must be C or F.")


def wind_direction(degrees: int) -> str:
    directions = (
        "North (N)",
        "North-East (NE)",
        "East (E)",
        "South-East (SE)",
        "South (S)",
        "South-West (SW)",
        "West (W)",
        "North-West (NW)",
    )
    return directions[int((degrees % 360 + 22.5) // 45) % len(directions)]


def get_weather(city: str, token: str, temperature_unit: str = "C") -> dict:
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": token},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "description": weather["description"].capitalize(),
        "temperature": convert_temperature(kelvin_to_celsius(main["temp"]), temperature_unit),
        "feels_like": convert_temperature(kelvin_to_celsius(main["feels_like"]), temperature_unit),
        "minimum": convert_temperature(kelvin_to_celsius(main["temp_min"]), temperature_unit),
        "maximum": convert_temperature(kelvin_to_celsius(main["temp_max"]), temperature_unit),
        "humidity": main["humidity"],
        "pressure": main["pressure"],
        "windspeed": wind["speed"],
        "winddir": wind_direction(wind["deg"]),
        "visibility_km": round(data["visibility"] / 1000, 1),
    }


def get_forecast(city: str, token: str, temperature_unit: str = "C") -> list:
    location_response = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct",
        params={"q": city, "appid": token, "limit": 1},
        timeout=10,
    )
    location_response.raise_for_status()
    locations = location_response.json()
    if not locations:
        raise ValueError("City not found.")

    location = locations[0]
    forecast_response = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "lat": location["lat"],
            "lon": location["lon"],
            "appid": token,
        },
        timeout=10,
    )
    forecast_response.raise_for_status()

    forecast = []
    for entry in forecast_response.json()["list"][:5]:
        forecast.append(
            {
                "time": entry["dt_txt"],
                "temperature": convert_temperature(
                    kelvin_to_celsius(entry["main"]["temp"]), temperature_unit
                ),
                "description": entry["weather"][0]["description"].capitalize(),
                "rain_chance": round(entry["pop"] * 100),
            }
        )
    return forecast
