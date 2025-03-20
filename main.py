import gui
import ttkbootstrap as tb
import tkinter as tk


def get_window_size():
    """Returns an appropriate window size based on screen resolution."""
    temp = tk.Tk()
    scr_width = temp.winfo_screenwidth()
    scr_height = temp.winfo_screenheight()
    temp.destroy()

    # Adjust size of the window incase the screen size if smaller than the window size
    width = min(1500, int(scr_width * 0.95))
    height = min(976, int(scr_height * 0.9))

    return width, height


def initialize_gui():
    """Initializes and returns the main application window which can be used in main to launch app UI."""
    width, height = get_window_size()
    return tb.Window(
        themename="solar",
        title="Outside?",
        size=(width, height),
        position=(0, 0),
        iconphoto=None,
    )


def main():
    get_window_size()
    root = initialize_gui()
    app = gui.WeatherApp(root)
    app.pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()
