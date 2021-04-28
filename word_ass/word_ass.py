import tkinter as tk
from tkinter import messagebox

import timer
import exercise


EXERCISE_NAME = 'Ассоциации к слову'

class Exercise_GUI(exercise.Exercise_GUI):
    def __init__(self, master, main_menu, cnf={}, **kw):
        exercise.Exercise_GUI.__init__(self, master, main_menu, cnf, **kw)

        self.exercise_name = EXERCISE_NAME
        self.create_widgets()

    def create_widgets(self):
        self.timer.grid(row=0, columnspan=3, pady=20)

        # entries
        self.word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.word_entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.word_entry.bind('<Return>', lambda e: self.generate())
        self.word_entry.bind('<Button-3>', lambda e: self.word_entry.delete(0, tk.END))

        self.ass_entry = tk.Entry(self, width=20, font=('Arial 12 bold'), justify='center')
        self.ass_entry.grid(row=1, column=1, padx=10, sticky='w')
        self.ass_entry.bind('<Return>', lambda e: self.check_word(word=e.widget.get()))
        self.ass_entry.bind('<Button-3>', lambda e: self.ass_entry.delete(0, tk.END))

        # buttons frame
        self.create_buttons_frame().grid(row=2, column=0, pady=10, sticky='w'+'e')

        # statistic frame
        stats_frame = tk.Frame(self)
        stats_frame.grid(row=3, column=0, padx=10, pady=10, sticky='n')

        total_label = tk.Label(stats_frame, bg=self.bg, text='Осталось:', font=('Arial 12 bold'), justify='left')
        total_label.grid(row=1, column=0, sticky='w')
        self.total_label = tk.Label(stats_frame, bg=self.bg, text='0', font=('Arial 12 bold'))
        self.total_label.grid(row=1, column=1)

        # tip text
        self.__tip_text = tk.Text(self, width=10, height=15, font=('Arial 12'), state='disabled')
        self.__tip_text.grid(row=4, column=0, padx=10, pady=10, sticky='swen')

        # right text
        self.__right_text = tk.Text(self, width=50, height=25, font=('Arial 12'), state='disabled')
        self.__right_text.grid(row=2, column=1, rowspan=3, padx=10, pady=5, sticky='n')

        # menu frame
        self.create_menu_frame().grid(row=5, columnspan=3, sticky='swen')

    def generate(self):
        if not self.word_entry.get():
            self.generate_random_words()

        try:
            self.exercise.generate_word_ass(word=self.word_entry.get())
        except:
            messagebox.showerror("Error", "Ошибочка...")
            return

        self.clear_right_text()
        self.tip_text_set(text='')
        self.ass_entry.delete(0, tk.END)
        self.recalculate_totals()
        self.ass_entry.focus()
    
    def get_generated_words(self) -> str:
        return self.word_entry.get()
    
    def generate_random_words(self):
        self.word_entry.insert(0, self.exercise.generate_random_word())
    
    def check_word(self, word):
        if not self.exercise.is_ass_word_right(ass_word=word):
            self.ass_entry.delete(0, tk.END)
            return

        self.insert_right_text(text=word)
        self.ass_entry.delete(0, tk.END)
        self.timer.add_start_time()
        self.recalculate_totals()
    
    def recalculate_totals(self):
        self.total_label['text'] = len(self.exercise.word_ass)
    
    def show_word(self):
        if self.exercise.word_ass:
            self.entry_set(entry=self.ass_entry, text=self.exercise.word_ass[0])
            self.check_word(word=self.exercise.word_ass[0])
    
    def get_tip(self):
        if self.exercise.word_ass:
            word_ass = self.exercise.get_word_ass(word=self.exercise.word_ass[0])
            short_ass = [ass for ass in word_ass if len(ass) <= 15]
            self.tip_text_set(text='\n'.join(short_ass))