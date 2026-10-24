import argparse
import tkinter as tk

import customtkinter as ctk
import requests

import modules

API_KEY = "12383b48d66ef5a9ab3d48e9b393fdba"
BOX_WIDTH = 78


def draw_box(title: str, lines: list[str]) -> None:
    print(f"+- {title} ".ljust(BOX_WIDTH - 1, "-") + "+")
    for line in lines:
        print(f"| {line[:BOX_WIDTH - 4]:<{BOX_WIDTH - 4}} |")
    print(f"+{'-' * (BOX_WIDTH - 2)}+")


def run_tui() -> None:
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
        code = error.response.status_code if error.response else None
        if code == 404:
            print(f"City not found: {city}")
        elif code == 401:
            print("OpenWeatherMap rejected the API key.")
        else:
            print(f"Weather request failed (HTTP {code}).")
        return
    except requests.RequestException:
        print("Could not connect to OpenWeatherMap. Check the connection and try again.")
        return
    except (KeyError, IndexError, TypeError, ValueError) as error:
        print(f"Could not read weather data: {error}")
        return

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
            f"Temperature: {report['temperature']:.1f} {unit}"
            f"    Feels like: {report['feels_like']:.1f} {unit}",
            f"Low: {report['minimum']:.1f} {unit}"
            f"    High: {report['maximum']:.1f} {unit}",
            f"Humidity: {report['humidity']}%"
            f"    Pressure: {report['pressure']} hPa",
            f"Wind: {report['windspeed']} m/s {report['winddir']}"
            f"    Visibility: {report['visibility_km']} km",
        ],
    )

    rows = [
        f"{'DATE / TIME':<19} {'TEMP':>9}  {'CONDITIONS':<27} {'RAIN':>6}",
        "-" * (BOX_WIDTH - 4),
    ]
    for item in forecast:
        rows.append(
            f"{item['time']:<19} {item['temperature']:>6.1f} {unit}  "
            f"{item['description'][:27]:<27} {item['rain_chance']:>5}%"
        )
    if not forecast:
        rows.append("No forecast data available.")
    draw_box("FORECAST - NEXT FIVE 3-HOUR SLOTS", rows)
    print()


def run_gui() -> None:
    app = ctk.CTk()
    app.title("Weather")
    app.geometry("1200x680")
    app.resizable(False, False)
    app.grid_columnconfigure(0, weight=5, minsize=550)
    app.grid_columnconfigure(1, weight=6, minsize=600)
    app.grid_rowconfigure(3, weight=1)

    ctk.CTkLabel(
        app,
        text="Weather",
        font=("Segoe UI", 30, "bold"),
    ).grid(row=0, column=0, columnspan=2, pady=(4, 1))

    theme_button = ctk.CTkButton(app, text="Light theme", width=95, height=28)
    theme_button.place(relx=0.985, rely=0.025, anchor="ne")

    search_frame = ctk.CTkFrame(app)
    search_frame.grid(row=1, column=0, columnspan=2, padx=12, pady=2, sticky="ew")
    search_frame.grid_columnconfigure(0, weight=1)
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city name")
    search_entry.grid(row=0, column=0, padx=(10, 6), pady=8, sticky="ew")
    unit_button = ctk.CTkSegmentedButton(search_frame, values=["C", "F"])
    unit_button.grid(row=0, column=1, padx=6, pady=8)
    unit_button.set("C")

    status = ctk.CTkLabel(app, text="Search for a city to see its weather.")
    status.grid(row=2, column=0, columnspan=2, padx=12, pady=(0, 2))

    cards = ctk.CTkFrame(app, fg_color="transparent")
    cards.grid(row=3, column=0, padx=(8, 3), pady=(0, 8), sticky="nsew")
    cards.grid_columnconfigure(0, weight=1)
    cards.grid_columnconfigure(1, weight=1)
    cards.grid_rowconfigure(0, weight=1)
    cards.grid_rowconfigure(1, weight=1)
    values: dict[str, ctk.CTkLabel] = {}
    sections = (
        ("Overview", (("location", "Location"), ("description", "Weather"))),
        (
            "Temperature",
            (
                ("temperature", "Current"),
                ("feels_like", "Feels like"),
                ("minimum", "Minimum"),
                ("maximum", "Maximum"),
            ),
        ),
        ("Conditions", (("humidity", "Humidity"), ("pressure", "Pressure"))),
        (
            "Wind & visibility",
            (
                ("windspeed", "Wind speed"),
                ("winddir", "Wind direction"),
                ("visibility", "Visibility"),
            ),
        ),
    )

    for index, (title, fields) in enumerate(sections):
        row, column = divmod(index, 2)
        section = ctk.CTkFrame(cards)
        section.grid(row=row, column=column, padx=3, pady=3, sticky="nsew")
        section.grid_columnconfigure(0, minsize=105)
        section.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            section, text=title, font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, padx=9, pady=(5, 2), sticky="w")

        for field_row, (key, label) in enumerate(fields, start=1):
            ctk.CTkLabel(section, text=label, font=("Arial", 14)).grid(
                row=field_row, column=0, padx=9, pady=2, sticky="w"
            )
            value = ctk.CTkLabel(
                section,
                text="--",
                anchor="w" if key in ("winddir", "visibility") else "e",
                font=("Arial", 14, "bold"),
            )
            value.grid(row=field_row, column=1, padx=9, pady=2, sticky="ew")
            values[key] = value

    forecast_frame = ctk.CTkFrame(app)
    forecast_frame.grid(row=3, column=1, padx=(3, 12), pady=(0, 8), sticky="nsew")
    forecast_frame.grid_columnconfigure(0, weight=1)
    forecast_frame.grid_rowconfigure(1, weight=1)
    ctk.CTkLabel(
        forecast_frame,
        text="Next five 3-hour forecasts",
        font=("Segoe UI", 19, "bold"),
    ).grid(row=0, column=0, padx=12, pady=(8, 6), sticky="w")

    background = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
    if isinstance(background, (tuple, list)):
        background = background[1 if ctk.get_appearance_mode() == "Dark" else 0]
    graph_text = {
        "color": "#eeeeee" if ctk.get_appearance_mode() == "Dark" else "#333333"
    }
    canvas = tk.Canvas(
        forecast_frame,
        width=600,
        height=1,
        background=background,
        highlightthickness=0,
    )
    canvas.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
    state = {"report": None, "forecast": [], "unit": "°C"}

    def draw_graph() -> None:
        canvas.delete("all")
        forecast = state["forecast"]
        if not forecast:
            canvas.create_text(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2,
                text="No forecast data",
                fill=graph_text["color"],
            )
            return

        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 2 or height < 2:
            return
        left, right, top, bottom = 38, width - 18, 48, max(86, height - 106)
        temps = [
            modules.convert_temperature(item["temperature"], unit_button.get())
            for item in forecast
        ]
        low = min(temps)
        spread = max(temps) - low or 1
        points = []
        for index, temperature in enumerate(temps):
            x = left + (right - left) * (index + 0.5) / len(temps)
            y = bottom - (temperature - low) / spread * (bottom - top - 32) - 16
            points.extend((x, y))

        for y in (top, (top + bottom) / 2, bottom):
            canvas.create_line(left, y, right, y, fill="#656b75", dash=(3, 3))
        canvas.create_line(*points, fill="#42a5f5", width=5, smooth=True)
        column_width = (right - left) / len(forecast) - 4
        for index, item in enumerate(forecast):
            x, y = points[index * 2], points[index * 2 + 1]
            canvas.create_oval(
                x - 6, y - 6, x + 6, y + 6,
                fill="#42a5f5", outline="#ffffff", width=2,
            )
            canvas.create_text(
                x, y - 20, text=f"{temps[index]:.1f}°",
                fill=graph_text["color"], font=("Arial", 14, "bold"),
            )
            canvas.create_text(
                x, bottom + 18, text=item["time"][5:16],
                fill=graph_text["color"], font=("Arial", 12, "bold"),
                justify="center", width=column_width,
            )
            canvas.create_text(
                x, bottom + 43, text=item["description"],
                fill=graph_text["color"], font=("Arial", 12),
                justify="center", width=column_width,
            )
            canvas.create_text(
                x, bottom + 69, text=f"Rain {item['rain_chance']}%",
                fill=graph_text["color"], font=("Arial", 12, "bold"),
            )

    def refresh_weather(unit: str | None = None) -> None:
        report = state["report"]
        if report is None:
            return
        selected_unit = unit or unit_button.get()
        degree_unit = f"°{selected_unit}"
        values["location"].configure(
            text=f"{report['city']}, {report['country']}"
        )
        values["description"].configure(text=report["description"])
        for key in ("temperature", "feels_like", "minimum", "maximum"):
            converted = modules.convert_temperature(report[key], selected_unit)
            values[key].configure(text=f"{converted:.1f} {degree_unit}")
        values["humidity"].configure(text=f"{report['humidity']}%")
        values["pressure"].configure(text=f"{report['pressure']} hPa")
        values["windspeed"].configure(text=f"{report['windspeed']} m/s")
        values["winddir"].configure(
            text=report["winddir"].split("(")[-1].rstrip(")")
        )
        values["visibility"].configure(text=f"{report['visibility_km']} km")
        state["unit"] = degree_unit
        draw_graph()

    def search() -> None:
        city = search_entry.get().strip()
        if not city:
            status.configure(text="Enter a city name first.")
            return
        status.configure(text="Loading weather...")
        app.update_idletasks()
        try:
            report = modules.get_weather(city, API_KEY, "C")
            forecast = modules.get_forecast(city, API_KEY, "C")
        except requests.HTTPError as error:
            code = error.response.status_code if error.response else None
            status.configure(
                text=f"City not found: {city}."
                if code == 404 else
                "OpenWeatherMap rejected the API key."
                if code == 401 else
                f"Weather request failed (HTTP {code})."
            )
            return
        except requests.RequestException:
            status.configure(text="Could not connect to OpenWeatherMap.")
            return
        except (KeyError, IndexError, TypeError, ValueError) as error:
            status.configure(text=str(error) or "OpenWeatherMap returned invalid data.")
            return
        state["report"] = report
        state["forecast"] = forecast
        refresh_weather()
        status.configure(text="Weather updated.")

    def toggle_theme() -> None:
        mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(mode)
        theme_button.configure(text=f"{'Dark' if mode == 'Light' else 'Light'} theme")
        frame_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        if isinstance(frame_color, (tuple, list)):
            frame_color = frame_color[1 if mode == "Dark" else 0]
        canvas.configure(background=frame_color)
        graph_text["color"] = "#eeeeee" if mode == "Dark" else "#333333"
        draw_graph()

    canvas.bind("<Configure>", lambda *_: draw_graph())
    unit_button.configure(command=refresh_weather)
    theme_button.configure(command=toggle_theme)
    ctk.CTkButton(search_frame, text="Search", command=search, width=80).grid(
        row=0, column=2, padx=(6, 12), pady=8
    )
    app.bind("<Return>", lambda *_: search())
    app.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Weather in a GUI or terminal.")
    parser.add_argument("--tui", action="store_true", help="use terminal mode")
    if parser.parse_args().tui:
        run_tui()
    else:
        run_gui()


if __name__ == "__main__":
    main()
