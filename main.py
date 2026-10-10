import customtkinter as ctk
from ui import main_window

MainWindow = getattr(main_window, "MainWindow")

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()