import unittest
import weather_api as weather
from database import DataBase
import os
import gc


def test_get_city():
    city = "kadi"
    if city == "kadi":
        result = weather.get_city(city)
        assert result is not None
        assert isinstance(result, list)
        assert result[0] == (1, "Kadi", "Gujarat", "India", 23.2991, 72.3336)

    city = ""
    if city == "":
        result = weather.get_city(city)
        assert result is None


def test_get_weather():
    result = weather.get_weather((23.2991, 72.3336))
    assert result is not None


class TestDatabase(unittest.TestCase):
    def setUp(self):
        db_name = "test_weather.db"
        self.db_path = db_name
        self.db = DataBase(db_name)

    def tearDown(self):
        if hasattr(self.db, "_execute_query"):
            del self.db

        # force garbage collection to free db reference to solve PermissionError
        gc.collect()

        if os.path.exists(self.db_path):
            os.remove(self.db_path)  # Now it should work!

    def test_add_and_get_city(self):
        city_data = (1, "Ahmedabad", "Gujarat", "India", 23.0258, 72.5873)
        self.db.add_city(city_data)
        cities = self.db.get_cities()
        self.assertGreater(len(cities), 0)
        self.assertIn("Ahmedabad", [city[0] for city in cities])

    def test_set_and_get_default_city(self):
        city_data = (2, "Kadi", "Gujarat", "India", 23.2991, 72.3336)
        self.db.add_city(city_data)
        self.db.set_default((23.2991, 72.3336))
        default_city = self.db.get_default()
        self.assertEqual(default_city[1], "Kadi")

    def test_remove_default(self):
        city_data = (3, "Mumbai", "Maharashtra", "India", 19.0728, 72.8826)
        self.db.add_city(city_data)
        self.db.set_default((19.0728, 72.8826))
        self.db.remove_default((19.0728, 72.8826))
        default_city = self.db.get_default()
        self.assertIsNone(default_city)


def main():
    test_get_city()
    test_get_weather()


if __name__ == "__main__":
    # For function based testing
    main()

    # For unittest testing
    unittest.main()
