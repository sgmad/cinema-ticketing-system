import tkinter as tk
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

class CustomerHome:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ScreenPass Movie List")
        self.window.geometry("1100x700")

        tk.Label(
            self.window,
            text="Now Showing",
            font=("Arial", 24)
        ).pack(pady=20)

        self.poster_width = 220
        self.poster_height = 330
        self.poster_padding = 28

        movie_frame = tk.Frame(self.window)
        movie_frame.pack()

        # movie data starring ma frends
        self.movie_data = {
            "Movie A": {
                "title": "Movie A",
                "year": "2024",
                "rating": "PG-13 • 8.2/10",
                "stars": "Starring Kyle Guadz and Aubreng Olario"
            },
            "Movie B": {
                "title": "Movie B",
                "year": "2023",
                "rating": "R • 7.5/10",
                "stars": "Starring James Homer and Kyle Adz"
            },
            "Movie C": {
                "title": "Movie C",
                "year": "2022",
                "rating": "PG • 6.9/10",
                "stars": "Starring Jonathan ManinGO and Steven Deliverables"
            },
            "Movie D": {
                "title": "Movie D",
                "year": "2024",
                "rating": "PG • 7.8/10",
                "stars": "Directed by Sam Tomorrow"
            }
        }

        # create 4 posters
        for title in self.movie_data:
            self.create_poster(movie_frame, title)

        tk.Button(
            self.window,
            text="Admin Login",
            command=self.open_admin_login
        ).pack(side="bottom", pady=20)

    def create_poster(self, parent, movie_title):
        info = self.movie_data[movie_title]

        canvas = tk.Canvas(
            parent,
            width=self.poster_width,
            height=self.poster_height,
            bg="#444444",
            highlightthickness=0
        )
        canvas.pack(side="left", padx=self.poster_padding)

        # base poster rectangle
        canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#dddddd",
            outline=""
        )

        # placeholder title text
        canvas.create_text(
            self.poster_width // 2,
            self.poster_height // 2,
            text=movie_title,
            fill="black",
            font=("Arial", 14, "bold")
        )

        # ----- solid overlay -----
        overlay_rect = canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#111111",
            outline="",
            state="hidden"
        )

        # overlay text items
        title_text = canvas.create_text(
            12, 20,
            text=info["title"],
            fill="white",
            anchor="nw",
            font=("Arial", 12, "bold"),
            state="hidden"
        )

        year_text = canvas.create_text(
            12, 50,
            text=info["year"],
            fill="white",
            anchor="nw",
            font=("Arial", 10),
            state="hidden"
        )

        rating_text = canvas.create_text(
            12, 75,
            text=info["rating"],
            fill="white",
            anchor="nw",
            font=("Arial", 10),
            state="hidden"
        )

        stars_text = canvas.create_text(
            12, 100,
            text=info["stars"],
            fill="white",
            anchor="nw",
            font=("Arial", 9),
            state="hidden"
        )

        overlay_items = [
            overlay_rect,
            title_text,
            year_text,
            rating_text,
            stars_text
        ]

        # hover functions
        def on_enter(event):
            for item in overlay_items:
                canvas.itemconfigure(item, state="normal")

        def on_leave(event):
            for item in overlay_items:
                canvas.itemconfigure(item, state="hidden")

        def on_click(event, t=movie_title):
            self.open_showtimes(t)

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


if __name__ == "__main__":
    app = CustomerHome()
    app.run()
