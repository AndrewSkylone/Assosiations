import requests
import json
import tkinter as tk
from tkinter import messagebox
import random

import timer


class MainFrame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.assosiater = Assosiater()
        self.chain_entries = []

        self.create_widgets()
    
    def create_widgets(self):
        self.timer = timer.Timer_GUI(self, start_function=self.on_timer_start, end_fuction=self.after_timer_finished)
        self.timer.grid(row=0, columnspan=4, pady=20)

        # chain entries
        self.first_word_entry = tk.Entry(self, width=15, font=('Arial 12 bold'), justify='center')
        self.first_word_entry.grid(row=1, column=0, padx=10)
        self.first_word_entry.bind('<Return>', lambda e: self.generate_chains())
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
        self.last_word_entry.bind('<Return>', lambda e: self.generate_chains())
        self.last_word_entry.bind('<Button-3>', lambda e: self.last_word_entry.delete(0, tk.END))
        self.chain_entries.append(self.last_word_entry)

        # buttons frame
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=2, pady=10, sticky='n')

        generate_button = tk.Button(buttons_frame, text='Сгенерировать', font=('Arial 12 bold'), command=self.generate_chains)
        generate_button.grid(row=0, column=0, padx=10, sticky='w'+'e')

        tip_button = tk.Button(buttons_frame, text='Подсказка', font=('Arial 12 bold'), command=self.get_tip)
        tip_button.grid(row=1, column=0, padx=10, pady=5, sticky='w'+'e')
        
        # statistic frame
        stats_frame = tk.Frame(self)
        stats_frame.grid(row=3, padx=10, sticky='n')
        three_depths_label = tk.Label(stats_frame, text='3 слова:', font=('Arial 12 bold'), justify='left')
        three_depths_label.grid(row=1, column=0, sticky='w')
        self.three_total_depths_label = tk.Label(stats_frame, text='0', font=('Arial 12 bold'))
        self.three_total_depths_label.grid(row=1, column=1)

        four_depths_label = tk.Label(stats_frame, text='4 слова:', font=('Arial 12 bold'))
        four_depths_label.grid(row=2, column=0, sticky='w')
        self.four_total_depths_label = tk.Label(stats_frame, text='0', font=('Arial 12 bold'))
        self.four_total_depths_label.grid(row=2, column=1)
    
        self.__found_chains_text = tk.Text(self, width=25, height=25, font=('Arial 12'), state='disabled')
        self.__found_chains_text.grid(row=2, column=1, rowspan=5, columnspan=3, padx=10, pady=10, sticky='swen')

    def insert_found_chains_text(self, text):
        self.__found_chains_text.config(state='normal')
        self.__found_chains_text.insert(0.0, text + '\n')
        self.__found_chains_text.config(state='disabled')

    def generate_chains(self):
        try:
            self.assosiater.generate_chains(first_word=self.first_word_entry.get(), last_word=self.last_word_entry.get())
        except:
            messagebox.showerror("Error", "Ошибочка...")
            return

        self.clear_found_chains_text()
        self.recalculate_totals()
        self.focus_set()

    def clear_found_chains_text(self):
        self.__found_chains_text.config(state='normal')
        self.__found_chains_text.delete(0.0, tk.END)
        self.__found_chains_text.config(state='disabled')

    def check_word(self, word):
        words_chain = self.get_words_chain()

        if not self.assosiater.is_word_right(word=word, words_chain=words_chain):
            if word == self.second_word_entry.get():
                self.second_word_entry.delete(0, tk.END)
            else:
                self.third_word_entry.delete(0, tk.END)
            return

        self.check_chain()
        self.focus_set()

    def check_chain(self):
        if self.assosiater.is_chain_right(words_chain=self.get_words_chain()):
            self.insert_found_chains_text(', '.join(self.get_words_chain()))
            self.recalculate_totals()
            self.clear_chain_entries()
            self.timer.add_start_time()
    
    def recalculate_totals(self):
        self.three_total_depths_label['text'] = self.assosiater.get_three_depths_total()
        self.four_total_depths_label['text'] = self.assosiater.get_four_depths_total()
    
    def clear_chain_entries(self):
        self.second_word_entry.delete(0, tk.END)
        self.third_word_entry.delete(0, tk.END)
    
    def on_timer_start(self):
        self.assosiater.found_chains = 0
    
    def after_timer_finished(self):
        time = self.timer.last_added_time
        found_chains = self.assosiater.found_chains
        messagebox.showinfo("Статистика", f'Время: {time}\nНайдено цепочек: {found_chains}')

        self.assosiater.found_chains = 0
    
    def get_tip(self):
        if not self.assosiater.chains:
            return 

        words_chain = self.get_words_chain()
        
        if not self.assosiater.is_word_right(word=self.second_word_entry.get(), words_chain=self.get_words_chain()):
            self.clear_chain_entries()
            self.second_word_entry.insert(0, self.assosiater.get_first_tip(words_chain=words_chain))
        else:
            self.third_word_entry.delete(0, tk.END)
            self.third_word_entry.insert(0, self.assosiater.get_second_tip(words_chain=words_chain))

        self.check_chain()
    
    def get_words_chain(self) -> list:
        return [entry.get() for entry in self.chain_entries if entry.get()]

class Assosiater(object):
    def __init__(self):
       self.session = self.create_session()
       self.chains = []
       self.found_chains = 0
    
    def generate_chains(self, first_word, last_word) -> list:
        url = r'https://sociation.org/ajax/find_path/'
        self.chains.clear()

        for depth in (3, 4):
            page_data = self.session.post(url, {'word_from' : first_word, 'word_to' : last_word, 'depth' : depth})
            chains_dict = json.loads(page_data.text)

            for path in chains_dict['paths']:
                self.chains.append(path['words'])
        
    def is_word_right(self, word, words_chain) -> bool:
        if not word in words_chain:
            return False

        word_indx = words_chain.index(word) 
        for chain in self.chains:
            if words_chain[:word_indx + 1] == chain[:word_indx + 1]:
                return True
        

    def is_chain_right(self, words_chain) -> bool:
        if words_chain in self.chains:
            self.found_chains += 1
            self.chains.remove(words_chain)
            return True
            
        return False
    
    def get_first_tip(self, words_chain) -> str:
        return random.choice(self.chains)[1]

    def get_second_tip(self, words_chain) -> str:
        four_depth_chains = [chain for chain in self.chains if len(chain) == 4]
        tip_chains = [chain for chain in four_depth_chains if chain[1] == words_chain[1]]

        return random.choice(tip_chains)[2]

    def get_three_depths_total(self) -> int:
        three_depths = [chain for chain in self.chains if len(chain) == 3]
        return len(three_depths)

    def get_four_depths_total(self) -> int:
        four_depths = [chain for chain in self.chains if len(chain) == 4]
        return len(four_depths)
    
    def create_session(self) -> requests.Session:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})

        return session


if __name__ == "__main__":
    
    root = tk.Tk()

    height = 650
    width = 650
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    
    root.geometry(f"{width}x{height}+{screen_w//2 - width//2}+{screen_h//2 - height//2}")
    root.resizable(False, False)
    root.title('Assosiations')

    main_frame = MainFrame(root)
    main_frame.grid()

    root.mainloop()