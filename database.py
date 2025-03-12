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
            lat REAL UNIQUE NOT NULL,
            long REAL UNIQUE NOT NULL,
            is_default INTEGER DEFAULT 0
        )
        """
        # sending this DB table create query to _execute_query so it gets executed
        self._execute_query(query)

    def add_city(self, city):
        query = "INSERT OR IGNORE INTO saved_cities (name, state, country, lat,  long) VALUES (?,?,?,?,?)"
        params = (city[1], city[2], city[3], round(city[4], 4), round(city[5], 4))
        self._execute_query(query, params)

    def remove_default(self, cords):
        lat, long = cords
        query = "UPDATE saved_cities SET is_default = ? WHERE lat = ? AND long = ?"
        params = (0, lat, long)
        self._execute_query(query, params)

    def get_cities(self):
        query = "SELECT name, state, country, is_default, lat, long FROM saved_cities"
        return self._execute_query(query, fetchall=True)

    def set_default(self, cords):
        lat, long = cords

        # clearing all other records default to zero so there can't be two default city
        query1 = "UPDATE saved_cities SET is_default = ? WHERE is_default = ?"
        params1 = (0, 1)
        self._execute_query(query1, params1)

        # now setting passed city as default:
        query2 = "UPDATE saved_cities SET is_default = ? WHERE lat = ? AND long =?"
        params2 = (1, lat, long)
        self._execute_query(query2, params2)

    def get_default(self):
        query = "SELECT is_default, name, state, country, lat, long FROM saved_cities WHERE is_default = ?"
        params = (1,)
        return self._execute_query(query, params, fetchone=True)
