import requests
import sys
import os
import json
import tkinter as tk
from tkinter import messagebox
import copy
import shelve
from datetime import datetime
from dateutil.parser import parse

import timer


class Exercise_GUI(tk.Frame):
    def __init__(self, master, main_menu, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.main_menu = main_menu
        self.bg = kw['bg']
        self.exercise_name = 'Exercise'

        self.__right_text = None
        self.__tip_text = None
        self.timer = timer.Timer_GUI(self, start_function=self.on_timer_start, stop_function=self.on_timer_stop)
        self.exercise = Exercise()

    def create_buttons_frame(self) -> tk.Frame:
        buttons_frame = tk.Frame(self, bg=self.bg)

        generate_button = tk.Button(buttons_frame, text='Сгенерировать', font=('Arial 12 bold'), command=self.generate)
        generate_button.grid(row=0, column=0, padx=10, sticky='w'+'e')

        show_word_button = tk.Button(buttons_frame, text='Показать слово', font=('Arial 12 bold'), command=self.show_word)
        show_word_button.grid(row=1, column=0, padx=10, pady=5, sticky='w'+'e')

        tip_button = tk.Button(buttons_frame, text='Подсказка', font=('Arial 12 bold'), command=self.get_tip)
        tip_button.grid(row=2, column=0, padx=10, sticky='w'+'e')

        return buttons_frame

    def create_menu_frame(self) -> tk.Frame:
        menu_frame = tk.Frame(self, bg=self.bg)

        menu_button = tk.Button(menu_frame, text='главное меню', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.display_main_menu)
        menu_button.pack(side=tk.LEFT, padx=5)

        quit_button = tk.Button(menu_frame, text='выход', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.exit)
        quit_button.pack(side=tk.RIGHT, padx=10)

        return menu_frame

    def insert_right_text(self, text):
        self.__right_text.config(state='normal')
        self.__right_text.insert(0.0, text + '\n')
        self.__right_text.config(state='disabled')
    
    def tip_text_set(self, text):
        self.__tip_text.config(state='normal')
        self.__tip_text.delete(0.0, tk.END)
        self.__tip_text.insert(0.0, text)
        self.__tip_text.config(state='disabled')
    
    def clear_right_text(self):
        self.__right_text.config(state='normal')
        self.__right_text.delete(0.0, tk.END)
        self.__right_text.config(state='disabled')

    def on_timer_start(self):
        self.exercise.result = 0
    
    def on_timer_stop(self):
        time = self.timer.last_added_time
        result = self.exercise.result

        self.save_statistics(seconds=time.seconds, result=result)
        messagebox.showinfo("Статистика", f'Время: {time}\nНайдено: {result}')

        self.exercise.result = 0    

    def entry_set(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)
    
    def save_statistics(self, seconds, result):
        if not seconds or not result or not self.get_generated_words():
            return        
        
        statistic_path = os.path.join(sys.path[0], 'statistics', 'statistics')
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with shelve.open(statistic_path, writeback=True) as stats_file:
                stats_file.setdefault(self.exercise_name, {})

                stats_file[self.exercise_name] = {
                    'date' : str(today),
                    'stats' : {'text' : self.get_generated_words(), 'seconds' : seconds,'result' : result}
                    }
    
    def generate(self):
        raise NotImplementedError

    def generate_random_words(self):
        raise NotImplementedError

    def get_generated_words(self) -> str:
        raise NotImplementedError
    
    def check_word(self, word):
        raise NotImplementedError
    
    def recalculate_totals(self):
        raise NotImplementedError        

    def show_word(self):
        raise NotImplementedError

    def get_tip(self):
        raise NotImplementedError          

class Exercise(object):
    def __init__(self):
       self.session = self.create_session()

       self.chains = []
       self.word_ass = []
       self.result = 0    

    def generate_chains(self, first_word, last_word):
        if not first_word or not last_word:
            return
        
        url = r'https://sociation.org/ajax/find_path/'
        self.chains = []

        for depth in (3, 4):
            page_data = self.session.post(url, {'word_from' : first_word, 'word_to' : last_word, 'depth' : depth})
            chains_dict = json.loads(page_data.text)

            for path in chains_dict['paths']:
                self.chains.append(path['words'])
                
    def generate_word_ass(self, word):
        url = r'https://sociation.org/ajax/word_associations/'
        self.word_ass = []

        page_data =  self.session.post(url, {'word' : word})
        ass_dict = json.loads(page_data.text)

        for ass in ass_dict['associations']:
                self.word_ass.append(ass['name'])        
    
    def get_word_ass(self, word) -> list:
        url = r'https://sociation.org/ajax/word_associations/'
        word_ass = []

        page_data =  self.session.post(url, {'word' : word})
        ass_dict = json.loads(page_data.text)

        for ass in ass_dict['associations']:
                word_ass.append(ass['name'])
        
        return word_ass

    def generate_random_word(self) -> str:
        url = r'https://sociation.org/ajax/random_word/'
        page_data =  self.session.post(url)
        word_dict = json.loads(page_data.text)

        return word_dict['word']['name']
    
    def is_chain_word_right(self, word, words_chain) -> bool:
        if not word or not words_chain:
            return False
        
        if not word in words_chain:
            return False

        word_indx = words_chain.index(word) 
        for i, chain in enumerate(self.chains):
            if words_chain[:word_indx + 1] == chain[:word_indx + 1]:
                return True        

    def is_chain_right(self, words_chain) -> bool:
        if words_chain in self.chains:
            self.result += 1
            self.chains.remove(words_chain)
            return True
            
        return False
    
    def is_ass_word_right(self, ass_word) -> bool:
        if ass_word in self.word_ass:
            self.result += 1
            self.word_ass.remove(ass_word)
            return True
        
        return False

    def get_first_chain_word(self) -> str:
        return self.chains[0][1]

    def get_second_chain_word(self, words_chain) -> str:
        four_depth_chains = [chain for chain in self.chains if len(chain) == 4]
        tip_chains = [chain for chain in four_depth_chains if chain[1] == words_chain[1]]

        return tip_chains[0][2]

    def get_three_depths_total(self) -> int:
        return len([chain for chain in self.chains if len(chain) == 3])

    def get_four_depths_total(self) -> int:
        return len([chain for chain in self.chains if len(chain) == 4])

    def create_session(self) -> requests.Session:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})

        return session   

