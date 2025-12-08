import tkinter as tk
from PIL import Image, ImageTk
import os

# OOP IMPORTS
from gui.base_window import BaseWindow
from gui.components import ScrollableFrame
from db.db_manager import DatabaseManager
from gui.seat_map import SeatMap

# THEME
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
TEXT_SUB = "#B3B3B3"
ACCENT = "#BB86FC"
RATING_COLOR = "#FFD700"

class CustomerShowtimeSelect(BaseWindow):
    def __init__(self, movie_object):
        # 1. Accept MOVIE OBJECT, not dict
        self.movie = movie_object
        
        # 2. BaseWindow Setup
        super().__init__(f"Showtimes - {self.movie.title}", 1000, 650, BG_COLOR)
        
        self.db = DatabaseManager()
        
        # Layout
        self.setup_layout()

    def setup_layout(self):
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=30, pady=30)

        # LEFT SIDE
        left_column = tk.Frame(main_container, bg=BG_COLOR, width=280)
        left_column.pack(side="left", fill="y", padx=(0, 30))
        left_column.pack_propagate(False)
        self.setup_sidebar(left_column)

        # RIGHT SIDE
        right_column = tk.Frame(main_container, bg=BG_COLOR)
        right_column.pack(side="left", fill="both", expand=True)
        self.setup_content(right_column)

    def setup_sidebar(self, parent):
        # Poster
        poster_card = tk.Frame(parent, bg=SURFACE_COLOR, padx=10, pady=10)
        poster_card.pack(fill="x")
        
        canvas = tk.Canvas(poster_card, width=240, height=360, bg="#000", highlightthickness=0)
        canvas.pack()

        # Using the Model's method!
        image_path = self.movie.get_poster_path()
        
        try:
            img = Image.open(image_path)
            img = img.resize((240, 360), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img) 
            canvas.create_image(0, 0, anchor="nw", image=self.photo)
        except:
            pass

        # Details
        info_frame = tk.Frame(parent, bg=BG_COLOR, pady=20)
        info_frame.pack(fill="x")

        def add_row(label, value):
            row = tk.Frame(info_frame, bg=BG_COLOR, pady=4)
            row.pack(fill="x")
            tk.Label(row, text=label.upper(), font=("Helvetica", 8, "bold"), fg="#666", bg=BG_COLOR, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 10), fg=TEXT_MAIN, bg=BG_COLOR, anchor="w", wraplength=200, justify="left").pack(side="left", fill="x")
            tk.Frame(info_frame, bg="#222", height=1).pack(fill="x", pady=4) 

        add_row("Director", self.movie.director)
        add_row("Cast", self.movie.cast)
        
        # Tagline
        tagline = self.movie.tagline if self.movie.tagline else "Experience it in theaters."
        tk.Label(info_frame, text="TAGLINE", font=("Helvetica", 8, "bold"), fg=ACCENT, bg=BG_COLOR).pack(anchor="w", pady=(15, 5))
        tk.Label(info_frame, text=tagline, font=("Helvetica", 10, "italic"), fg="#999", bg=BG_COLOR, wraplength=260, justify="left", anchor="w").pack(fill="x")

    def setup_content(self, parent):
        # Title
        tk.Label(parent, text=self.movie.title, font=("Helvetica", 28, "bold"), fg=TEXT_MAIN, bg=BG_COLOR, anchor="w").pack(fill="x")

        # Badges
        meta_frame = tk.Frame(parent, bg=BG_COLOR)
        meta_frame.pack(fill="x", pady=(10, 15))
        
        def add_badge(text, bg_col, txt_col="#000"):
            f = tk.Frame(meta_frame, bg=bg_col, padx=8, pady=3)
            f.pack(side="left", padx=(0, 10))
            tk.Label(f, text=text, font=("Helvetica", 9, "bold"), fg=txt_col, bg=bg_col).pack()
            
        add_badge(self.movie.rating, ACCENT)
        add_badge(self.movie.imdb_rating, RATING_COLOR)
        add_badge(self.movie.get_display_duration(), "#333", "#FFF")
        add_badge(self.movie.genre, "#333", "#FFF")

        # Synopsis
        desc = self.movie.description
        if len(desc) > 600: desc = desc[:600] + "..."
        tk.Label(parent, text=desc, font=("Helvetica", 11), fg=TEXT_SUB, bg=BG_COLOR, wraplength=600, justify="left", anchor="w").pack(fill="x", pady=(0, 20))

        # Schedule Area
        tk.Label(parent, text="Select Showtime", font=("Helvetica", 14, "bold"), fg=ACCENT, bg=BG_COLOR, anchor="w").pack(fill="x", pady=(0, 10))

        # Reusing our Scrollable Component!
        self.scroll_frame = ScrollableFrame(parent)
        self.scroll_frame.pack(fill="both", expand=True)

        self.load_showtimes()

    def load_showtimes(self):
        # Fetch Objects from DB Manager
        showtimes = self.db.fetch_showtimes_by_movie(self.movie.id)

        if not showtimes:
            tk.Label(self.scroll_frame.scroll_window, text="No upcoming showtimes.", bg=BG_COLOR, fg=TEXT_SUB).pack(pady=20)
            return

        # Group by Date string
        grouped = {}
        for st in showtimes:
            d = st.get_formatted_date()
            if d not in grouped: grouped[d] = []
            grouped[d].append(st)

        for date_str, shows in grouped.items():
            # Date Header
            header_f = tk.Frame(self.scroll_frame.scroll_window, bg=SURFACE_COLOR, pady=5, padx=10)
            header_f.pack(fill="x", pady=(10, 8))
            tk.Label(header_f, text=date_str, font=("Helvetica", 11, "bold"), fg=TEXT_MAIN, bg=SURFACE_COLOR).pack(side="left")

            # Grid Container
            btn_container = tk.Frame(self.scroll_frame.scroll_window, bg=BG_COLOR)
            btn_container.pack(fill="x", pady=(0, 15))

            for i, show_obj in enumerate(shows):
                r = i // 3
                c = i % 3
                self.create_time_button(btn_container, show_obj, r, c)

    def create_time_button(self, parent, show_obj, r, c):
        f = tk.Frame(parent, bg=BG_COLOR)
        f.grid(row=r, column=c, padx=10, pady=5) 

        # Button Text from Object Methods
        btn_text = f"{show_obj.get_formatted_time()}\n{show_obj.hall_name}\n{show_obj.get_formatted_price()}"

        btn = tk.Button(
            f, text=btn_text, font=("Helvetica", 10),
            bg=SURFACE_COLOR, fg=ACCENT, activebackground=ACCENT, activeforeground="#000",
            relief="flat", bd=0, width=18, height=3, cursor="hand2",
            # Pass the OBJECT to the handler
            command=lambda: self.select_showtime(show_obj)
        )
        btn.pack()
        
        def on_enter(e): btn.config(bg=ACCENT, fg="#000")
        def on_leave(e): btn.config(bg=SURFACE_COLOR, fg=ACCENT)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def select_showtime(self, showtime_obj):
        seat_screen = SeatMap(showtime_obj, movie_title=self.movie.title)
        seat_screen.run()
