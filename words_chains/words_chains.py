import requests
import json
import tkinter as tk
from tkinter import messagebox
import copy

import timer
import exercise


name = 'Цепочки слов'

class Exercise_GUI(exercise.Exercise_GUI):
    def __init__(self, master, cnf={}, **kw):
        exercise.Exercise_GUI.__init__(self, master, cnf, **kw)

    def insert_found_chains_text(self, text):
        self.__found_chains_text.config(state='normal')
        self.__found_chains_text.insert(0.0, text + '\n')
        self.__found_chains_text.config(state='disabled')
    
    def tip_text_set(self, text):
        self.__tip_text.config(state='normal')
        self.__tip_text.delete(0.0, tk.END)
        self.__tip_text.insert(0.0, text)
        self.__tip_text.config(state='disabled')

    def generate_chains(self):
        try:
            self.exercise.generate_chains(first_word=self.first_word_entry.get(), last_word=self.last_word_entry.get())
        except:
            messagebox.showerror("Error", "Ошибочка...")
            return

    def on_chains_set(self, chains=[]):
        self.recalculate_totals()

    def on_chains_generated(self):
        self.clear_found_chains_text()
        self.clear_chain_entries()
        self.focus_set()
    
    def on_word_ass_set(self, word_ass):
        short_ass = [ass for ass in word_ass if len(ass) <= 15]
        self.tip_text_set(text='')        
        self.tip_text_set(text='\n'.join(short_ass))
    
    def clear_found_chains_text(self):
        self.__found_chains_text.config(state='normal')
        self.__found_chains_text.delete(0.0, tk.END)
        self.__found_chains_text.config(state='disabled')

    def check_word(self, word):
        words_chain = self.get_words_chain()

        if not self.exercise.is_word_right(word=word, words_chain=words_chain):
            if word == self.second_word_entry.get():
                self.second_word_entry.delete(0, tk.END)
            else:
                self.third_word_entry.delete(0, tk.END)
            return

        self.check_chain()
        self.focus_set()

    def check_chain(self):
        if self.exercise.is_chain_right(words_chain=self.get_words_chain()):
            self.insert_found_chains_text(', '.join(self.get_words_chain()))
            self.recalculate_totals()
            self.clear_chain_entries()
            self.timer.add_start_time()
    
    def recalculate_totals(self):
        self.three_total_depths_label['text'] = self.exercise.get_three_depths_total()
        self.four_total_depths_label['text'] = self.exercise.get_four_depths_total()
    
    def clear_chain_entries(self):
        self.second_word_entry.delete(0, tk.END)
        self.third_word_entry.delete(0, tk.END)
    
    def on_timer_start(self):
        self.exercise.result = 0
    
    def after_timer_finished(self):
        time = self.timer.last_added_time
        found_chains = self.exercise.result
        messagebox.showinfo("Статистика", f'Время: {time}\nНайдено цепочек: {found_chains}')

        self.exercise.result = 0    

    def show_word(self):
        word = self.second_word_entry.get()
        words_chain = self.get_words_chain()
        
        if not self.exercise.is_word_right(word=word, words_chain=words_chain):
            self.clear_chain_entries()
            self.second_word_entry.insert(0, self.exercise.get_first_word(words_chain=words_chain))
        else:
            self.third_word_entry.delete(0, tk.END)
            self.third_word_entry.insert(0, self.exercise.get_second_word(words_chain=words_chain))

        self.check_chain()

    def get_tip(self):
        word = self.second_word_entry.get()
        words_chain = self.get_words_chain()

        if not self.exercise.is_word_right(word=word, words_chain=words_chain):
            self.clear_chain_entries()
            word = self.exercise.get_first_word(words_chain=words_chain)
        else:
            self.third_word_entry.delete(0, tk.END)
            word = self.exercise.get_second_word(words_chain=words_chain)
        
        self.exercise.generate_word_ass(word=word)            

    def get_words_chain(self) -> list:
        return [entry.get() for entry in self.chain_entries if entry.get()]

class Exercise(exercise.Exercise):
    def __init__(self):
       self.session = self.create_session()

       self.__chains = []
       self.__word_ass = []
       self.__listeners = []
       self.result = 0    

    def generate_chains(self, first_word, last_word):
        if not first_word or not last_word:
            return
        
        url = r'https://sociation.org/ajax/find_path/'
        chains = []

        for depth in (3, 4):
            page_data = self.session.post(url, {'word_from' : first_word, 'word_to' : last_word, 'depth' : depth})
            chains_dict = json.loads(page_data.text)

            for path in chains_dict['paths']:
                chains.append(path['words'])
        
        self.set_chains(chains=chains)
        self.on_chains_generated()
        
    def generate_word_ass(self, word):
        url = r'https://sociation.org/ajax/word_associations/'
        word_ass = []

        page_data =  self.session.post(url, {'word' : word})
        ass_dict = json.loads(page_data.text)

        for ass in ass_dict['associations']:
                word_ass.append(ass['name'])
        
        self.set_word_ass(word_ass=word_ass)

    def is_word_right(self, word, words_chain) -> bool:
        if not word or not words_chain:
            return False
        
        if not word in words_chain:
            return False

        word_indx = words_chain.index(word) 
        for i, chain in enumerate(self.get_chains()):
            if words_chain[:word_indx + 1] == chain[:word_indx + 1]:
                return True        

    def is_chain_right(self, words_chain) -> bool:
        if words_chain in self.get_chains():
            self.result += 1
            chains = self.get_chains()
            chains.remove(words_chain)
            self.set_chains(chains=chains)
            return True
            
        return False
    
    def get_first_word(self, words_chain) -> str:
        return self.get_chains()[0][1]

    def get_second_word(self, words_chain) -> str:
        four_depth_chains = [chain for chain in self.get_chains() if len(chain) == 4]
        tip_chains = [chain for chain in four_depth_chains if chain[1] == words_chain[1]]

        return tip_chains[0][2]

    def get_three_depths_total(self) -> int:
        three_depths = [chain for chain in self.get_chains() if len(chain) == 3]
        return len(three_depths)

    def get_four_depths_total(self) -> int:
        four_depths = [chain for chain in self.get_chains() if len(chain) == 4]
        return len(four_depths)
    
    def create_session(self) -> requests.Session:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        session = requests.Session()
        session.headers.update({'User-Agent': user_agent})

        return session

    def set_chains(self, chains):
        self.__chains = copy.deepcopy(chains)
        self.on_chains_set()
    
    def get_chains(self) -> list:
        return copy.deepcopy(self.__chains)
    
    def on_chains_set(self):
        for listener in self.__listeners:
            listener.on_chains_set(chains=self.get_chains())

    def set_word_ass(self, word_ass):
        self.__word_ass = copy.deepcopy(word_ass)
        self.on_word_ass_set()
    
    def get_word_ass(self) -> list:
        return copy.deepcopy(self.__word_ass)
    
    def on_word_ass_set(self):
        for listener in self.__listeners:
            listener.on_word_ass_set(word_ass=self.get_word_ass())

    def on_chains_generated(self):
        for listener in self.__listeners:
            listener.on_chains_generated()
    
    def add_listener(self, listener):
        self.__listeners.append(listener)

if __name__ == "__main__":
    
    root = tk.Tk()

    height = 650
    width = 650
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    
    root.geometry(f"{width}x{height}+{screen_w//2 - width//2}+{screen_h//2 - height//2}")
    root.resizable(False, False)
    root.title('Assosiations')

    main_frame = Exercise_GUI(root)
    main_frame.grid()

    root.mainloop()