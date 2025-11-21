import tkinter as tk
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect
import tkinter.font as tkfont

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

        # Poster layout BIG
        self.poster_width = 220
        self.poster_height = 330
        self.poster_padding = 28

        movie_frame = tk.Frame(self.window)
        movie_frame.pack()

        # Made up movie data starring mah frens
        self.movie_data = {
            "Movie A": {
                "title": "Movie A",
                "year": "2025",
                "rating": "PG-13 • 8.2/10",
                "stars": "Starring Kyle Guadz and Aubreng Olario"
            },
            "Movie B": {
                "title": "Movie B",
                "year": "2025",
                "rating": "R • 7.5/10",
                "stars": "Starring James Homer and Kyle Adz"
            },
            "Movie C": {
                "title": "Movie C",
                "year": "2025",
                "rating": "PG • 6.9/10",
                "stars": "Starring Jonathan Manigs and Steven Deliverables"
            },
            "Movie D": {
                "title": "Movie D",
                "year": "2025",
                "rating": "PG • 7.8/10",
                "stars": "Directed by Sam Ugmad"
            }
        }

        # Creates the 4 posters
        for title in self.movie_data:
            self.create_poster(movie_frame, title)

        tk.Button(
            self.window,
            text="Admin Login",
            command=self.open_admin_login
        ).pack(side="bottom", pady=20)

    # =====================================================================
    # Poster creation
    # =====================================================================
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

        # Poster placeholder rectangle
        canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#dddddd",
            outline=""
        )

        # Centered placeholder title text
        canvas.create_text(
            self.poster_width // 2,
            self.poster_height // 2,
            text=movie_title,
            fill="black",
            font=("Arial", 16, "bold")
        )

        # ===============================================================================
        # Solid overlay because tkinter can't do semi-transparent colors (Install PyQt5?)
        # ===============================================================================
        overlay_rect = canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#111111",
            outline="",
            state="hidden"
        )

        # Padding for overlay text
        padding_left = 16

        # Title
        overlay_title = canvas.create_text(
            padding_left, 30,
            text=info["title"],
            fill="white",
            anchor="nw",
            font=("Arial", 14, "bold"),
            state="hidden"
        )

        # Year just below title
        overlay_year = canvas.create_text(
            padding_left, 65,
            text=info["year"],
            fill="white",
            anchor="nw",
            font=("Arial", 12),
            state="hidden"
        )

        # Rating
        overlay_rating = canvas.create_text(
            padding_left, 95,
            text=info["rating"],
            fill="white",
            anchor="nw",
            font=("Arial", 12),
            state="hidden"
        )

        # Stars text, but wrapped manually
        stars_lines = self.wrap_text(info["stars"], max_width=self.poster_width - 2 * padding_left, font=("Arial", 11))

        overlay_stars_items = []
        stars_y = 130
        for line in stars_lines:
            item = canvas.create_text(
                padding_left, stars_y,
                text=line,
                fill="white",
                anchor="nw",
                font=("Arial", 11),
                state="hidden"
            )
            overlay_stars_items.append(item)
            stars_y += 20

        # Items to show or hide on hover
        overlay_items = [overlay_rect, overlay_title, overlay_year, overlay_rating] + overlay_stars_items

        # =================================================================
        # Hover logic
        # =================================================================
        def on_enter(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="normal")

        def on_leave(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="hidden")

        def on_click(event, t=movie_title):
            self.open_showtimes(t)

        # Hover and click binding
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

    # ==================================
    # Basic word wrap using font.measure
    # ==================================
    def wrap_text(self, text, max_width, font=("Arial", 11)):
        """
        Wrap text to fit within max_width using a tkinter Font measurement.
        Returns a list of lines that fit.
        """
        f = tkfont.Font(font=font)
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test_line = current + (" " if current else "") + word
            if f.measure(test_line) <= max_width:
                current = test_line
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines

    # =====================================================================
    # Navigation
    # =====================================================================
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
