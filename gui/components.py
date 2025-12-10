import tkinter as tk
from tkinter import ttk

# THEME CONSTANTS
BG_COLOR = "#121212"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # --- Scrollbar Styling ---
        style = ttk.Style()
        style.theme_use('clam') 
        
        style.configure("Dark.Vertical.TScrollbar",
            gripcount=0, 
            background="#333333", 
            darkcolor=BG_COLOR, 
            lightcolor=BG_COLOR,
            troughcolor=BG_COLOR, 
            bordercolor=BG_COLOR, 
            arrowcolor="white"
        )
        
        style.map("Dark.Vertical.TScrollbar", 
            background=[("active", ACCENT), ("pressed", ACCENT_DARK)]
        )

        # --- Canvas Setup ---
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=BG_COLOR)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Dark.Vertical.TScrollbar")
        self.scroll_window = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scroll_window.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_window, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Global binding for mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            # Squelch error if widget is destroyed (e.g. window closed)
            pass
