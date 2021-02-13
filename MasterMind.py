from mvc.Controller import Controller
from tkinter import *


# Useful to restart the game
class MasterMind:

    def __init__(self):
        self.root = Tk()
        self.app = Controller(self.root)
        self.root.mainloop()
