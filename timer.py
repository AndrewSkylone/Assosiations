import tkinter as tk
from datetime import datetime
from datetime import timedelta
import winsound
import dateutil
from dateutil.parser import parse

NULL_TIME = datetime(year=2020, month=10, day=1, hour=0, minute=0, second=0)

class Timer_GUI(tk.Frame):
    def __init__(self, master, start_function=None, stop_function=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.timer_var = tk.StringVar()
        self.start_function = start_function
        self.stop_function = stop_function
        self.is_timer_work = False
        self.worked_time = timedelta(seconds=0)
        self.last_added_time = timedelta(seconds=0)
        self.start_time = NULL_TIME

        self.create_widgets()
        self.set_time(self.start_time)
    
    def create_widgets(self):
        self.timer_entry = tk.Entry(self, state='readonly', font='Arial 22 bold', textvariable=self.timer_var, width=10, justify=tk.CENTER)
        self.timer_entry.bind('<Button-3>', lambda e: self.start_timer())
        self.timer_entry.bind('<FocusIn>', lambda e: self.timer_entry.config(state='normal'))
        self.timer_entry.bind('<FocusOut>', lambda e: self.timer_entry.config(state='readonly'))
        self.timer_entry.bind('<Return>', lambda e: self.start_timer())
        self.timer_entry.grid(row=0, column=0, columnspan=2)

        start_button = tk.Button(self, text='start', bg='#B0E0E6', font='Arial 12 bold', command=self.start_timer)
        start_button.grid(row=1, column=0, sticky='swen')

        stop_button = tk.Button(self, text='stop', bg='#B0E0E6', font='Arial 12 bold', command=self.stop_timer)
        stop_button.grid(row=1, column=1, sticky='swen')
    
    def set_time(self, time : datetime):
        self.timer_var.set(time.time())
        self.timer_entry.update()
    
    def get_time(self) -> datetime:
        return dateutil.parser.parse(self.timer_var.get())
    
    def add_start_time(self):
        if self.is_timer_work:
            self.last_added_time = self.worked_time
            self.set_time(time=self.get_time() + timedelta(seconds=self.start_time.second))

    def start_timer(self):
        if self.is_timer_work:
            return

        if self.start_function:
            self.start_function()

        self.is_timer_work = True
        self.worked_time = timedelta(seconds=0)
        self.last_added_time = timedelta(seconds=0)
        self.start_time = self.get_time()
        self.count_time()
        self.focus()

    def count_time(self):
        time = self.get_time()

        if time.hour == 0 and time.minute == 0 and time.second == 0:
            self.stop_timer()
        elif self.is_timer_work:
            self.after(1000, lambda: self.take_second(time=time))

    def take_second(self, time):
        if self.is_timer_work:
            self.worked_time += timedelta(seconds=1)
            self.set_time(self.get_time() - timedelta(seconds=1))
            self.count_time()

    def stop_timer(self):
        self.is_timer_work = False
        winsound.Beep(2500, 750)
        self.set_time(time=self.start_time)

        if self.stop_function:
            self.stop_function()

if __name__ == "__main__":
    
    root = tk.Tk()

    timer = Timer_GUI(root)
    timer.grid()

    timer.set_time(datetime(year=2020, month=10, day=1, hour=0, minute=0, second=0))

    root.mainloop()