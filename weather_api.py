import requests
import json
import openmeteo_requests
import requests_cache
from retry_requests import retry


def get_cordinates(city: str):
    # geocoding API calling
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 10, "language": "en", "format": "json"}

    try:
        response_raw = requests.get(url, params=params)
        response_raw.raise_for_status()
        response = response_raw.json()
        # $PRODUCTION$ storing data in a file to compare
        with open("response.json", "w") as data:
            json.dump(response, data, indent=4)

        if "results" in response and len(response["results"]) > 0:
            indx = 0
            for r in response["results"]:
                name = r["name"]
                state = r.get("admin1", "N/A")
                # using get method so default value can be assigned incase there is no key names "admin1", prevents KeyError
                country = r.get("country", "N/A")
                print(f"{indx}. Name: {name},   State: {state},   Country: {country}")
                indx += 1
            pick = int(input("Enter the index of your city "))
            lat = response["results"][pick]["latitude"]
            long = response["results"][pick]["longitude"]
            return lat, long

        else:
            print("City not found, please enter correct city name")
            return None

    except requests.RequestException as RE:
        print(f"Error while fetching the city: {RE}")

    except TypeError as TE:
        print(f"Enter only the index of the city: {TE}")


def get_weather(cords):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # weather API calling
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": cords[0],
        "longitude": cords[1],
        "current": ["temperature_2m", "is_day", "precipitation", "wind_speed_10m"],
        "hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "is_day"],
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Current values. The order of variables needs to be the same as requested.
        return response.Current()
        # current_temperature_2m = current.Variables(0).Value()
        # current_is_day = current.Variables(1).Value()
        # current_precipitation = current.Variables(2).Value()
        # current_wind_speed_10m = current.Variables(3).Value()

    except Exception as E:
        print(f"Error while fetching weather data: {E}")

        # NOT HANDLING HOURLY DATA AND FORECAST YET


def main():
    city = input("Enter city name: ").strip()
    cords = get_cordinates(city)
    print(cords)
    weather_data = get_weather(cords)
    print(f"Temp: {weather_data.Variables(0).Value():2f}")


if __name__ == "__main__":
    main()
