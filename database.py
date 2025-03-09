import sqlite3


class DataBase:

    def __init__(self):
        self.db_name = "weather_app.db"
        self._init_database()

    # manages all queries
    def _execute_query(self, query: str, params=(), fetchone=False, fetchall=False):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            # only committing if query is not for SELECT for better performance by eliminating redundant commit
            if not query.strip().upper().startswith("SELECT"):
                conn.commit()

            # if fetching was passed during calling
            if fetchone:
                return cursor.fetchone()
            elif fetchall:
                return cursor.fetchall()

    # initializes database by creating a data table
    def _init_database(self):
        query = """
        CREATE TABLE IF NOT EXISTS saved_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            country TEXT NOT NULL,
            lat REAL NOT NULL,
            long REAL NOT NULL,
            is_default INTEGER DEFAULT 0
        )
        """
        # sending this DB table create query to _execute_query so it gets executed
        self._execute_query(query)

    def add_city(self):
        # IMP logical thinking
        # need city data tuple of the user selected city from the gui.py. Go to gui.py's popup func
        # where it gets user choice index and select the city tuple using that and call this function by passing that tuple

        # DB has two tables? 1 for cities and 1 for current city's weather data

        # when application starts search databse's column "default" for 1 if no record has 1 then popup window asking user to search for city
        # alternatively, you can also cache the last searched city and show the data for that next time app opens.

        # In the Saved Locations page, give set default column (there can only be one), and select button for each city
        # which will take you to main page and app will show weather for that city.
        pass

    def delete_city(self):
        pass

    def add_weather_data(self):
        pass

    def get_weather_data(self):
        pass

    def get_cities(self):
        pass

    def set_default(self):
        # after setting a city as default, make sure there is only one default city. If not, resolve so there is only one
        pass

    def get_default(self):
        query = (
            "SELECT is_default, name, lat, long FROM saved_cities WHERE is_default = ?"
        )
        return self._execute_query(query, (1,), fetchone=True)
