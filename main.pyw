import tkinter as tk
from importlib import reload
import sys
import os
import atexit

from word_ass import word_ass
from short_chain import short_chain
from words_chains import words_chains


exercises_libs = {word_ass : "#ffc9c9", short_chain : '#e0ffff', words_chains : '#e1ffe0'}
BACKGROUNG = '#fff3d1'

class MainFrame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.exercise_frame = None

        self.create_widgets()
    
    def create_widgets(self):
        menu_frame = tk.Frame(self, bg=BACKGROUNG)
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for index, lib in enumerate(exercises_libs.keys()):
            ex_button = tk.Button(menu_frame, text=lib.EXERCISE_NAME, width=20)
            ex_button.configure(font=('Arial 16'), bg=exercises_libs[lib])
            ex_button.configure(command=lambda lib=lib: self.create_exercise(exercise_lib=lib))
            ex_button.grid(row=index, pady=10, sticky='swen')
        
    def create_exercise(self, exercise_lib):
        self.pack_forget()

        reload(exercise_lib)
        self.exercise_frame = exercise_lib.Exercise_GUI(self.master, main_menu=self, bg=exercises_libs[exercise_lib])
        self.exercise_frame.pack(fill=tk.BOTH, expand=True)

    def display_main_menu(self):
        if self.exercise_frame:
            self.exercise_frame.destroy()

        self.pack(fill=tk.BOTH, expand=True)
    
    def exit(self):
        sys.exit()

if __name__ == "__main__":
    
    root = tk.Tk()

    height = 675
    width = 650
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    
    root.geometry(f"{width}x{height}+{screen_w//2 - width//2}+{screen_h//2 - height//2}")
    root.resizable(False, False)
    root.title('Ассоциации')

    main_frame = MainFrame(root, bg=BACKGROUNG)
    main_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()