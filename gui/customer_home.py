import tkinter as tk
from tkinter import ttk 
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
import ctypes 
from datetime import datetime, timedelta

# DB Imports
from db.queries import get_movies_by_date
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

# =========================================================
# DESIGN SYSTEM: "Cyberpunk Violet"
# =========================================================
BG_COLOR = "#121212"       
SURFACE_COLOR = "#1E1E1E"  
HEADER_BG = "#000000"      
TEXT_MAIN = "#FFFFFF"      
TEXT_SUB = "#B3B3B3"       
ACCENT = "#BB86FC"         
ACCENT_DARK = "#3700B3"    

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
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
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class CustomerHome:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ScreenPass Cinemas")
        self.window.configure(bg=BG_COLOR)

        # ---------------------------------------------------------
        # THE SCROLLBAR STYLING ENGINE
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # DARK TITLE BAR HACK
        # ---------------------------------------------------------
        try:
            self.window.update()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.window.winfo_id())
            rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
            value = 2
            value = ctypes.c_int(value)
            set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))
        except:
            pass

        try:
            self.window.state('zoomed') 
        except:
            self.window.geometry("1400x900")

        # =========================================================
        # 1. HEADER SECTION
        # =========================================================
        header_frame = tk.Frame(self.window, bg=HEADER_BG, pady=20, padx=40)
        header_frame.pack(fill="x")
        
        tk.Frame(self.window, bg=ACCENT, height=2).pack(fill="x")

        # LOGO AREA
        logo_frame = tk.Frame(header_frame, bg=HEADER_BG)
        logo_frame.pack(side="left")

        tk.Label(logo_frame, text="Screen", font=("Helvetica", 26, "bold"), fg=TEXT_MAIN, bg=HEADER_BG).pack(side="left")
        tk.Label(logo_frame, text="Pass", font=("Helvetica", 26, "bold"), fg=ACCENT, bg=HEADER_BG).pack(side="left")

        # Controls
        btn_frame = tk.Frame(header_frame, bg=HEADER_BG)
        btn_frame.pack(side="right")

        self.create_header_btn(btn_frame, "🔄 Refresh", self.load_week_view)
        tk.Frame(btn_frame, width=20, bg=HEADER_BG).pack(side="left") 
        self.create_header_btn(btn_frame, "Admin Portal", self.open_admin_login, is_primary=True)

        # =========================================================
        # 2. CONTENT AREA
        # =========================================================
        self.scroll_container = ScrollableFrame(self.window)
        self.scroll_container.pack(fill="both", expand=True)

        # UPDATED: Slightly smaller width to ensure 6 fit on screen
        self.poster_width = 210 
        self.poster_height = 315
        self.poster_padding = 15
        self.images = [] 

        self.load_week_view()

    def create_header_btn(self, parent, text, command, is_primary=False):
        bg = ACCENT if is_primary else "#333333"
        fg = "#000000" if is_primary else TEXT_MAIN
        
        btn = tk.Button(
            parent, 
            text=text, font=("Helvetica", 11, "bold"),
            bg=bg, fg=fg, 
            activebackground=ACCENT_DARK, activeforeground=TEXT_MAIN,
            padx=20, pady=8, relief="flat", cursor="hand2",
            command=command
        )
        btn.pack(side="left")

        def on_enter(e): btn.config(bg=ACCENT_DARK, fg=TEXT_MAIN)
        def on_leave(e): btn.config(bg=bg, fg=fg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def load_week_view(self):
        for widget in self.scroll_container.scroll_window.winfo_children():
            widget.destroy()
        self.images = []

        today = datetime.now()
        
        for i in range(7): 
            date_obj = today + timedelta(days=i)
            date_str = date_obj.strftime('%Y-%m-%d')
            display_date = date_obj.strftime("%A, %d %B") 
            
            movies = get_movies_by_date(date_str)
            
            if movies:
                self.create_day_section(display_date, movies)

    def create_day_section(self, date_text, movies):
        parent = self.scroll_container.scroll_window
        
        # 1. Date Header
        header_container = tk.Frame(parent, bg=BG_COLOR, pady=10)
        # UPDATED: Reduced padx here too
        header_container.pack(fill="x", pady=(30, 10), padx=20) 
        
        tk.Frame(header_container, bg=ACCENT, width=5, height=30).pack(side="left")
        
        tk.Label(
            header_container, text=f"  {date_text}",
            font=("Helvetica", 18, "bold"), fg=TEXT_MAIN, bg=BG_COLOR
        ).pack(side="left")
        
        # 2. Grid
        grid_frame = tk.Frame(parent, bg=BG_COLOR)
        # UPDATED: Reduced padx from 40 to 20 to shift everything Left
        grid_frame.pack(fill="x", padx=20)

        columns_per_row = 6 
        
        for index, movie in enumerate(movies):
            r = index // columns_per_row
            c = index % columns_per_row
            self.create_poster(grid_frame, movie, r, c)

    def create_poster(self, parent, movie, r, c):
        canvas = tk.Canvas(parent, width=self.poster_width, height=self.poster_height, bg=SURFACE_COLOR, highlightthickness=0)
        canvas.grid(row=r, column=c, padx=self.poster_padding, pady=self.poster_padding)

        image_path = movie.get('poster_path', 'assets/sample_posters/default.png')
        if not os.path.exists(image_path): image_path = os.path.abspath(image_path)
             
        try:
            img = Image.open(image_path)
            img = img.resize((self.poster_width, self.poster_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo) 
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except:
            canvas.create_text(self.poster_width//2, self.poster_height//2, text=movie['title'], width=180, font=("Helvetica", 10, "bold"), fill=TEXT_MAIN)

        # OVERLAY LOGIC
        overlay_rect = canvas.create_rectangle(0, 0, self.poster_width, self.poster_height, fill="#0a0a0a", outline=ACCENT, width=2, state="hidden")
        pad = 16
        
        overlay_title = canvas.create_text(pad, 30, text=movie['title'], fill=TEXT_MAIN, anchor="nw", font=("Helvetica", 13, "bold"), width=self.poster_width - (pad*2), state="hidden")
        overlay_meta = canvas.create_text(pad, 90, text=f"★ {movie.get('rating', 'N/A')}\n🕑 {movie.get('duration_minutes', 0)} mins", fill=ACCENT, anchor="nw", font=("Helvetica", 10, "bold"), state="hidden")
        
        desc = movie.get('description', '')
        if len(desc) > 120: desc = desc[:120] + "..."
        overlay_desc = canvas.create_text(pad, 135, text=desc, fill="#CCCCCC", anchor="nw", font=("Helvetica", 9), width=self.poster_width - (pad*2), state="hidden")

        overlay_items = [overlay_rect, overlay_title, overlay_meta, overlay_desc]

        def on_enter(e): 
            for it in overlay_items: canvas.itemconfigure(it, state="normal")
        def on_leave(e): 
            for it in overlay_items: canvas.itemconfigure(it, state="hidden")
        def on_click(e): self.open_showtimes(movie)

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

    def open_showtimes(self, movie_dict):
        screen = CustomerShowtimeSelect(movie_dict) 
        screen.run()

    def open_admin_login(self):
        admin = AdminLogin()
        admin.run()
        self.load_week_view()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CustomerHome()
    app.run()
