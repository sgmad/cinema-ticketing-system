import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import ctypes
from datetime import datetime
from db.queries import get_showtimes_for_movie
from gui.seat_map import SeatMap

# THEME CONSTANTS
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
TEXT_SUB = "#B3B3B3"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"
RATING_COLOR = "#FFD700"

class CustomerShowtimeSelect:
    def __init__(self, movie_data):
        self.movie = movie_data
        
        self.window = tk.Toplevel()
        self.window.title(f"Showtimes - {self.movie['title']}")
        self.window.configure(bg=BG_COLOR)

        # ---------------------------------------------------------
        # BALANCED SIZE (1000x650)
        # ---------------------------------------------------------
        window_width = 1000
        window_height = 650
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Force Dark Title Bar
        try:
            self.window.update()
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.window.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

        # Scrollbar Styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Dark.Vertical.TScrollbar",
            gripcount=0, background="#333", darkcolor=BG_COLOR, lightcolor=BG_COLOR,
            troughcolor=BG_COLOR, bordercolor=BG_COLOR, arrowcolor="white"
        )
        style.map("Dark.Vertical.TScrollbar", background=[("active", ACCENT)])

        # =========================================================
        # MAIN LAYOUT
        # =========================================================
        main_container = tk.Frame(self.window, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # LEFT COLUMN (Poster + Info)
        left_column = tk.Frame(main_container, bg=BG_COLOR, width=280)
        left_column.pack(side="left", fill="y", padx=(0, 30))
        left_column.pack_propagate(False)

        self.setup_left_sidebar(left_column)

        # RIGHT COLUMN (Content)
        right_column = tk.Frame(main_container, bg=BG_COLOR)
        right_column.pack(side="left", fill="both", expand=True)
        
        self.setup_content_area(right_column)

    def setup_left_sidebar(self, parent):
        # 1. Poster Card
        poster_card = tk.Frame(parent, bg=SURFACE_COLOR, padx=10, pady=10)
        poster_card.pack(fill="x")
        
        poster_w, poster_h = 240, 360 # Slightly smaller poster to fit height
        canvas = tk.Canvas(poster_card, width=poster_w, height=poster_h, bg="#000", highlightthickness=0)
        canvas.pack()

        image_path = self.movie.get('poster_path', 'assets/sample_posters/default.png')
        if not os.path.exists(image_path): image_path = os.path.abspath(image_path)
        
        try:
            img = Image.open(image_path)
            img = img.resize((poster_w, poster_h), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img) 
            canvas.create_image(0, 0, anchor="nw", image=self.photo)
        except:
            canvas.create_text(poster_w//2, poster_h//2, text=self.movie['title'], fill="white")

        # 2. Info Grid
        info_frame = tk.Frame(parent, bg=BG_COLOR, pady=20)
        info_frame.pack(fill="x")

        def add_info_row(label, value):
            row = tk.Frame(info_frame, bg=BG_COLOR, pady=4)
            row.pack(fill="x")
            tk.Label(row, text=label.upper(), font=("Helvetica", 8, "bold"), fg="#666", bg=BG_COLOR, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10), fg=TEXT_MAIN, bg=BG_COLOR, anchor="w", wraplength=200, justify="left").pack(side="left", fill="x")
            tk.Frame(info_frame, bg="#222", height=1).pack(fill="x", pady=4) 

        add_info_row("Director", self.movie.get('director', 'TBA'))
        add_info_row("Cast", self.movie.get('cast', 'Unavailable'))
        
        # 3. Tagline
        tagline = self.movie.get('review', 'No tagline.')
        if not tagline or tagline == "No reviews available.": tagline = "Experience it in theaters."
            
        tk.Label(info_frame, text="TAGLINE", font=("Helvetica", 8, "bold"), fg=ACCENT, bg=BG_COLOR).pack(anchor="w", pady=(15, 5))
        tk.Label(
            info_frame, text=tagline, 
            font=("Helvetica", 10, "italic"), fg="#999", bg=BG_COLOR, 
            wraplength=260, justify="left", anchor="w"
        ).pack(fill="x")

    def setup_content_area(self, parent):
        # 1. Title
        tk.Label(
            parent, text=self.movie['title'], 
            font=("Helvetica", 28, "bold"), fg=TEXT_MAIN, bg=BG_COLOR, anchor="w"
        ).pack(fill="x")

        # 2. Badges
        meta_frame = tk.Frame(parent, bg=BG_COLOR)
        meta_frame.pack(fill="x", pady=(10, 15))
        
        def add_badge(text, bg_col, txt_col="#000"):
            f = tk.Frame(meta_frame, bg=bg_col, padx=8, pady=3)
            f.pack(side="left", padx=(0, 10))
            tk.Label(f, text=text, font=("Helvetica", 9, "bold"), fg=txt_col, bg=bg_col).pack()
            
        add_badge(self.movie.get('rating', 'NR'), ACCENT)
        add_badge(self.movie.get('imdb_rating', '★ -/10'), RATING_COLOR)
        add_badge(f"{self.movie.get('duration_minutes', 0)} min", "#333", "#FFF")
        add_badge(self.movie.get('genre', 'General'), "#333", "#FFF")

        # 3. Synopsis
        desc = self.movie.get('description', 'No synopsis available.')
        tk.Label(
            parent, text=desc, 
            font=("Helvetica", 11), fg=TEXT_SUB, bg=BG_COLOR, 
            wraplength=600, justify="left", anchor="w"
        ).pack(fill="x", pady=(0, 20))

        # 4. Schedule
        tk.Label(
            parent, text="Select Showtime", 
            font=("Helvetica", 14, "bold"), fg=ACCENT, bg=BG_COLOR, anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Scroll Container
        container = tk.Frame(parent, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview, style="Dark.Vertical.TScrollbar")
        scroll_frame = tk.Frame(canvas, bg=BG_COLOR)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.load_showtimes_into_frame(scroll_frame)

    def load_showtimes_into_frame(self, frame):
        showtimes = get_showtimes_for_movie(self.movie['id'])

        if not showtimes:
            tk.Label(frame, text="No upcoming showtimes found.", bg=BG_COLOR, fg=TEXT_SUB, font=("Helvetica", 12)).pack(pady=20)
            return

        grouped_shows = {}
        for st in showtimes:
            date_key = st['start_time'].strftime("%A, %d %B")
            if date_key not in grouped_shows: grouped_shows[date_key] = []
            grouped_shows[date_key].append(st)

        for date_str, shows_list in grouped_shows.items():
            header_f = tk.Frame(frame, bg=SURFACE_COLOR, pady=5, padx=10)
            header_f.pack(fill="x", pady=(10, 8))
            tk.Label(header_f, text=date_str, font=("Helvetica", 11, "bold"), fg=TEXT_MAIN, bg=SURFACE_COLOR).pack(side="left")

            # Grid Container for 3 Columns
            btn_container = tk.Frame(frame, bg=BG_COLOR)
            btn_container.pack(fill="x", pady=(0, 15))

            for i, show in enumerate(shows_list):
                # 3 BUTTONS PER ROW = Comfortable spacing
                r = i // 3
                c = i % 3
                self.create_time_button(btn_container, show, r, c)

    def create_time_button(self, parent, show, r, c):
        time_str = show['start_time'].strftime("%I:%M %p")
        hall_name = show['hall_name']
        price = show['price_standard']
        
        f = tk.Frame(parent, bg=BG_COLOR)
        # Wider horizontal padding between grid items
        f.grid(row=r, column=c, padx=10, pady=5) 

        # RESTORED WIDTH 18
        btn = tk.Button(
            f,
            text=f"{time_str}\n{hall_name}\n₱{price}",
            font=("Helvetica", 10), # Slightly larger font
            bg=SURFACE_COLOR,
            fg=ACCENT,
            activebackground=ACCENT,
            activeforeground="#000",
            relief="flat",
            bd=0,
            width=18, # WIDE BUTTONS RESTORED
            height=3,
            cursor="hand2",
            command=lambda s=show: self.select_showtime(s)
        )
        btn.pack()
        
        def on_enter(e): btn.config(bg=ACCENT, fg="#000")
        def on_leave(e): btn.config(bg=SURFACE_COLOR, fg=ACCENT)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def select_showtime(self, showtime_dict):
        showtime_dict['movie_title'] = self.movie['title'] 
        seat_screen = SeatMap(showtime_dict)
        seat_screen.run()

    def run(self):
        self.window.mainloop()
