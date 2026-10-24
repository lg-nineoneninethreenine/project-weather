import requests

import modules

API_KEY = "12383b48d66ef5a9ab3d48e9b393fdba"
BOX_WIDTH = 78


def draw_box(title: str, lines: list[str]) -> None:
    inner_width = BOX_WIDTH - 4
    heading = f" {title} "
    print(f"+-{heading:-^{inner_width}}-+")
    for line in lines:
        print(f"| {line[:inner_width]:<{inner_width}} |")
    print(f"+{'-' * (BOX_WIDTH - 2)}+")


def show_weather(report: dict, forecast: list, unit: str) -> None:
    degree_unit = unit
    location = f"{report['city']}, {report['country']}"

    print()
    print("=" * BOX_WIDTH)
    print(f"{'PROJECT WEATHER':^{BOX_WIDTH}}")
    print(f"{location:^{BOX_WIDTH}}")
    print("=" * BOX_WIDTH)

    draw_box(
        "CURRENT CONDITIONS",
        [
            f"Weather: {report['description']}",
            f"Temperature: {report['temperature']:.1f} {degree_unit}"
            f"    Feels like: {report['feels_like']:.1f} {degree_unit}",
            f"Low: {report['minimum']:.1f} {degree_unit}"
            f"    High: {report['maximum']:.1f} {degree_unit}",
            f"Humidity: {report['humidity']}%"
            f"    Pressure: {report['pressure']} hPa",
            f"Wind: {report['windspeed']} m/s {report['winddir']}"
            f"    Visibility: {report['visibility_km']} km",
        ],
    )

    forecast_lines = [
        f"{'DATE / TIME':<19} {'TEMP':>9}  {'CONDITIONS':<27} {'RAIN':>6}",
        "-" * (BOX_WIDTH - 4),
    ]
    for item in forecast:
        forecast_lines.append(
            f"{item['time']:<19} "
            f"{item['temperature']:>6.1f} {degree_unit}  "
            f"{item['description'][:27]:<27} "
            f"{item['rain_chance']:>5}%"
        )
    if not forecast:
        forecast_lines.append("No forecast data available.")

    draw_box("FORECAST - NEXT FIVE 3-HOUR SLOTS", forecast_lines)
    print()


def main() -> None:
    city = input("City: ").strip()
    if not city:
        print("Please enter a city name.")
        return

    unit = input("Temperature unit (C/F) [C]: ").strip().upper() or "C"
    while unit not in ("C", "F"):
        unit = input("Enter C for Celsius or F for Fahrenheit: ").strip().upper()

    try:
        report = modules.get_weather(city, API_KEY, unit)
        forecast = modules.get_forecast(city, API_KEY, unit)
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response else None
        if status_code == 404:
            print(f"City not found: {city}")
        elif status_code == 401:
            print("OpenWeatherMap rejected the API key.")
        else:
            print(f"Weather request failed (HTTP {status_code}).")
        return
    except requests.RequestException:
        print("Could not connect to OpenWeatherMap. Check the connection and try again.")
        return
    except (KeyError, IndexError, TypeError, ValueError) as error:
        print(f"Could not read weather data: {error}")
        return

    show_weather(report, forecast, unit)


if __name__ == "__main__":
    main()
