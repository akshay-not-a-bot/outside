# WeatherApp


## Description

WeatherApp is a Python-based graphical application that provides real-time weather updates and forecasts. It features a user-friendly interface built with Tkinter and ttkbootstrap, integrating Open-Meteo API to fetch weather data and an SQLite database to manage saved locations. The app allows users to check current weather conditions, save favorite cities, set a default city, and view forecasts. 

## Features

- **Search and View Weather:** Get real-time weather details for any city.
- **Hourly and 7-Day Forecast:** Get Hourly and 7-Day forecast 
- **Saved Cities Management:** Save, list, delete, and mark cities as favorites.
- **Metric Units:** Get upto-date weather info in universal Metric units

## Project Structure

### `main.py`

This is the main entry point of the application. It must be executed to run the WeatherApp. The required `main()` function is defined at the top level along with other functions. However, all of the functionality is handled in supporting modules not in this file.

### `weather_api.py`

This module handles all interactions with the Open-Meteo API, including:

- Fetching weather data based on latitude and longitude.
- Geocoding city names to coordinates.
- Returning structured weather details for display in the GUI.

### `database.py`

Manages the SQLite database, including:

- Creating and maintaining the `saved_cities` table.
- Adding, removing, and retrieving saved cities.
- Setting and getting the default city.

### `gui.py`

Implements the Tkinter-based user interface with ttkbootstrap enhancements. Key functionalities:

- Displaying weather information.
- Managing city preferences.
- Interacting with the database and API.


## Design Choices

- **Project Structure:** While the CS50 requirement mandates a top-level `main()` function in `project.py`, all the real work is done in separate modules to maintain clean and modular code.
- **Tkinter & ttkbootstrap:** Chosen for ease of GUI development while maintaining a modern look.
- **SQLite:** Provides lightweight local storage without requiring additional dependencies.
- **Open-Meteo API:** Free, accurate, and sufficient for the app’s needs.


## Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/weatherapp.git
   cd weatherapp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Acknowledgments

- Open-Meteo API for weather data.
- ttkbootstrap for UI enhancements.

