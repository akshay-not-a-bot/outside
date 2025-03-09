import weather_api as weather
import gui
import ttkbootstrap as tb


def main():
    city = input("Enter city name: ").strip()
    cords = weather.get_cordinates(city)
    weather_data = weather.get_weather(cords)
    root = tb.Window(
        themename="solar",
        title="Outside?",
        size=(1500, 976),
        position=(0, 0),
        iconphoto=None,
    )
    app = gui.WeatherApp(root, cords, weather_data)
    app.mainloop()


if __name__ == "__main__":
    main()
