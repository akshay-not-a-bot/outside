import requests
import json


def get_cordinates(city: str):
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


def main():
    city = input("Enter city name: ").strip()
    cords = get_cordinates(city)


if __name__ == "__main__":
    main()
