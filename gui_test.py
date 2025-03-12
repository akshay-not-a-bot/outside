from database import DataBase

db = DataBase()

default = db.get_default()
print(default)
cities = db.get_cities()
print(cities)
