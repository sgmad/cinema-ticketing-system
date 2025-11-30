import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

# DB Imports
from db.queries import get_movies_by_date
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

class ScrollableFrame(tk.Frame):
    """ A helper class to create a scrollable container """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # The Canvas is the window into the scrolling area
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # The Scrollable Window (This is where we put the movie rows)
        self.scroll_window = tk.Frame(self.canvas, bg="#f0f0f0")

        self.scroll_window.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_window, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling binding
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class CustomerHome:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ScreenPass Movie List")
        self.window.geometry("1100x800")

        # Top Header (Fixed, does not scroll)
        header_frame = tk.Frame(self.window, bg="white", pady=10)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, 
            text="ScreenPass Cinemas", 
            font=("Arial", 24, "bold"), 
            bg="white"
        ).pack(side="left", padx=20)

        tk.Button(
            header_frame, 
            text="Admin Login", 
            command=self.open_admin_login,
            bg="#444", fg="white"
        ).pack(side="right", padx=20)

        # =======================================================
        # SCROLLABLE AREA
        # =======================================================
        self.scroll_container = ScrollableFrame(self.window)
        self.scroll_container.pack(fill="both", expand=True)

        # Settings
        self.poster_width = 200
        self.poster_height = 300
        self.poster_padding = 15
        self.images = [] # Image Garbage Collection prevention

        # Load the next 7 days of movies
        self.load_week_view()

    def load_week_view(self):
        today = datetime.now()
        
        for i in range(7): # Loop through next 7 days
            date_obj = today + timedelta(days=i)
            date_str = date_obj.strftime('%Y-%m-%d')
            display_date = date_obj.strftime("%A, %d %B") # e.g., "Monday, 30 October"
            
            # Fetch movies for this specific day
            movies = get_movies_by_date(date_str)
            
            # Only show the day section if there are movies playing
            if movies:
                self.create_day_section(display_date, movies)

    def create_day_section(self, date_text, movies):
        """ Creates a header and a GRID of posters for a specific day """
        parent = self.scroll_container.scroll_window
        
        # 1. Date Header
        header = tk.Label(
            parent, 
            text=date_text, 
            font=("Arial", 16, "bold"), 
            fg="#333",
            bg="#f0f0f0",
            anchor="w"
        )
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # 2. Poster Container
        row_frame = tk.Frame(parent, bg="#f0f0f0")
        row_frame.pack(fill="x", padx=20)

        # ---------------------------------------------------------
        # GRID LOGIC: 5 Posters per row, then wrap
        # ---------------------------------------------------------
        columns_per_row = 5 
        
        for index, movie in enumerate(movies):
            # Calculate grid position
            row_pos = index // columns_per_row
            col_pos = index % columns_per_row
            
            # Pass these coordinates to the poster creator
            self.create_poster(row_frame, movie, row_pos, col_pos)
            
        # Divider Line
        tk.Frame(parent, height=1, bg="#ccc").pack(fill="x", pady=20, padx=20)

    def create_poster(self, parent, movie, r, c):
        canvas = tk.Canvas(
            parent,
            width=self.poster_width,
            height=self.poster_height,
            bg="#444",
            highlightthickness=0
        )
        
        # CHANGE: Use Grid instead of Pack
        canvas.grid(row=r, column=c, padx=10, pady=10)

        # Image Loading (Same as before)
        image_path = movie.get('poster_path', 'assets/sample_posters/default.png')
        if not os.path.exists(image_path):
             image_path = os.path.abspath(image_path)
             
        try:
            img = Image.open(image_path)
            img = img.resize((self.poster_width, self.poster_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo) 
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            canvas.create_rectangle(0, 0, self.poster_width, self.poster_height, fill="#dddddd")
            canvas.create_text(self.poster_width//2, self.poster_height//2, text=movie['title'], width=180)

        # Click event
        canvas.bind("<Button-1>", lambda e: self.open_showtimes(movie))

    def open_showtimes(self, movie_dict):
        # CHANGE: Pass the whole dictionary, not just the title
        screen = CustomerShowtimeSelect(movie_dict) 
        screen.run()

    def open_admin_login(self):
        admin = AdminLogin()
        admin.run()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CustomerHome()
    app.run()