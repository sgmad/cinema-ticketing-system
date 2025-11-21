import tkinter as tk

class CustomerShowtimeSelect:
    def __init__(self, movie_title="[Unknown Movie]"):
        self.window = tk.Toplevel()
        self.window.title(f"Showtimes for {movie_title}")
        self.window.geometry("500x480")

        self.movie_info = {
            "Movie A": {
                "year": "2024",
                "duration": "2h 15m",
                "genre": "Romance",
                "synopsis": "Two friends connect by chance and discover a connection that changes their lives.",
                "review": "Well paced and emotionally grounded. -KingReviews",
                "showtimes": ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM"]
            },
            "Movie B": {
                "year": "2023",
                "duration": "1h 55m",
                "genre": "Drama",
                "synopsis": "A family confronts an unresolved past during a single turbulent weekend.",
                "review": "Strong performances and tight writing. -MovieCritic",
                "showtimes": ["11:30 AM", "2:45 PM", "6:10 PM"]
            },
            "Movie C": {
                "year": "2022",
                "duration": "2h 5m",
                "genre": "Comedy",
                "synopsis": "A failing restaurant owner turns to absurd schemes to save the business.",
                "review": "Light, simple, and consistently funny. -MediaWatch",
                "showtimes": ["9:20 AM", "12:00 PM", "3:00 PM", "8:20 PM"]
            },
            "Movie D": {
                "year": "2024",
                "duration": "2h 40m",
                "genre": "Sci-Fi",
                "synopsis": "The Creator but good.",
                "review": "Visually striking with strong world-building. -CinephileDaily",
                "showtimes": ["1:10 PM", "5:00 PM", "9:00 PM"]
            }
        }

        info = self.movie_info.get(movie_title, {
            "year": "-",
            "duration": "-",
            "genre": "-",
            "synopsis": "No synopsis available.",
            "review": "No review available.",
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
        sub.pack(pady=(0, 10))

        synopsis_label = tk.Label(
            self.window,
            text=info["synopsis"],
            font=("Arial", 11),
            wraplength=450,
            justify="left"
        )
        synopsis_label.pack(pady=(0, 8))

        review_label = tk.Label(
            self.window,
            text=f"Review: {info['review']}",
            font=("Arial", 10),
            wraplength=450,
            justify="left"
        )
        review_label.pack(pady=(0, 20))

        showtime_frame = tk.Frame(self.window)
        showtime_frame.pack()

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
        print(f"Selected showtime: {movie} at {time}")

    def run(self):
        self.window.mainloop()
