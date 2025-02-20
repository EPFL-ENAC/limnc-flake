import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.constants import *
from ..services.scheduler import SchedulerService

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

class FlakeUI(ttk.Frame):
  
    def __init__(self, master, url: str):
        super().__init__(master)
        self.url = url
        self.scheduler = SchedulerService(url)
        self.pack(fill=BOTH, expand=YES)
        self.status_text = ttk.StringVar(value=self.scheduler.get_status()["status"])

        self.create_status_widgets()
        self.create_status_controls()
        self.update_status_display()

    def is_running(self):
      return self.status_text.get() == "running"
    
    def is_stopped(self):
      return self.status_text.get() == "stopped"
    
    def is_paused(self):
      return self.status_text.get() == "paused"
    
    def create_status_widgets(self):
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
        if self.is_running():
          self.on_pause()
        elif self.is_paused():
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
        else:
            button.configure(bootstyle=INFO, text="Start")
            self.circle.set_color("red")

    def on_start(self):
        resp = self.scheduler.start()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_stop(self):
        resp = self.scheduler.stop()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_refresh(self):
        resp = self.scheduler.get_status()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_pause(self):
        resp = self.scheduler.pause()
        self.status_text.set(resp["status"])
        self.update_status_display()

    def on_resume(self):
        resp = self.scheduler.resume()
        self.status_text.set(resp["status"])
        self.update_status_display()
