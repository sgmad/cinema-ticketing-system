import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk # pip install pillow
import os

# Import database function
from db.queries import get_all_movies
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

        # Poster layout settings
        self.poster_width = 220
        self.poster_height = 330
        self.poster_padding = 28

        movie_frame = tk.Frame(self.window)
        movie_frame.pack()

        # =======================================================
        # Fetch real data from MySQL
        # =======================================================
        self.movies = get_all_movies() # Returns a list of dictionaries

        # If DB is empty
        if not self.movies:
            tk.Label(movie_frame, text="No movies found in database.").pack()

        # Create a poster for every movie found in the DB
        for movie_dict in self.movies:
            self.create_poster(movie_frame, movie_dict)

        tk.Button(
            self.window,
            text="Admin Login",
            command=self.open_admin_login
        ).pack(side="bottom", pady=20)

    # =====================================================================
    # Modified to accept a 'movie_dict' directly from DB
    # =====================================================================
    def create_poster(self, parent, movie):
        # movie is: {'id': 1, 'title': 'Test Movie', 'poster_path': '...', ...}
        
        canvas = tk.Canvas(
            parent,
            width=self.poster_width,
            height=self.poster_height,
            bg="#444444",
            highlightthickness=0
        )
        canvas.pack(side="left", padx=self.poster_padding)

        # ---------------------------------------------------------
        # IMAGE LOADING LOGIC
        # ---------------------------------------------------------
        # Tkinter requires keeping a reference to images or garbage collector deletes them
        if not hasattr(self, 'images'):
            self.images = []

        image_path = movie.get('poster_path', 'assets/sample_posters/default.png')
        
        # Fallback if file doesn't exist
        if not os.path.exists(image_path):
            print(f"Warning: Image not found at {image_path}")
            # You could set a default placeholder here if you wanted
        
        try:
            # Load and Resize Image to fit poster size
            img = Image.open(image_path)
            img = img.resize((self.poster_width, self.poster_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Keep reference
            self.images.append(photo)
            
            # Draw Image
            canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Draw gray rectangle if image fails
            canvas.create_rectangle(0, 0, self.poster_width, self.poster_height, fill="#dddddd")

        # ---------------------------------------------------------
        # OVERLAY LOGIC (Same as before, just using dictionary keys)
        # ---------------------------------------------------------
        overlay_rect = canvas.create_rectangle(
            0, 0, self.poster_width, self.poster_height,
            fill="#111111", outline="", state="hidden"
        )

        padding_left = 16
        
        # Title
        overlay_title = canvas.create_text(
            padding_left, 30,
            text=movie['title'],
            fill="white", anchor="nw",
            font=("Arial", 14, "bold"), state="hidden"
        )

        # Rating / Duration
        overlay_rating = canvas.create_text(
            padding_left, 65,
            text=f"{movie['rating']} • {movie['duration_minutes']}m",
            fill="white", anchor="nw",
            font=("Arial", 12), state="hidden"
        )

        # Description (Wrapped)
        desc_text = movie.get('description', 'No description')
        desc_lines = self.wrap_text(desc_text, self.poster_width - 2 * padding_left)
        
        overlay_desc_items = []
        y_pos = 100
        for line in desc_lines[:8]: # Limit to 8 lines so it doesn't overflow
            item = canvas.create_text(
                padding_left, y_pos,
                text=line,
                fill="#cccccc", anchor="nw",
                font=("Arial", 10), state="hidden"
            )
            overlay_desc_items.append(item)
            y_pos += 18

        overlay_items = [overlay_rect, overlay_title, overlay_rating] + overlay_desc_items

        # Hover Bindings
        def on_enter(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="normal")

        def on_leave(event):
            for it in overlay_items:
                canvas.itemconfigure(it, state="hidden")

        # Click Binding - Pass the Movie ID now!
        def on_click(event):
            self.open_showtimes(movie)

        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        canvas.bind("<Button-1>", on_click)

    def wrap_text(self, text, max_width, font=("Arial", 10)):
        f = tkfont.Font(font=font)
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = current + " " + word if current else word
            if f.measure(test) <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        if current: lines.append(current)
        return lines

    def open_showtimes(self, movie_dict):
        # We pass the WHOLE dictionary now, not just title
        print(f"Opening showtimes for: {movie_dict['title']} (ID: {movie_dict['id']})")
        # You will need to update CustomerShowtimeSelect next!
        screen = CustomerShowtimeSelect(movie_dict['title']) 
        screen.run()

    def open_admin_login(self):
        admin = AdminLogin()
        admin.run()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CustomerHome()
    app.run()
