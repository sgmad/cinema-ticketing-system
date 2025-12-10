import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# OOP IMPORTS
from gui.base_window import BaseWindow
from gui.components import ScrollableFrame
from db.db_manager import DatabaseManager
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

# THEME CONSTANTS
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
HEADER_BG = "#000000"
TEXT_MAIN = "#FFFFFF"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"

class CustomerHome(BaseWindow): # INHERITANCE
    def __init__(self):
        # Call BaseWindow constructor (Title, Width, Height)
        # Note: We use 1400x900 as a default, but BaseWindow handles centering/maximizing logic
        super().__init__("ScreenPass Cinemas", 1400, 900, BG_COLOR)
        
        # COMPOSITION
        self.db = DatabaseManager()
        
        # State
        self.poster_width = 210 
        self.poster_height = 315
        self.poster_padding = 15
        self.images = [] 

        # Setup UI
        try:
            self.state('zoomed') 
        except: pass
        
        self.setup_header()
        self.setup_content()
        self.load_week_view()

    def setup_header(self):
        header_frame = tk.Frame(self, bg=HEADER_BG, pady=20, padx=40)
        header_frame.pack(fill="x")
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x")

        # Logo
        logo_frame = tk.Frame(header_frame, bg=HEADER_BG)
        logo_frame.pack(side="left")
        tk.Label(logo_frame, text="Screen", font=("Helvetica", 26, "bold"), fg=TEXT_MAIN, bg=HEADER_BG).pack(side="left")
        tk.Label(logo_frame, text="Pass", font=("Helvetica", 26, "bold"), fg=ACCENT, bg=HEADER_BG).pack(side="left")

        # Buttons
        btn_frame = tk.Frame(header_frame, bg=HEADER_BG)
        btn_frame.pack(side="right")
        self.create_header_btn(btn_frame, "🔄 Refresh", self.load_week_view)
        tk.Frame(btn_frame, width=20, bg=HEADER_BG).pack(side="left") 
        self.create_header_btn(btn_frame, "Admin Portal", self.open_admin_login, is_primary=True)

    def setup_content(self):
        self.scroll_container = ScrollableFrame(self)
        self.scroll_container.pack(fill="both", expand=True)

    def create_header_btn(self, parent, text, command, is_primary=False):
        bg = ACCENT if is_primary else "#333333"
        fg = "#000000" if is_primary else TEXT_MAIN
        
        btn = tk.Button(
            parent, text=text, font=("Helvetica", 11, "bold"),
            bg=bg, fg=fg, activebackground=ACCENT_DARK, activeforeground=TEXT_MAIN,
            padx=20, pady=8, relief="flat", cursor="hand2", command=command
        )
        btn.pack(side="left")
        
        # Hover Effects
        def on_enter(e): btn.config(bg=ACCENT_DARK, fg=TEXT_MAIN)
        def on_leave(e): btn.config(bg=bg, fg=fg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def load_week_view(self):
        # Clear existing
        for widget in self.scroll_container.scroll_window.winfo_children():
            widget.destroy()
        self.images = []

        today = datetime.now()
        print("Rendering Schedule...")
        
        for i in range(14): 
            date_obj = today + timedelta(days=i)
            date_str = date_obj.strftime('%Y-%m-%d')
            display_date = date_obj.strftime("%A, %d %B") 
            
            # ABSTRACTION: Asking the DB Manager for Objects
            movies = self.db.fetch_movies_by_date(date_str)
            
            if movies:
                self.create_day_section(display_date, movies)

    def create_day_section(self, date_text, movies):
        parent = self.scroll_container.scroll_window
        
        # Section Header
        header_container = tk.Frame(parent, bg=BG_COLOR, pady=10)
        header_container.pack(fill="x", pady=(30, 10), padx=20) 
        tk.Frame(header_container, bg=ACCENT, width=5, height=30).pack(side="left")
        tk.Label(header_container, text=f"  {date_text}", font=("Helvetica", 18, "bold"), fg=TEXT_MAIN, bg=BG_COLOR).pack(side="left")
        
        grid_frame = tk.Frame(parent, bg=BG_COLOR)
        grid_frame.pack(fill="x", padx=20)

        columns_per_row = 6 
        for index, movie_obj in enumerate(movies):
            r = index // columns_per_row
            c = index % columns_per_row
            self.create_poster(grid_frame, movie_obj, r, c)

    def create_poster(self, parent, movie, r, c):
        # Note: 'movie' here is now an OBJECT, not a dictionary!
        canvas = tk.Canvas(parent, width=self.poster_width, height=self.poster_height, bg=SURFACE_COLOR, highlightthickness=0)
        canvas.grid(row=r, column=c, padx=self.poster_padding, pady=self.poster_padding)

        # ENCAPSULATION: The movie object knows how to find its poster
        image_path = movie.get_poster_path()
             
        try:
            img = Image.open(image_path)
            img = img.resize((self.poster_width, self.poster_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo) 
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except:
            # Fallback text
            canvas.create_text(self.poster_width//2, self.poster_height//2, text=movie.title, width=180, font=("Helvetica", 10, "bold"), fill=TEXT_MAIN)

        # OVERLAY
        overlay_rect = canvas.create_rectangle(0, 0, self.poster_width, self.poster_height, fill="#0a0a0a", outline=ACCENT, width=2, state="hidden")
        pad = 16
        
        # Accessing Object Attributes directly
        overlay_title = canvas.create_text(pad, 30, text=movie.title, fill=TEXT_MAIN, anchor="nw", font=("Helvetica", 13, "bold"), width=self.poster_width - (pad*2), state="hidden")
        
        meta_text = f"{movie.imdb_rating}  |  {movie.rating}\n🕑 {movie.get_display_duration()}"
        overlay_meta = canvas.create_text(pad, 90, text=meta_text, fill=ACCENT, anchor="nw", font=("Helvetica", 10, "bold"), state="hidden")
        
        desc = movie.description if len(movie.description) <= 120 else movie.description[:120] + "..."
        overlay_desc = canvas.create_text(pad, 135, text=desc, fill="#CCCCCC", anchor="nw", font=("Helvetica", 9), width=self.poster_width - (pad*2), state="hidden")

        overlay_items = [overlay_rect, overlay_title, overlay_meta, overlay_desc]

        def on_enter(e): 
            for it in overlay_items: canvas.itemconfigure(it, state="normal")
        def on_leave(e): 
            for it in overlay_items: canvas.itemconfigure(it, state="hidden")
        
        def on_click(e): self.open_showtimes(movie) # Pass the Object directly!

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

if __name__ == "__main__":
    app = CustomerHome()
    app.run()