import requests
import json
import openmeteo_requests
import requests_cache
from retry_requests import retry


def get_city(city: str):
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
            indx = 1
            cities = []
            for r in response["results"]:
                name = r["name"]
                state = r.get("admin1", "N/A")
                # using get method so default value can be assigned incase there is no key names "admin1", prevents KeyError
                country = r.get("country", "N/A")
                lat = r["latitude"]
                long = r["longitude"]
                cities.append(
                    (indx, name, state, country, lat, long)
                )  # keep a note of the sequence for indexing the touple later
                indx += 1
            # returning list of cities info in the form of touple, so other funcitons can use this and display a list/tabel of
            # the information that user can choose from by indexing the touple
            return cities
        else:
            print("City not found, please enter correct city name")
            return None

    except requests.RequestException as RE:
        print(f"Error while fetching the city: {RE}")

    except TypeError as TE:
        print(f"Enter only the index of the city: {TE}")


# this function gets cities list from get_city() and get's user picked index of the city from main
def get_cordinates(cities, p):
    pick = int(p)
    # $PRODUCTION$ printing list in terminal for testing purposes
    # print("Index    Name    State   Country")
    # for city in cities:
    #     print(f"{city[0]}.  {city[1]}    {city[2]}   {city[3]}")
    lat = cities[pick - 1][4]
    long = cities[pick - 1][5]
    return lat, long


# this funcation takes touple of cordinates: (latitude, longitude) as argument
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
    user_input = input("Enter city name: ").strip()
    cities_list = get_city(user_input)
    pick = input("Enter the index of your city ")
    cords = get_cordinates(cities_list, pick)
    weather_data = get_weather(cords)
    print(f"Temp: {weather_data.Variables(0).Value():2f}")


if __name__ == "__main__":
    main()
