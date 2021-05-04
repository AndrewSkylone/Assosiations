import tkinter as tk
from tkinter import messagebox

import timer
import exercise


EXERCISE_NAME = 'Цепочки слов'

class Exercise_GUI(exercise.Exercise_GUI):
    def __init__(self, master, main_menu, cnf={}, **kw):
        exercise.Exercise_GUI.__init__(self, master, main_menu, cnf, **kw)

        self.exercise_name = EXERCISE_NAME
        self.chain_entries = []

        self.create_widgets()

    def create_widgets(self):
        self.timer.grid(row=0, columnspan=4, pady=20)
        
        # chain entries
        self.first_word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.first_word_entry.grid(row=1, column=0, padx=10)
        self.first_word_entry.bind('<Return>', lambda e: self.generate())
        self.first_word_entry.bind('<Button-3>', lambda e: self.first_word_entry.delete(0, tk.END))
        self.chain_entries.append(self.first_word_entry)

        self.second_word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.second_word_entry.grid(row=1, column=1, padx=10)
        self.second_word_entry.bind('<Return>', lambda e: self.check_word(word=e.widget.get()))
        self.second_word_entry.bind('<Button-3>', lambda e: self.second_word_entry.delete(0, tk.END))
        self.chain_entries.append(self.second_word_entry)

        self.third_word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.third_word_entry.grid(row=1, column=2, padx=10)
        self.third_word_entry.bind('<Return>', lambda e: self.check_word(word=e.widget.get()))
        self.third_word_entry.bind('<Button-3>', lambda e: self.third_word_entry.delete(0, tk.END))
        self.chain_entries.append(self.third_word_entry)

        self.last_word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.last_word_entry.grid(row=1, column=3, padx=10)
        self.last_word_entry.bind('<Return>', lambda e: self.generate())
        self.last_word_entry.bind('<Button-3>', lambda e: self.last_word_entry.delete(0, tk.END))
        self.chain_entries.append(self.last_word_entry)

        # buttons frame
        self.create_buttons_frame().grid(row=2, pady=10, sticky='n')

        # statistic frame
        stats_frame = tk.Frame(self)
        stats_frame.grid(row=3, padx=10, pady=10, sticky='n')

        three_depths_label = tk.Label(stats_frame, bg=self.bg, text='3 слова:', font=('Arial 12 bold'), justify='left')
        three_depths_label.grid(row=1, column=0, sticky='w')
        self.three_total_depths_label = tk.Label(stats_frame, bg=self.bg, text='0', font=('Arial 12 bold'))
        self.three_total_depths_label.grid(row=1, column=1)

        four_depths_label = tk.Label(stats_frame, bg=self.bg, text='4 слова:', font=('Arial 12 bold'))
        four_depths_label.grid(row=2, column=0, sticky='w')
        self.four_total_depths_label = tk.Label(stats_frame, bg=self.bg, text='0', font=('Arial 12 bold'))
        self.four_total_depths_label.grid(row=2, column=1)

        # tip text
        self.__tip_text = tk.Text(self, width=10, height=15, font=('Arial 12'), state='disabled')
        self.__tip_text.grid(row=4, column=0, padx=10, pady=10, sticky='swen')

        # right text
        self.__right_text = tk.Text(self, width=25, height=25, font=('Arial 12'), state='disabled')
        self.__right_text.grid(row=2, column=1, rowspan=3, columnspan=3, padx=10, pady=10, sticky='swen')

        # menu frame
        self.create_menu_frame().grid(row=5, columnspan=4, sticky='swen')

    def generate(self):
        if not self.first_word_entry.get() or not self.last_word_entry.get():
            self.generate_random_words()
        
        try:
            self.exercise.generate_chains(first_word=self.first_word_entry.get(), last_word=self.last_word_entry.get())
        except:
            messagebox.showerror("Error", "Ошибочка...")
            return

        self.clear_right_text()
        self.tip_text_set(text='')
        self.clear_chain_entries()
        self.recalculate_totals()
        self.second_word_entry.focus()
    
    def generate_random_words(self):
        if not self.first_word_entry.get():
            self.first_word_entry.insert(0, self.exercise.generate_random_word())
        if not self.last_word_entry.get():
            self.last_word_entry.insert(0, self.exercise.generate_random_word())
    
    def get_generated_words(self) -> str:
        first = self.first_word_entry.get()
        last = self.last_word_entry.get()

        return f'{first} -> {last}' if first and last else ''

    def check_word(self, word):
        words_chain = self.get_entries_chain()

        if not self.exercise.is_chain_word_right(word=word, words_chain=words_chain):
            if word == self.second_word_entry.get():
                self.second_word_entry.delete(0, tk.END)
            else:
                self.third_word_entry.delete(0, tk.END)
            return

        self.third_word_entry.focus()
        self.check_chain()

    def check_chain(self):
        if self.exercise.is_chain_right(words_chain=self.get_entries_chain()):
            self.insert_right_text(', '.join(self.get_entries_chain()))
            self.recalculate_totals()
            self.clear_chain_entries()
            self.timer.add_start_time()
            self.second_word_entry.focus()

    def recalculate_totals(self):
        self.three_total_depths_label['text'] = self.exercise.get_three_depths_total()
        self.four_total_depths_label['text'] = self.exercise.get_four_depths_total()
    
    def clear_chain_entries(self):
        self.second_word_entry.delete(0, tk.END)
        self.third_word_entry.delete(0, tk.END)

    def show_word(self):
        entry_word = self.second_word_entry.get()
        words_chain = self.get_entries_chain()
        
        if not self.exercise.is_chain_word_right(word=entry_word, words_chain=words_chain):
            self.clear_chain_entries()
            tip_word = self.exercise.get_first_chain_word()
            self.second_word_entry.insert(0, tip_word)
        else:
            self.third_word_entry.delete(0, tk.END)
            tip_word = self.exercise.get_second_chain_word(words_chain=words_chain)
            self.third_word_entry.insert(0, tip_word)

        self.check_word(word=tip_word)

    def get_tip(self):
        word = self.second_word_entry.get()
        words_chain = self.get_entries_chain()

        if not self.exercise.is_chain_word_right(word=word, words_chain=words_chain):
            self.clear_chain_entries()
            word = self.exercise.get_first_chain_word()
        else:
            self.third_word_entry.delete(0, tk.END)
            word = self.exercise.get_second_chain_word(words_chain=words_chain)
        
        self.exercise.generate_word_ass(word=word)
        self.on_word_ass_set()

    def get_entries_chain(self) -> list:
        return [entry.get() for entry in self.chain_entries if entry.get()]
        
    def on_word_ass_set(self):
        word_ass = self.exercise.word_ass
        short_ass = [ass for ass in word_ass if len(ass) <= 15]
        self.tip_text_set(text='\n'.join(short_ass))