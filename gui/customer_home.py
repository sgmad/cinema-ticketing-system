import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

# DB Imports
from db.queries import get_movies_by_date
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

# COLOR PALETTE (Cinema Dark Mode)
BG_COLOR = "#121212"       # Deep Background
HEADER_BG = "#000000"      # Pure Black Header
DATE_BG = "#1f1f1f"        # Dark Gray for Date Strips
TEXT_MAIN = "#FFFFFF"      # White Text
TEXT_SUB = "#AAAAAA"       # Gray Text
ACCENT = "#E50914"         # Netflix/Cinema Red

class ScrollableFrame(tk.Frame):
    """ A helper class to create a scrollable container """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Update colors for dark mode
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=BG_COLOR)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
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
        
        # 1. START MAXIMIZED / LARGER
        # Try to use the Windows 'zoomed' state, fallback to size if on other OS
        try:
            self.window.state('zoomed') 
        except:
            self.window.geometry("1400x900")
            
        self.window.configure(bg=BG_COLOR)

        # =========================================================
        # 2. HEADER SECTION
        # =========================================================
        header_frame = tk.Frame(self.window, bg=HEADER_BG, pady=15, padx=30)
        header_frame.pack(fill="x")
        
        # Red Accent Line
        tk.Frame(self.window, bg=ACCENT, height=2).pack(fill="x")

        # Brand
        tk.Label(
            header_frame, 
            text="ScreenPass", 
            font=("Helvetica", 24, "bold"), 
            fg=ACCENT, bg=HEADER_BG
        ).pack(side="left")
        
        tk.Label(
            header_frame, 
            text="Cinemas", 
            font=("Helvetica", 24), 
            fg=TEXT_MAIN, bg=HEADER_BG
        ).pack(side="left", padx=5)

        # Right Side Controls
        btn_frame = tk.Frame(header_frame, bg=HEADER_BG)
        btn_frame.pack(side="right")

        # Refresh
        tk.Button(
            btn_frame, 
            text="🔄 Refresh", 
            font=("Helvetica", 10),
            bg="#333", fg="white", 
            activebackground="#444", activeforeground="white",
            padx=10, pady=5, relief="flat",
            command=self.load_week_view
        ).pack(side="left", padx=10)

        # Admin
        tk.Button(
            btn_frame, 
            text="Admin Access", 
            font=("Helvetica", 10, "bold"),
            bg="#333", fg="white", 
            activebackground="#444", activeforeground="white",
            padx=15, pady=5, relief="flat",
            command=self.open_admin_login
        ).pack(side="left")

        # =========================================================
        # 3. SCROLLABLE CONTENT AREA
        # =========================================================
        self.scroll_container = ScrollableFrame(self.window)
        self.scroll_container.pack(fill="both", expand=True)

        self.poster_width = 200
        self.poster_height = 300
        self.poster_padding = 10
        self.images = [] 

        # Load Data
        self.load_week_view()

    def load_week_view(self):
        """ Clears the screen and reloads the schedule """
        # Clear existing widgets
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
        
        # 1. Date Header (Dark Strip)
        header_container = tk.Frame(parent, bg=DATE_BG, pady=8, padx=20)
        header_container.pack(fill="x", pady=(20, 15))
        
        # Date Text
        tk.Label(
            header_container, 
            text=date_text, 
            font=("Helvetica", 16, "bold"), 
            fg=TEXT_MAIN,
            bg=DATE_BG,
            anchor="w"
        ).pack(fill="x")
        
        # 2. Grid Container
        grid_frame = tk.Frame(parent, bg=BG_COLOR)
        grid_frame.pack(fill="x", padx=30)

        # ---------------------------------------------------------
        # GRID LOGIC: 6 Posters per row (Side by Side)
        # ---------------------------------------------------------
        columns_per_row = 6 
        
        for index, movie in enumerate(movies):
            r = index // columns_per_row
            c = index % columns_per_row
            self.create_poster(grid_frame, movie, r, c)

    def create_poster(self, parent, movie, r, c):
        # Canvas for Image
        canvas = tk.Canvas(
            parent,
            width=self.poster_width,
            height=self.poster_height,
            bg="#222", 
            highlightthickness=0
        )
        canvas.grid(row=r, column=c, padx=self.poster_padding, pady=self.poster_padding)

        # Image Loading
        image_path = movie.get('poster_path', 'assets/sample_posters/default.png')
        if not os.path.exists(image_path):
             image_path = os.path.abspath(image_path)
             
        try:
            img = Image.open(image_path)
            img = img.resize((self.poster_width, self.poster_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo) 
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except:
            canvas.create_text(
                self.poster_width//2, self.poster_height//2, 
                text=movie['title'], width=180, font=("Helvetica", 10, "bold"), fill="white"
            )

        # ===============================================================================
        # THE DARK OVERLAY LOGIC (RESTORED & IMPROVED)
        # ===============================================================================
        
        # 1. Solid Dark Overlay (Initially Hidden)
        overlay_rect = canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#111111", # Very dark gray
            outline="",
            state="hidden"
        )

        padding_left = 14
        
        # 2. Title (White, Bold)
        overlay_title = canvas.create_text(
            padding_left, 30,
            text=movie['title'],
            fill="#FFFFFF",
            anchor="nw",
            font=("Helvetica", 14, "bold"),
            width=self.poster_width - 20,
            state="hidden"
        )

        # 3. Rating / Duration (Red Accent)
        overlay_meta = canvas.create_text(
            padding_left, 80,
            text=f"{movie.get('rating', 'N/A')} • {movie.get('duration_minutes', 0)}m",
            fill=ACCENT, 
            anchor="nw",
            font=("Helvetica", 10, "bold"),
            state="hidden"
        )

        # 4. Description (Wrapped Text)
        desc_text = movie.get('description', 'No synopsis available.')
        # Helper to wrap text for canvas
        overlay_desc = canvas.create_text(
            padding_left, 110,
            text=desc_text,
            fill="#CCCCCC",
            anchor="nw",
            font=("Helvetica", 9),
            width=self.poster_width - 25, # Wrap text
            state="hidden"
        )

        # List of items to toggle
        overlay_items = [overlay_rect, overlay_title, overlay_meta, overlay_desc]

        # =================================================================
        # HOVER BINDINGS
        # =================================================================
        def on_enter(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="normal")

        def on_leave(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="hidden")

        def on_click(event):
            self.open_showtimes(movie)

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
