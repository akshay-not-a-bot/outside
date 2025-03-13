import gui
import ttkbootstrap as tb


def main():
    root = tb.Window(
        themename="solar",
        title="Outside?",
        size=(1500, 976),
        position=(0, 0),
        iconphoto=None,
    )
    app = gui.WeatherApp(root)
    app.pack(fill="both", expand=True)

    app.mainloop()


if __name__ == "__main__":
    main()
