import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb


class WeatherApp(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title("Weather App")
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_widgets(self):
        # Search Frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        # Entry widget for user input
        self.entry1 = ttk.Entry(search_frame, font=("Arial", 14))
        self.entry1.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)

        # Bind Enter key to a function
        self.entry1.bind("<Return>", self.process_input)

        # Button for manual submission (optional)
        search_button = ttk.Button(
            search_frame, text="Search", command=self.process_input
        )
        search_button.pack(side=tk.RIGHT, padx=10)

    def process_input(self, event=None):
        """Function to process the input when Enter is pressed."""
        user_input = self.entry1.get()
        print(f"User entered: {user_input}")  # Replace this with your processing logic


if __name__ == "__main__":
    root = tb.Window(themename="solar")
    app = WeatherApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
