from colorama import init

class Colours:
    def __init__(self):
        init()
        self.red = "\x1b[31m"
        self.green = "\x1b[32m"
        self.blue = "\x1b[34m"
        self.magenta = "\x1b[35m"
        self.yellow = "\x1b[33m"
        self.cyan = "\x1b[36m"
        self.white = "\x1b[37m"
        self.bright = "\x1b[1m"
        self.reset = "\x1b[0m"

colours=Colours()