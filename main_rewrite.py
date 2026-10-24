import tkinter as tk

import customtkinter as ctk
import requests

import modules

API_KEY = "12383b48d66ef5a9ab3d48e9b393fdba"

app = ctk.CTk()
app.title("Weather")
app.geometry("1080x620")
app.resizable(False, False)
app.grid_columnconfigure(0, weight=5, minsize=500)
app.grid_columnconfigure(1, weight=6, minsize=560)
app.grid_rowconfigure(3, weight=1)

heading_label = ctk.CTkLabel(app, text="Weather", font=("Segoe UI", 30, "bold"))
heading_label.grid(row=0, column=0, columnspan=2, pady=(4, 1))

theme_button = ctk.CTkButton(app, text="Light theme", width=95, height=28)
theme_button.place(relx=0.985, rely=0.025, anchor="ne")

searchframe = ctk.CTkFrame(app)
searchframe.grid(row=1, column=0, columnspan=2, padx=12, pady=2, sticky="ew")
searchframe.grid_columnconfigure(0, weight=1)

searchbar = ctk.CTkEntry(
    searchframe,
    placeholder_text="Enter city name",
)
searchbar.grid(row=0, column=0, padx=(10, 6), pady=8, sticky="ew")

tempbutton = ctk.CTkSegmentedButton(searchframe, values=["C", "F"])
tempbutton.grid(row=0, column=1, padx=6, pady=8)
tempbutton.set("C")

status_label = ctk.CTkLabel(app, text="Search for a city to see its weather.")
status_label.grid(row=2, column=0, columnspan=2, padx=12, pady=(0, 2))

cards_frame = ctk.CTkFrame(app, fg_color="transparent")
cards_frame.grid(row=3, column=0, padx=(8, 3), pady=(0, 8), sticky="nsew")
cards_frame.grid_columnconfigure(0, weight=1)
cards_frame.grid_columnconfigure(1, weight=1)
cards_frame.grid_rowconfigure(0, weight=1)
cards_frame.grid_rowconfigure(1, weight=1)

weather_values: dict[str, ctk.CTkLabel] = {}


def add_section(
    title: str,
    fields: tuple[tuple[str, str], ...],
    row: int,
    column: int,
    value_anchor: str = "e",
) -> None:
    section = ctk.CTkFrame(cards_frame)
    section.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
    section.grid_columnconfigure(0, minsize=105)
    section.grid_columnconfigure(1, weight=1)

    title_label = ctk.CTkLabel(section, text=title, font=("Segoe UI", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, padx=9, pady=(5, 2), sticky="w")

    for field_row, (key, label) in enumerate(fields, start=1):
        field_label = ctk.CTkLabel(section, text=label, font=("Arial", 14))
        field_label.grid(row=field_row, column=0, padx=9, pady=2, sticky="w")

        value_label = ctk.CTkLabel(
            section,
            text="--",
            anchor=value_anchor,
            font=("Arial", 14, "bold"),
        )
        value_label.grid(row=field_row, column=1, padx=9, pady=2, sticky="ew")
        weather_values[key] = value_label


add_section(
    "Overview",
    (("location", "Location"), ("description", "Weather")),
    row=0,
    column=0,
)
add_section(
    "Temperature",
    (
        ("temperature", "Current"),
        ("feels_like", "Feels like"),
        ("minimum", "Minimum"),
        ("maximum", "Maximum"),
    ),
    row=0,
    column=1,
)
add_section(
    "Conditions",
    (("humidity", "Humidity"), ("pressure", "Pressure")),
    row=1,
    column=0,
)
add_section(
    "Wind & visibility",
    (
        ("windspeed", "Wind speed"),
        ("winddir", "Wind direction"),
        ("visibility", "Visibility"),
    ),
    row=1,
    column=1,
    value_anchor="w",
)

forecast_frame = ctk.CTkFrame(app)
forecast_frame.grid(row=3, column=1, padx=(3, 12), pady=(0, 8), sticky="nsew")
forecast_frame.grid_columnconfigure(0, weight=1)
forecast_frame.grid_rowconfigure(1, weight=1)

forecast_title = ctk.CTkLabel(
    forecast_frame,
    text="Next five 3-hour forecasts",
    font=("Segoe UI", 19, "bold"),
)
forecast_title.grid(row=0, column=0, padx=12, pady=(8, 6), sticky="w")

plot_background = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
if isinstance(plot_background, (tuple, list)):
    plot_background = plot_background[1 if ctk.get_appearance_mode() == "Dark" else 0]
plot_colors = {
    "text": "#eeeeee" if ctk.get_appearance_mode() == "Dark" else "#333333"
}
temperature_plot = tk.Canvas(
    forecast_frame,
    width=560,
    height=1,
    background=plot_background,
    highlightthickness=0,
)
temperature_plot.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
plot_state = {"forecast": [], "unit": "°C"}
weather_state = {"report": None}


def draw_temperature_plot(forecast: list, unit: str) -> None:
    temperature_plot.delete("all")
    if not forecast:
        temperature_plot.create_text(
            temperature_plot.winfo_width() // 2,
            temperature_plot.winfo_height() // 2,
            text="No forecast data",
            fill=plot_colors["text"],
        )
        return

    width = temperature_plot.winfo_width()
    height = temperature_plot.winfo_height()
    if width < 2 or height < 2:
        return

    left, right, top, bottom = 38, width - 18, 48, max(86, height - 106)
    temperatures = [
        modules.cel2f(item["temperature"]) if unit == "°F" else item["temperature"]
        for item in forecast
    ]
    minimum = min(temperatures)
    maximum = max(temperatures)
    spread = maximum - minimum or 1
    points = []

    temperature_plot.create_text(
        8,
        8,
        text=unit,
        fill=plot_colors["text"],
        anchor="nw",
        font=("Arial", 12, "bold"),
    )
    for index, temperature in enumerate(temperatures):
        x = left + (right - left) * (index + 0.5) / len(temperatures)
        y = bottom - (temperature - minimum) / spread * (bottom - top - 32) - 16
        points.extend((x, y))

    for y in (top, (top + bottom) / 2, bottom):
        temperature_plot.create_line(
            left,
            y,
            right,
            y,
            fill="#656b75",
            dash=(3, 3),
        )
    temperature_plot.create_line(
        *points,
        fill="#42a5f5",
        width=5,
        smooth=True,
    )
    for index, item in enumerate(forecast):
        x, y = points[index * 2], points[index * 2 + 1]
        temperature_plot.create_oval(
            x - 6, y - 6, x + 6, y + 6, fill="#42a5f5", outline="#ffffff", width=2
        )
        temperature_plot.create_text(
            x,
            y - 20,
            text=f"{temperatures[index]:.1f}°",
            fill=plot_colors["text"],
            font=("Arial", 14, "bold"),
        )
        temperature_plot.create_text(
            x,
            bottom + 18,
            text=item["time"][5:16],
            fill=plot_colors["text"],
            font=("Arial", 12, "bold"),
            justify="center",
            width=(right - left) / len(forecast) - 4,
        )
        column_width = (right - left) / len(forecast) - 4
        temperature_plot.create_text(
            x,
            bottom + 43,
            text=item["description"],
            fill=plot_colors["text"],
            font=("Arial", 12),
            justify="center",
            width=column_width,
        )
        temperature_plot.create_text(
            x,
            bottom + 69,
            text=f"Rain {item['rain_chance']}%",
            fill=plot_colors["text"],
            font=("Arial", 12, "bold"),
        )


temperature_plot.bind(
    "<Configure>",
    lambda *_: draw_temperature_plot(
        plot_state["forecast"],
        plot_state["unit"],
    ),
)


def search() -> None:
    city = searchbar.get().strip()
    if not city:
        status_label.configure(text="Enter a city name first.")
        return
    status_label.configure(text="Loading weather...")
    app.update_idletasks()
    try:
        report = modules.get_weather(city, API_KEY, "C")
        forecast = modules.get_forecast(city, API_KEY, "C")
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response else None
        if status_code == 404:
            message = f"City not found: {city}."
        elif status_code == 401:
            message = "OpenWeatherMap rejected the API key."
        else:
            message = f"Weather request failed (HTTP {status_code})."
        status_label.configure(text=message)
        return
    except requests.RequestException:
        status_label.configure(text="Could not connect to OpenWeatherMap.")
        return
    except (KeyError, IndexError, TypeError, ValueError) as error:
        status_label.configure(text=str(error) or "OpenWeatherMap returned invalid data.")
        return

    weather_state["report"] = report
    plot_state["forecast"] = forecast
    refresh_temperatures()
    status_label.configure(text="Weather updated.")


def refresh_temperatures(unit: str | None = None) -> None:
    report = weather_state["report"]
    if report is None:
        return

    if unit is None:
        unit = tempbutton.get()
    degree_unit = f"°{unit}"
    weather_values["location"].configure(
        text=f"{report['city']}, {report['country']}"
    )
    weather_values["description"].configure(text=report["description"])
    weather_values["temperature"].configure(
        text=f"{convert_temperature(report['temperature'], unit):.1f} {degree_unit}"
    )
    weather_values["feels_like"].configure(
        text=f"{convert_temperature(report['feels_like'], unit):.1f} {degree_unit}"
    )
    weather_values["minimum"].configure(
        text=f"{convert_temperature(report['minimum'], unit):.1f} {degree_unit}"
    )
    weather_values["maximum"].configure(
        text=f"{convert_temperature(report['maximum'], unit):.1f} {degree_unit}"
    )
    weather_values["humidity"].configure(text=f"{report['humidity']}%")
    weather_values["pressure"].configure(text=f"{report['pressure']} hPa")
    weather_values["windspeed"].configure(text=f"{report['windspeed']} m/s")
    weather_values["winddir"].configure(text=report["winddir"].split("(")[-1].rstrip(")"))
    weather_values["visibility"].configure(text=f"{report['visibility_km']} km")
    plot_state["unit"] = degree_unit
    draw_temperature_plot(plot_state["forecast"], degree_unit)


def convert_temperature(temperature: float, unit: str) -> float:
    if unit == "F":
        return modules.cel2f(temperature)
    return temperature


def change_theme() -> None:
    new_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
    ctk.set_appearance_mode(new_mode)
    theme_button.configure(text=f"{'Dark' if new_mode == 'Light' else 'Light'} theme")

    background = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
    if isinstance(background, (tuple, list)):
        background = background[1 if new_mode == "Dark" else 0]
    temperature_plot.configure(
        background=background,
    )
    plot_colors["text"] = "#eeeeee" if new_mode == "Dark" else "#333333"
    draw_temperature_plot(plot_state["forecast"], plot_state["unit"])


tempbutton.configure(command=refresh_temperatures)
theme_button.configure(command=change_theme)

searchbutton = ctk.CTkButton(searchframe, text="Search", command=search, width=80)
searchbutton.grid(row=0, column=2, padx=(6, 12), pady=12)
app.bind("<Return>", lambda *_: searchbutton.invoke())

app.mainloop()
