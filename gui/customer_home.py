import tkinter as tk
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

class CustomerHome:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ScreenPass Movie List")
        self.window.geometry("950x600")

        tk.Label(
            self.window,
            text="Now Showing",
            font=("Arial", 22)
        ).pack(pady=20)

        movie_frame = tk.Frame(self.window)
        movie_frame.pack()

        # Fake movie data for hover info
        self.movie_data = {
            "Movie A": {
                "title": "Movie A",
                "year": "2024",
                "rating": "PG-13 • 8.2/10",
                "stars": "Starring John Doe and Anna Bright"
            },
            "Movie B": {
                "title": "Movie B",
                "year": "2023",
                "rating": "R • 7.5/10",
                "stars": "Starring Chris Vale and Mira Sung"
            },
            "Movie C": {
                "title": "Movie C",
                "year": "2022",
                "rating": "PG • 6.9/10",
                "stars": "Starring Aya Rios and Mark Crane"
            },
            "Movie D": {
                "title": "Movie D",
                "year": "2024",
                "rating": "PG • 7.8/10",
                "stars": "Directed by Lianne Frost"
            }
        }

        # Create 4 posters
        self.create_poster(movie_frame, "Movie A")
        self.create_poster(movie_frame, "Movie B")
        self.create_poster(movie_frame, "Movie C")
        self.create_poster(movie_frame, "Movie D")

        tk.Button(
            self.window,
            text="Admin Login",
            command=self.open_admin_login
        ).pack(side="bottom", pady=20)

    def create_poster(self, parent, movie_title):
        info = self.movie_data[movie_title]

        # Canvas poster element
        canvas = tk.Canvas(parent, width=150, height=220, bg="#cccccc", highlightthickness=0)
        canvas.pack(side="left", padx=30)

        # Poster background (placeholder)
        poster_rect = canvas.create_rectangle(0, 0, 150, 220, fill="#cccccc", outline="")
        poster_text = canvas.create_text(
            75, 110,
            text=movie_title,
            fill="black",
            font=("Arial", 12, "bold")
        )

        # Overlay elements
        overlay_rect = canvas.create_rectangle(
            0, 0, 150, 220,
            fill="black",
            stipple="gray50",
            state="hidden"
        )

        overlay_title = canvas.create_text(
            10, 20,
            text=info["title"],
            fill="white",
            anchor="w",
            font=("Arial", 11, "bold"),
            state="hidden"
        )

        overlay_year = canvas.create_text(
            10, 50,
            text=info["year"],
            fill="white",
            anchor="w",
            font=("Arial", 10),
            state="hidden"
        )

        overlay_rating = canvas.create_text(
            10, 80,
            text=info["rating"],
            fill="white",
            anchor="w",
            font=("Arial", 10),
            state="hidden"
        )

        overlay_stars = canvas.create_text(
            10, 110,
            text=info["stars"],
            fill="white",
            anchor="w",
            font=("Arial", 9),
            state="hidden"
        )

        overlay_items = [
            overlay_rect, overlay_title, overlay_year, overlay_rating, overlay_stars
        ]

        # Mouse enter event
        def on_enter(event):
            for item in overlay_items:
                canvas.itemconfigure(item, state="normal")

        # Mouse exit event
        def on_leave(event):
            for item in overlay_items:
                canvas.itemconfigure(item, state="hidden")

        # Click event
        def on_click(event):
            self.open_showtimes(movie_title)

        # Bind events to poster
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

    def open_showtimes(self, movie_title):
        screen = CustomerShowtimeSelect(movie_title)
        screen.run()

    def open_admin_login(self):
        admin = AdminLogin()
        admin.run()

    def run(self):
        self.window.mainloop()
