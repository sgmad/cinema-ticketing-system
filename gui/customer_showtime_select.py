import tkinter as tk
from tkinter import ttk
from datetime import datetime
from db.queries import get_showtimes_for_movie
from gui.seat_map import SeatMap

class CustomerShowtimeSelect:
    def __init__(self, movie_data):
        """
        movie_data is a dictionary containing: 
        {'id': 1, 'title': '...', 'genre': '...', 'description': '...', ...}
        """
        self.movie = movie_data
        
        self.window = tk.Toplevel()
        self.window.title(f"Showtimes - {self.movie['title']}")
        self.window.geometry("600x600")
        self.window.configure(bg="white")

        # ==========================================
        # 1. MOVIE DETAILS HEADER
        # ==========================================
        header_frame = tk.Frame(self.window, bg="white", padx=20, pady=20)
        header_frame.pack(fill="x")

        # Title & Year
        tk.Label(
            header_frame, 
            text=self.movie['title'], 
            font=("Arial", 22, "bold"), 
            bg="white", fg="#333"
        ).pack(anchor="w")

        # Meta Info (Genre | Duration | Rating)
        meta_text = f"{self.movie.get('genre', 'Unknown')}  •  {self.movie.get('duration_minutes', 0)} mins  •  {self.movie.get('rating', 'N/A')}"
        tk.Label(
            header_frame, 
            text=meta_text, 
            font=("Arial", 11), 
            fg="#666", bg="white"
        ).pack(anchor="w", pady=(5, 10))

        # Description
        desc_text = self.movie.get('description', 'No synopsis available.')
        tk.Label(
            header_frame, 
            text=desc_text, 
            font=("Arial", 10), 
            wraplength=550, 
            justify="left", 
            bg="white"
        ).pack(anchor="w")

        tk.Frame(self.window, height=1, bg="#ddd").pack(fill="x", padx=20, pady=10)

        # ==========================================
        # 2. SHOWTIME LIST (Scrollable)
        # ==========================================
        lbl_schedule = tk.Label(self.window, text="Select a Showtime", font=("Arial", 14, "bold"), bg="white")
        lbl_schedule.pack(anchor="w", padx=20, pady=(0, 10))

        # Create a scrollable container for the times
        container = tk.Frame(self.window)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load real showtimes
        self.load_showtimes(scrollable_frame)

    def load_showtimes(self, parent_frame):
        # 1. Fetch from DB
        showtimes = get_showtimes_for_movie(self.movie['id'])

        if not showtimes:
            tk.Label(parent_frame, text="No upcoming showtimes found.", bg="white", fg="gray").pack(pady=20)
            return

        # 2. Group by Date
        # Logic: We want to display headers like "Monday, 30 Oct"
        grouped_shows = {}
        for st in showtimes:
            # st['start_time'] is a datetime object
            date_key = st['start_time'].strftime("%A, %d %B") # e.g. "Monday, 30 October"
            if date_key not in grouped_shows:
                grouped_shows[date_key] = []
            grouped_shows[date_key].append(st)

        # 3. Create UI Elements
        for date_str, shows_list in grouped_shows.items():
            # Date Header
            tk.Label(
                parent_frame, 
                text=date_str, 
                font=("Arial", 11, "bold"), 
                bg="#f0f0f0", 
                width=60, anchor="w", padx=10, pady=5
            ).pack(fill="x", pady=(10, 5))

            # Buttons Container
            btn_frame = tk.Frame(parent_frame, bg="white")
            btn_frame.pack(fill="x", pady=(0, 10), padx=10)

            for show in shows_list:
                time_str = show['start_time'].strftime("%I:%M %p") # 02:30 PM
                hall_name = show['hall_name']
                price = show['price_standard']
                
                # Button Text: "02:30 PM\nCinema 1 (₱730)"
                btn_text = f"{time_str}\n{hall_name} (₱{price})"
                
                btn = tk.Button(
                    btn_frame,
                    text=btn_text,
                    font=("Arial", 9),
                    bg="#e1f5fe",
                    relief="flat",
                    width=18,
                    height=3,
                    # We pass the ID and the info to the next function
                    command=lambda s=show: self.select_showtime(s)
                )
                btn.pack(side="left", padx=5, pady=5)

    def select_showtime(self, showtime_dict):
        # Inject the movie title from the parent class so SeatMap knows it
        showtime_dict['movie_title'] = self.movie['title'] 
        
        seat_screen = SeatMap(showtime_dict)
        seat_screen.run()

    def run(self):
        self.window.mainloop()
