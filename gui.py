import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb  # Import ttkbootstrap for styling
from ttkbootstrap.tableview import Tableview
import weather_api as weather
from database import DataBase
from PIL import Image, ImageTk  # for icons


class WeatherApp(ttk.Frame):
    def __init__(self, master=None, db_name="weather_app.db"):
        super().__init__(master)
        self.master = master

        # initiating DB
        self.db = DataBase(db_name)

        self.configure_gui()

        self.user_input = None
        self.is_default = tb.IntVar(master=self, value=0)

        # check for default city in DB if doesn't exist, pop up cities_popup
        if self.db.get_default():
            default_city = self.db.get_default()
            self.is_default = tb.IntVar(value=default_city[0])
            self.city_name = default_city[1]
            self.state_name = default_city[2]
            self.country_name = default_city[3]
            self.cords = (default_city[4], default_city[5])

            self.create_widgets()
        else:
            # if default city is set, create main screen directly
            self.default_city = 0
            self.mand_city_search()

    def configure_gui(self):
        self.master.iconbitmap("assets/favicon.ico")
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def _get_index(self, event=None):
        # storing user choice
        selected = self.city_table.view.selection()
        if selected:
            # extracting values from first selected row
            values = self.city_table.view.item(selected[0], "values")

        self.index = int(values[0]) - 1
        self.popup.destroy()

    def _get_input(self, event=None):
        # moving entered value to user_input before clearing the entry
        if self.entry1.get():
            self.user_input = self.entry1.get()
            self.entry1.delete(0, tk.END)
        return self.user_input

    def _get_tl_input(self, event=None):
        if self.tl_entry1.get():
            self.user_input = self.tl_entry1.get()
            self.tl_entry1.delete(0, tk.END)
            self.cities_popup()
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
        # checking to see if popup windows already exists:
        if hasattr(self, "popup") and self.popup.winfo_exists():
            # clear existing content and create those widgets later down the line
            # rather than opening a new popup window
            for widget in self.popup.winfo_children():
                widget.destroy()

        # create a new popup window only if it doesn't exist
        else:
            self.popup = tb.Toplevel(
                title="Choose your City",
                size=(1200, 800),
                position=(150, 88),
            )

        # City search bar, if user needs to search for a city again
        tl_search_frame = tb.Labelframe(
            self.popup, text="City Search", takefocus=True, style="success"
        )
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
        header = ["Index", "City Name", "State", "Country", "Latitude", "Longitude"]
        filtered_city_data = [
            (city[0], city[1], city[2], city[3], city[4], city[5])
            for city in self.cities
        ]
        self.city_table = Tableview(
            self.popup,
            coldata=header,
            rowdata=filtered_city_data,
            bootstyle="success",
            autoalign=True,
        )
        self.city_table.pack(padx=20, pady=20)
        self.city_table.view.bind("<ButtonRelease-1>", self._get_index)

        # Enter widget to get the user choice index
        # index_frame = tb.Labelframe(
        #     self.popup,
        #     text="Enter the index of the city",
        #     style="success",
        # )
        # index_frame.pack(padx=20, ipadx=20)
        # self.index_entry = ttk.Entry(
        #     index_frame, justify="center", font=("Poppins", 16)
        # )
        # self.index_entry.pack()
        # self.index_entry.bind("<Return>", self._get_index)
        self.wait_window(self.popup)

        # Storing values
        self.city_name = self.cities[self.index][1]
        self.state_name = self.cities[self.index][2]
        self.country_name = self.cities[self.index][3]
        self.cords = (self.cities[self.index][4], self.cities[self.index][5])
        self.is_default = tb.IntVar(value=0)

        self.create_widgets()

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

    def select_city(self, event=None):
        selected_city = self.saved_table.view.selection()
        if selected_city:
            # extracting values from first selected row
            values = self.saved_table.view.item(selected_city[0], "values")

            # updating values
            self.city_name = values[0]
            self.state_name = values[1]
            self.country_name = values[2]
            self.is_default = tb.IntVar(value=values[3])
            self.cords = (values[4], values[5])

        self.saved_frame.destroy()
        self.create_widgets()

    def saved_locations(self, event=None):
        self.saved_frame = tb.Toplevel(
            title="Saved Locations",
            size=(850, 550),
            position=(300, 225),
            transient=self.master,
        )
        self.saved_frame.config(bg="#34495e")

        header = ["City Name", "State", "Country", "Default", "Latitude", "Longitude"]
        saved = self.db.get_cities()
        self.saved_table = Tableview(
            self.saved_frame,
            coldata=header,
            rowdata=saved,
            bootstyle="success",
            autoalign=True,
        )
        self.saved_table.pack(padx=40, pady=20)
        self.saved_table.view.bind("<ButtonRelease-1>", self.select_city)

    def default_op(self, cords):
        # setting current city as default if button checked
        if self.is_default.get() == 1:
            self.db.set_default(cords)
        # removing current city as default if button unchecked
        elif self.is_default.get() == 0:
            self.db.remove_default(cords)

    def create_widgets(self):
        # ------ Main Container Frame ------
        # First checking to see if main frame already exists:
        if hasattr(self, "main_frame") and self.main_frame.winfo_exists():
            # Reloading main frame so content gets updated
            for widget in self.main_frame.winfo_children():
                widget.destroy()

        # no pre-existing main frame, meaning it is getting called the first time
        else:
            self.main_frame = ttk.Frame(self, padding=10)
            self.main_frame.pack(fill=tk.BOTH, expand=True)

        # getting weather data
        self.weather_data = weather.get_weather(self.cords)

        # ****** Search Frame ******
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(pady=5, fill="x")

        # *** Sub search: App name ***
        name_frame = ttk.Frame(search_frame)
        name_frame.pack(side="left", padx=20)
        ttk.Label(
            name_frame,
            text="OUTSIDE?",
            font=("Poppins", 20, "bold"),
            justify="center",
        ).pack()
        ttk.Label(
            name_frame,
            text="a weather app",
            font=("Poppins", 10, "italic"),
            justify="center",
        ).pack()

        # *** Sub Search: search city ***
        search_box_frame = ttk.Frame(search_frame)
        search_box_frame.pack(side="top", anchor="center", pady=10, expand=True)

        self.entry1 = ttk.Entry(search_box_frame, font=("Poppins", 14), width=40)
        self.entry1.pack(side="left", padx=10, ipady=5)

        # Sub Search: getting info for city search
        self.entry1.bind(
            "<Return>", lambda event: (self._get_input(), self.cities_popup())
        )
        ttk.Button(
            search_box_frame,
            text="Search",
            bootstyle="success-outline",
            command=lambda event=None: (self._get_input(), self.cities_popup()),
        ).pack(side="left", padx=10)

        # Save button to save current city
        ttk.Button(
            search_box_frame,
            text="Save 📑",
            bootstyle="success-outline",
            command=lambda event=None: self.db.add_city(self.cities[self.index]),
        ).pack(side="left", padx=10)

        # Spacer
        ttk.Frame(search_box_frame, width=100).pack(side="left")

        # Set current city as default button
        self.check_button = tb.Checkbutton(
            search_box_frame,
            text="Set as Default",
            variable=self.is_default,
            bootstyle="success-round-toggle",
            command=lambda: self.default_op(self.cords),
        )
        self.check_button.pack(side="left", padx=10)

        # Sub Search: Saved locations
        button1 = ttk.Button(
            search_box_frame,
            text="Saved Locations",
            bootstyle="success-outline",
            command=self.saved_locations,
        )
        button1.pack(side="left", padx=10, pady=10)

        # ------ City & Weather Info Frame ------
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        # ****** City info frame ******
        city_frame = tk.LabelFrame(info_frame, text="City Info", width=480, height=330)
        city_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        city_frame.grid_propagate(False)
        city_frame.pack_propagate(False)
        ttk.Label(
            city_frame,
            text=self.city_name,
            font=("Poppins", 28, "bold"),
        ).pack(pady=(65, 0))
        ttk.Label(
            city_frame,
            text=self.state_name,
            font=("Poppins", 18, "bold"),
        ).pack(pady=10)
        ttk.Label(
            city_frame,
            text=self.country_name,
            font=("Poppins", 18, "bold"),
        ).pack()

        # ****** current weather info frame ******
        weather_frame = tk.LabelFrame(
            info_frame, text="Weather Info", width=870, height=330
        )
        weather_frame.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        weather_frame.grid_propagate(False)
        weather_frame.pack_propagate(False)

        # storing current weather data
        current = self.weather_data.Current()
        cur_time = current.Time()
        cur_temp = current.Variables(0).Value()
        cur_humidity = current.Variables(1).Value()
        cur_act_temp = current.Variables(2).Value()
        cur_day = current.Variables(3).Value()
        cur_wind = current.Variables(4).Value()

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

        # ------ Forecast Frames ------
        forecast_frame = ttk.Frame(self.main_frame)
        forecast_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ****** Daily forecast frame ******
        day_frame = tk.LabelFrame(forecast_frame, text="", width=510, height=370)
        day_frame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        day_frame.grid_propagate(False)
        day_frame.pack_propagate(False)

        # daily forecast data
        daily = self.weather_data.Daily()
        # Variables(0) = temp, Variables(1) = wind; Values for each day
        daily_data = [
            (daily.Variables(0).Values(i), daily.Variables(1).Values(i))
            for i in range(7)
        ]
        ttk.Label(
            day_frame,
            text="7 Days Forecast from today:",
            font=("Poppins", 18, "bold"),
        ).pack(anchor="w", pady=(5, 10), padx=5)

        for i, (daily_temp, daily_wind) in enumerate(daily_data):
            ttk.Label(
                day_frame,
                text=f" ⁘ Day{i+1}    🌤 Temp: {daily_temp:.1f}℃    💨 Wind: {daily_wind:.1f}km/h",
                font=("Poppins semibold", 12),
            ).pack(anchor="center", pady=5)

        # ****** Hourly data frame ******
        hourly = self.weather_data.Hourly()
        hourly_frame = tk.LabelFrame(forecast_frame, text="", width=870, height=370)
        hourly_frame.grid(row=0, column=1, padx=5, pady=5)
        hourly_frame.grid_propagate(False)
        hourly_frame.pack_propagate(False)
        ttk.Label(
            hourly_frame,
            text="Hourly Forecast (for each hour):",
            font=("Poppins", 18, "bold"),
        ).pack(fill="x", padx=(10,), pady=(10, 20))

        # Variable(0) = temp, Variable(1) = actual temp, Variable(2) = wind -> (i)
        # Values for 6 hour forecast -> (j)
        hourly_data = [
            [hourly.Variables(i).Values(j) for j in range(6)] for i in range(3)
        ]

        # reformating so labeling is easier
        for i in range(len(hourly_data[0])):  # Iterate over columns (hours)
            temp = hourly_data[0][i]
            act_temp = hourly_data[1][i]
            wind = hourly_data[2][i]

            formatted_hourly = f"🌤  Temp: {temp:.1f}°C \t   🌡  Feels: {act_temp:.1f}°C \t   💨  Wind: {wind:.1f}km/h"

            ttk.Label(
                hourly_frame, text=f"{formatted_hourly}", font=("Poppins semibold", 12)
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
