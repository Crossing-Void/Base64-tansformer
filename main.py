from Tkinter_template.base import Interface
import time

Interface.rate = 0.85


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)


if __name__ == "__main__":
    main = Main("Base64 Transformer", "favicon.ico")
    while True:
        main.canvas.update()
        time.sleep(0.02)
