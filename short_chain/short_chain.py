import tkinter as tk
from tkinter import messagebox

import timer
import exercise


EXERCISE_NAME = 'Короткий путь'

class Exercise_GUI(exercise.Exercise_GUI):
    def __init__(self, master, main_menu, cnf={}, **kw):
        exercise.Exercise_GUI.__init__(self, master, main_menu, cnf, **kw)

        self.exercise_name = EXERCISE_NAME
        self.create_widgets()

    def create_widgets(self):
        self.timer.grid(row=0, columnspan=4, pady=20)
