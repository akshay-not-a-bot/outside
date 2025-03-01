import weather_api as weather


def main():
    city = input("Enter city name: ").strip()
    cords = weather.get_cordinates(city)
    weather_data = weather.get_weather(cords)


if __name__ == "__main__":
    main()
