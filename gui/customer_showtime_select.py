import tkinter as tk

class CustomerShowtimeSelect:
    def __init__(self, movie_title="[Unknown Movie]"):
        self.window = tk.Toplevel()
        self.window.title(f"Showtimes for {movie_title}")
        self.window.geometry("500x380")

        # Placeholder info per movie
        self.movie_info = {
            "Movie A": {
                "year": "2024",
                "duration": "2h 15m",
                "genre": "Romance",
                "showtimes": ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM"]
            },
            "Movie B": {
                "year": "2023",
                "duration": "1h 55m",
                "genre": "Drama",
                "showtimes": ["11:30 AM", "2:45 PM", "6:10 PM"]
            },
            "Movie C": {
                "year": "2022",
                "duration": "2h 5m",
                "genre": "Comedy",
                "showtimes": ["9:20 AM", "12:00 PM", "3:00 PM", "8:20 PM"]
            },
            "Movie D": {
                "year": "2024",
                "duration": "2h 40m",
                "genre": "Sci-Fi",
                "showtimes": ["1:10 PM", "5:00 PM", "9:00 PM"]
            }
        }

        info = self.movie_info.get(movie_title, {
            "year": "-",
            "duration": "-",
            "genre": "-",
            "showtimes": []
        })

        header = tk.Label(
            self.window,
            text=f"{movie_title} ({info['year']})",
            font=("Arial", 18)
        )
        header.pack(pady=10)

        sub = tk.Label(
            self.window,
            text=f"{info['genre']}  •  {info['duration']}",
            font=("Arial", 12)
        )
        sub.pack(pady=(0, 20))

        showtime_frame = tk.Frame(self.window)
        showtime_frame.pack()

        # Create buttons for each showtime
        for st in info["showtimes"]:
            tk.Button(
                showtime_frame,
                text=st,
                width=12,
                font=("Arial", 11),
                command=lambda t=st: self.select_showtime(movie_title, t)
            ).pack(pady=5)

        tk.Button(
            self.window,
            text="Back",
            command=self.window.destroy
        ).pack(pady=20)

    def select_showtime(self, movie, time):
        # This will eventually open the seat map screen
        print(f"Selected showtime: {movie} at {time}")

    def run(self):
        self.window.mainloop()
