import tkinter as tk
from datetime import datetime
from datetime import timedelta
import winsound
import dateutil
from dateutil.parser import parse


class Timer_GUI(tk.Frame):
    def __init__(self, master, start_function=None, end_fuction=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.timer_var = tk.StringVar()
        self.start_function = start_function
        self.end_function = end_fuction
        self.is_timer_work = False
        self.worked_time = timedelta(seconds=0)
        self.last_added_time = timedelta(seconds=0)
        self.start_time = datetime(year=2020, month=10, day=1, hour=0, minute=0, second=0)

        self.create_widgets()
        self.set_time(self.start_time)

    
    def create_widgets(self):
        self.timer_entry = tk.Entry(self, state='readonly', font='Arial 22 bold', textvariable=self.timer_var, width=10, justify=tk.CENTER)
        self.timer_entry.bind('<Button-3>', lambda e: self.start_timer())
        self.timer_entry.bind('<FocusIn>', lambda e: self.timer_entry.config(state='normal'))
        self.timer_entry.bind('<FocusOut>', lambda e: self.timer_entry.config(state='readonly'))
        self.timer_entry.bind('<Return>', lambda e: self.focus())
        self.timer_entry.grid()
    
    def set_time(self, time : datetime):
        self.timer_var.set(time.time())
    
    def get_time(self) -> datetime:
        return dateutil.parser.parse(self.timer_var.get())
    
    def add_start_time(self):
        self.last_added_time = self.worked_time
        self.set_time(time=self.get_time() + timedelta(seconds=self.start_time.second))

    def start_timer(self):
        if self.start_function:
            self.start_function()
            
        if self.is_timer_work:
            return

        self.is_timer_work = True
        self.worked_time = timedelta(seconds=0)
        self.start_time = self.get_time()
        self.count_time()

    def count_time(self):
        time = self.get_time()
        if time.hour == 0 and time.minute == 0 and time.second == 0:
            self.timer_entry.update()
            self.end_timer()
        else:
            self.worked_time += timedelta(seconds=1)
            self.after(1000, lambda: self.set_time(self.get_time() - timedelta(seconds=1)))
            self.after(1000, lambda: self.count_time())

    def end_timer(self):
        self.is_timer_work = False
        winsound.Beep(2500, 750)
        self.set_time(time=self.start_time)

        if self.end_function:
            self.end_function()

if __name__ == "__main__":
    
    root = tk.Tk()

    timer = Timer_GUI(root)
    timer.grid()

    timer.set_time(datetime(year=2020, month=10, day=1, hour=0, minute=0, second=0))

    root.mainloop()