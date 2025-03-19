import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk
#from ttkbootstrap.style import Style
from ttkbootstrap.constants import *
from ..services.config import ConfigService
from ..services.scheduler import SchedulerService
from ..services.instrument import InstrumentService
from ..services.job import JobService

theme_name = "flatly"

class ColorCircle:
    def __init__(self, parent, size):
        self.canvas = ttk.Canvas(
            parent,
            width=size,
            height=size,
            background="white",
            highlightthickness=0
        )
        # Create the circle and store its id
        self.circle_id = self.canvas.create_oval(
            0, 0, size, size,
            fill="white",  # default color
            outline=""
        )
    
    def set_color(self, color):
        # Update circle color
        self.canvas.itemconfig(self.circle_id, fill=color)
    
    def pack(self, *args, **kwargs):
        self.canvas.pack(*args, **kwargs)

class StatusUI(ttk.Frame):
    
    def __init__(self, master, url: str):
        super().__init__(master)
        self.scheduler_service = SchedulerService(url)
        self.refresh_listeners = []
        
        self.pack(fill=BOTH, expand=YES)
        self.create_status_widgets()
    
    def add_refresh_listener(self, listener):
        self.refresh_listeners.append(listener)
        
    def create_status_widgets(self):
        self.status_text = ttk.StringVar(value=self.scheduler_service.get_status()["status"])
        self.create_status_view()
        self.create_status_controls()
        self.update_status_display()
    
    def create_status_view(self):
        """Create the status display"""
        container = ttk.Frame(self, padding=10)
        container.pack(fill=X)
        self.circle = ColorCircle(container, 50)
        self.circle.pack(side=LEFT, padx=20)
        lbl = ttk.Label(
            master=container,
            font="-size 16",
            #anchor=CENTER,
            textvariable=self.status_text,
        )
        lbl.pack(side=TOP, fill=X, padx=20, pady=20)
    
    def create_status_controls(self):
        """Create the control frame with buttons"""
        container = ttk.Frame(self, padding=10)
        container.pack(fill=X)
        self.buttons = []
        self.buttons.append(
            ttk.Button(
                master=container,
                text= "?",
                width=10,
                bootstyle=INFO,
                command=self.on_toggle,
            )
        )
        self.buttons.append(
            ttk.Button(
                master=container,
                text="Refresh",
                width=10,
                bootstyle=SUCCESS,
                command=self.on_refresh,
            )
        )
        self.buttons.append(
            ttk.Button(
                master=container,
                text="Stop",
                width=10,
                bootstyle=DANGER,
                command=self.on_stop,
            )
        )
        for button in self.buttons:
            button.pack(side=LEFT, fill=X, expand=YES, pady=0, padx=5)
    
    def on_toggle(self):
        """Toggle the start and pause button."""
        if self.status_text.get() == "running":
            self.on_pause()
        elif self.status_text.get() == "paused":
            self.on_resume()
        else:
            self.on_start()
    
    def update_status_display(self):
        button = self.buttons[0]
        if self.is_paused():
            button.configure(bootstyle=INFO, text="Resume")
            self.circle.set_color("orange")
        elif self.is_running():
            button.configure(bootstyle=INFO, text="Pause")
            self.circle.set_color("green")
        elif self.is_stopped():
            button.configure(bootstyle=INFO, text="Start")
            self.circle.set_color("red")
        else:
            button.configure(bootstyle=INFO, text="Start")
            self.circle.set_color("black")

    def is_running(self):
      return self.status_text.get() == "running"
    
    def is_stopped(self):
      return self.status_text.get() == "stopped"
    
    def is_paused(self):
      return self.status_text.get() == "paused"
  
    def is_error(self):
      return self.status_text.get() == "error"

    def on_start(self):
        resp = self.scheduler_service.start()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_stop(self):
        resp = self.scheduler_service.stop()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_refresh(self):
        resp = self.scheduler_service.get_status()
        self.status_text.set(resp["status"])
        self.update_status_display()
        for listener in self.refresh_listeners:
            listener()

    def on_pause(self):
        resp = self.scheduler_service.pause()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_resume(self):
        resp = self.scheduler_service.resume()
        self.status_text.set(resp["status"])
        self.update_status_display()

class InstrumentsListBox:
    
    def __init__(self, parent):
        self.listbox = tk.Listbox(parent)
        self.listbox.pack(fill=BOTH, expand=YES)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.instruments = []
        self.listeners = []
        
    def apply(self, instruments):
        self.clear()
        self.instruments = instruments
        for instrument in instruments:
            self.insert(instrument)
    
    def insert(self, instrument):
        self.listbox.insert(END, instrument["name"])
    
    def clear(self):
        self.listbox.delete(0, END)
        self.instruments = []
    
    def select(self, index):
        self.listbox.select_set(index)
        self.listbox.event_generate("<<ListboxSelect>>")
    
    def get_selected(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            return self.instruments[index]
        return None

    def add_listener(self, listener):
        self.listeners.append(listener)
        
    def on_select(self, event):
        for listener in self.listeners:
            listener(self.get_selected())
    
    def pack(self, *args, **kwargs):
        self.listbox.pack(*args, **kwargs)
        
class InstrumentTabs:
    def __init__(self, parent, url: str):
        self.url = url
        self.instrument_service = None
        self.scheduler_service = SchedulerService(url)
        
        self.notebook = ttk.Notebook(parent)
        
        self.config_tab = ttk.Frame(self.notebook)
        self.config_label = ttk.Label(self.config_tab, text="", font=("Arial", 10))
        self.config_label.pack(side="left", anchor="nw", padx=10, pady=10)
        self.add_tab("Configuration", self.config_tab)
        
        self.jobs_tab = ttk.Frame(self.notebook)
        self.jobs_label = ttk.Label(self.jobs_tab, text="", font=("Arial", 10))
        self.jobs_label.pack(side="left", anchor="nw", padx=10, pady=10)
        self.add_tab("Jobs", self.jobs_tab)
        
        self.logs_tab = ttk.Frame(self.notebook)
        self.logs_text_area = ScrolledText(self.logs_tab, font=("Arial", 10))
        self.logs_text_area.pack(side="left", anchor="nw", padx=10, pady=10)
        self.add_tab("Logs", self.logs_tab)
    
    def add_tab(self, title, content):
        self.notebook.add(content, text=title)
        
    def show_instrument(self, instrument):
        self.logs_text_area.delete(1.0, END)
        if instrument is None:
            self.instrument_service = None
            self.config_label.config(text="No instrument selected")
            self.jobs_label.config(text="No instrument selected")
        else:
            self.instrument_service = InstrumentService(self.url, instrument["name"])
            self.config_label.config(text=json.dumps(instrument, indent=2))
            self.jobs_label.config(text=json.dumps(self.scheduler_service.get_jobs(instrument["name"]), indent=2))
            self.logs_text_area.insert(END, self.instrument_service.get_logs(100))
    
    def pack(self, *args, **kwargs):
        self.notebook.pack(*args, **kwargs)
        
class InstrumentsUI(ttk.Frame):
    
        def __init__(self, master, url: str):
            super().__init__(master)
            self.url = url
            self.config_service = ConfigService(url)
            self.scheduler_service = SchedulerService(url)
            
            self.pack(fill=BOTH, expand=YES)
            self.create_instruments_widgets()
        
        def create_instruments_widgets(self):
            
            left_frame = ttk.Frame(self, width=150)  # Fixed width
            left_frame.pack(side="left", fill="y")
            left_frame.pack_propagate(False)  # Prevent shrinking
            self.create_instrument_list(left_frame)
            
            right_frame = ttk.Frame(self)
            right_frame.pack(side="right", expand=True, fill="both")
            self.create_instrument_tabs(right_frame)
            
        def create_instrument_list(self, parent):
            self.list = InstrumentsListBox(parent)
            self.list.pack(fill=BOTH, expand=YES, padx=10, pady=10)
            #self.list.add_listener(print)
            self.list.add_listener(self.on_instrument_selected)
            
        def init(self):
            # Add instruments to the list
            try:
                self.instruments = []
                self.instruments = self.config_service.get_instruments()
                if len(self.instruments) > 0:
                    self.list.apply(self.instruments)
                    self.list.select(0)
                else:
                    self.list.clear()
            except Exception as e:
                self.list.clear()
            
        def create_instrument_tabs(self, parent):
            """Create the tabs for the different views"""
            self.tabs = InstrumentTabs(parent, self.url)
            self.tabs.pack(fill=BOTH, expand=YES, padx=10, pady=10)
            
        def on_instrument_selected(self, instrument):
            self.tabs.show_instrument(instrument)

class FlakeUI(ttk.Frame):
  
    def __init__(self, master, url: str):
        super().__init__(master)
        self.url = url
                
        self.pack(fill=BOTH, expand=YES)

        status = StatusUI(self, self.url)
        status.pack(fill=BOTH, expand=YES)
        
        instruments = InstrumentsUI(self, self.url)
        instruments.pack(fill=BOTH, expand=YES)
        
        instruments.init()
        status.add_refresh_listener(instruments.init)
        
