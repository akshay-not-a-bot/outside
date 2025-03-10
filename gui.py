import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb  # Import ttkbootstrap for styling
from ttkbootstrap.tableview import Tableview
import weather_api as weather
from database import DataBase
from PIL import Image, ImageTk  # for icons


class WeatherApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # initiating DB
        self.db = DataBase()
        # check for default city in DB if doesn't exist, pop up cities_popup
        self.user_input = None

        if not self.db.get_default():
            self.mand_city_search()

        self.configure_gui()

        self.create_widgets()

    def configure_gui(self):
        self.master.iconbitmap("assets/favicon.ico")
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # private function, only to be used in index_entry.bind

    def _get_index(self, event=None):
        # storing user choice
        self.index = int(self.index_entry.get())
        self.popup.destroy()

    def _get_input(self, event=None):
        # moving entered value to user_input before clearing the entry
        if self.entry1.get():
            self.user_input = self.entry1.get()
            self.entry1.delete(0, tk.END)

    def _get_tl_input(self, event=None):
        if self.tl_entry1.get():
            self.user_input = self.tl_entry1.get()
            self.tl_entry1.delete(0, tk.END)
        return self.user_input

    def _get_mand_input(self, event=None):
        if self.mand_entry.get():
            self.user_input = self.mand_entry.get()
            self.mand_entry.delete(0, tk.END)
            self.cities_popup()
        self.temp_frame.destroy()
        return self.user_input

    # function to search & select city by user in a Toplevel window
    def cities_popup(self, event=None):
        self.popup = tb.Toplevel(
            title="Choose your City",
            size=(1200, 800),
            position=(150, 88),
        )

        # City search bar, if user needs to search for a city again
        tl_search_frame = tb.Labelframe(self.popup, takefocus=True, style="success")
        tl_search_frame.pack(padx=20, pady=20)

        self.tl_entry1 = ttk.Entry(
            tl_search_frame, font=("Arial", 16), justify="center"
        )
        self.tl_entry1.pack(side=tk.LEFT, padx=(5, 10), pady=10)
        self.tl_entry1.pack_propagate(False)
        self.tl_entry1.configure(width=25)
        self.tl_entry1.bind("<Return>", self._get_tl_input)
        ttk.Button(
            tl_search_frame,
            text="Search",
            bootstyle="success-outline",
            command=self._get_tl_input,
        ).pack(side=tk.LEFT, padx=(10, 5), pady=10)

        # getting cities list
        self.cities = weather.get_city(self.user_input)

        # creating table for cities

        header = ["Index", "City Name", "State", "Country"]
        filtered_city_data = [
            (city[0], city[1], city[2], city[3]) for city in self.cities
        ]
        city_table = Tableview(
            self.popup,
            coldata=header,
            rowdata=filtered_city_data,
            bootstyle="success",
            autoalign=True,
        )
        city_table.pack(padx=20, pady=20)

        # Enter widget to get the user choice index
        index_frame = tb.Labelframe(
            self.popup,
            text="Enter the index of the city",
            style="success",
        )
        index_frame.pack(padx=20, ipadx=20)
        self.index_entry = ttk.Entry(
            index_frame, justify="center", font=("Poppins", 16)
        )
        self.index_entry.pack()
        self.index_entry.bind("<Return>", self._get_index)
        self.popup.wait_window()
        # getting cordinates
        cords = weather.get_cordinates(self.cities, self.index)
        # getting weather data
        self.weather_data = weather.get_weather(cords)

    # mandatory city search if there is no default city set
    def mand_city_search(self):
        self.temp_frame = tb.Toplevel(
            title="Enter city",
            size=(850, 550),
            position=(300, 225),
            transient=self.master,
        )
        self.temp_frame.config(bg="#34495e")
        labelframe1 = tb.LabelFrame(
            self.temp_frame,
            text="No default city found, please search for a city",
            bootstyle="warning",
        )
        labelframe1.pack(pady=50)
        self.mand_entry = ttk.Entry(
            labelframe1, font=("Poppins", 16, "bold"), justify="center"
        )
        self.mand_entry.pack(side="left", padx=20, pady=10)
        self.mand_entry.bind("<Return>", self._get_mand_input)
        ttk.Button(
            labelframe1,
            text="Search",
            bootstyle="warning-outline",
            command=self._get_mand_input,
        ).pack(side="right", padx=20, pady=10)

        self.master.wait_window(self.temp_frame)

    def create_widgets(self):
        # Main Container Frame
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        # Sub search: App name
        name_frame = ttk.Frame(search_frame)
        name_frame.pack(side="left", anchor="nw")
        ttk.Label(
            name_frame,
            text="OUTSIDE?",
            font=("Poppins", 20, "bold"),
            justify="center",
        ).grid(row=0, column=0, sticky="NSEW")
        ttk.Label(
            name_frame,
            text="a weather app",
            font=("Poppins", 10, "italic"),
            justify="center",
        ).grid(row=1, column=0, sticky="NSEW", padx=(25, 0))

        # Sub Search: search city
        self.entry1 = ttk.Entry(search_frame, font=("Arial", 14))
        self.entry1.pack(side=tk.LEFT, padx=10, ipadx=40, pady=10)
        self.entry1.pack_propagate(False)
        self.entry1.configure(width=50)

        # Sub Search: getting info for city search
        self.entry1.bind(
            "<Return>", lambda event: (self.cities_popup(), self._get_input())
        )
        ttk.Button(
            self.entry1,
            text="Search",
            bootstyle="success-outline",
            command=lambda: (self.cities_popup(), self._get_input()),
        ).pack(side="right")

        # storing current weather data
        current = self.weather_data.Current()
        cur_time = current.Time()
        cur_temp = current.Variables(0).Value()
        cur_humidity = current.Variables(1).Value()
        cur_act_temp = current.Variables(2).Value()
        cur_day = current.Variables(3).Value()
        cur_wind = current.Variables(4).Value()

        # Sub Search: Saved location
        button1 = ttk.Button(
            search_frame, text="Saved Locations", bootstyle="success-outline"
        )
        button1.pack(side=tk.RIGHT, padx=30, pady=10)

        # City & Weather Info Frame
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        city_frame = tk.LabelFrame(info_frame, text="City Info", width=510, height=330)
        city_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        city_frame.grid_propagate(False)
        city_frame.pack_propagate(False)
        ttk.Label(
            city_frame,
            text=self.cities[self.index - 1][1],
            font=("Poppins", 28, "bold"),
        ).pack(pady=(80, 0))
        ttk.Label(
            city_frame,
            text=self.cities[self.index - 1][2],
            font=("Poppins", 18, "bold"),
        ).pack()
        ttk.Label(
            city_frame,
            text=self.cities[self.index - 1][3],
            font=("Poppins", 18, "bold"),
        ).pack()

        # current weather info frame
        weather_frame = tk.LabelFrame(
            info_frame, text="Weather Info", width=780, height=330
        )
        weather_frame.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        weather_frame.grid_propagate(False)
        weather_frame.pack_propagate(False)
        # temp
        ttk.Label(
            weather_frame,
            text=f"{cur_temp:.1f}°C",
            font=("Poppins", 40, "italic"),
        ).grid(row=0, column=0, sticky="w", padx=30, pady=(50, 0))
        # actual temp
        ttk.Label(
            weather_frame,
            text=f"Feels like {cur_act_temp:.1f}°C",
            font=("Poppins", 14, "italic"),
            justify="center",
        ).grid(row=1, column=0, sticky="w", padx=35)
        # Day / Night icon
        try:
            if cur_day == 1:
                img = Image.open("assets/day.png").resize((150, 150))
                dn_text = "Day"
            elif cur_day == 0:
                img = Image.open("assets/night.png").resize((150, 150))
                dn_text = "Night"
            self.icon = ImageTk.PhotoImage(img)
        except Exception as e:
            print("Error loading image: ", e)
        icon_label = ttk.Label(weather_frame, image=self.icon)
        icon_label.grid(row=0, column=1, padx=20, pady=20)

        # Day / Night label
        ttk.Label(
            weather_frame,
            text=dn_text,
            font=("Poppins semibold", 20),
        ).grid(row=1, column=1, padx=20)

        # Other info
        other_frame = ttk.Frame(weather_frame)
        other_frame.grid(row=0, column=2, rowspan=2, padx=(40, 0), pady=50)

        info_labels = [
            ("💦 Humidity  ", f"{cur_humidity}%"),
            ("💨 Wind  ", f"{cur_wind:.1f}km/h"),
        ]

        for i, (text, value) in enumerate(info_labels):
            ttk.Label(other_frame, text=text, font=("Poppins", 14, "bold")).grid(
                row=i, column=0, sticky="w"
            )
            ttk.Label(other_frame, text=value, font=("Poppins", 12)).grid(
                row=i, column=1, sticky="w"
            )

        # Forecast Frames
        forecast_frame = ttk.Frame(self.main_frame)
        forecast_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 6 day data
        five_day_frame = tk.LabelFrame(forecast_frame, text="", width=420, height=370)
        five_day_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        five_day_frame.grid_propagate(False)
        five_day_frame.pack_propagate(False)
        ttk.Label(
            five_day_frame, text="5 Days Forecast:", font=("Poppins", 24, "bold")
        ).pack(anchor="w")
        for day in [
            "20°C  Friday, 1 Sep",
            "22°C  Saturday, 2 Sep",
            "27°C  Sunday, 3 Sep",
            "18°C  Monday, 4 Sep",
            "16°C  Tuesday, 5 Sep",
        ]:
            ttk.Label(
                five_day_frame, text=f"☀️ {day}", font=("Poppins semibold", 16)
            ).pack(anchor="w")

        # Hourly data frame
        hourly = self.weather_data.Hourly()
        hourly_frame = tk.LabelFrame(forecast_frame, text="", width=870, height=366)
        hourly_frame.grid(row=0, column=1, padx=5, pady=5)
        hourly_frame.grid_propagate(False)
        hourly_frame.pack_propagate(False)
        ttk.Label(
            hourly_frame,
            text="Hourly Forecast(for each hour):",
            font=("Poppins", 22, "bold"),
        ).pack(fill="x", padx=(10,), pady=(10, 20))

        # Variable(0) = temp, Variable(1) = actual temp, Variable(2) = wind -> (i)
        # Values for 6 hour forecast -> (j)
        hourly_data = [
            [hourly.Variables(i).Values(j) for j in range(6)] for i in range(3)
        ]

        # reformating so labeling is easier
        for i in range(len(hourly_data[0])):  # Iterate over columns (hours)
            temp = hourly_data[0][i]  # Temperature
            act_temp = hourly_data[1][i]  # Actual Temperature
            wind = hourly_data[2][i]  # Wind Speed

            formatted_hourly = f"🌤  Temp: {temp:.1f}°C \t   🌡  Feels: {act_temp:.1f}°C \t   💨  Wind: {wind:.1f}km/h"

            ttk.Label(
                hourly_frame, text=f"{formatted_hourly}", font=("Poppins semibold", 14)
            ).pack(anchor="center", pady=5)


if __name__ == "__main__":
    root = tb.Window(
        themename="solar",
        title="Outside?",
        size=(1500, 976),
        position=(0, 0),
        iconphoto=None,
    )
    app = WeatherApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
