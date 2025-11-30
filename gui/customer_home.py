import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
from datetime import datetime, timedelta

# DB Imports
from db.queries import get_movies_by_date
from gui.admin_login import AdminLogin
from gui.customer_showtime_select import CustomerShowtimeSelect

class CustomerHome:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ScreenPass Movie List")
        self.window.geometry("1100x750") # Made slightly taller for date bar

        # Header
        tk.Label(self.window, text="Now Showing", font=("Arial", 24, "bold")).pack(pady=(20, 10))

        # =======================================================
        # 1. DATE SELECTOR BAR
        # =======================================================
        self.date_frame = tk.Frame(self.window)
        self.date_frame.pack(pady=10)

        # Generate next 7 days
        self.selected_date_btn = None
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Create buttons for the next 7 days
        today = datetime.now()
        for i in range(7):
            date_obj = today + timedelta(days=i)
            date_str = date_obj.strftime('%Y-%m-%d')
            
            # Format display text (e.g., "Mon\n30 Oct")
            day_name = date_obj.strftime("%a")
            day_num = date_obj.strftime("%d %b")
            display_text = f"{day_name}\n{day_num}"

            btn = tk.Button(
                self.date_frame,
                text=display_text,
                width=8,
                height=2,
                relief="flat",
                bg="#e0e0e0",
                command=lambda d=date_str, b=i: self.select_date(d, b)
            )
            btn.pack(side="left", padx=5)
            
            # Save reference to button 0 (Today) so we can highlight it initially
            if i == 0:
                self.btn_today = btn

        # =======================================================
        # 2. MOVIE CONTAINER
        # =======================================================
        # We need a scrollable area in case there are many movies? 
        # For now, let's keep it simple with a standard frame.
        self.movie_frame = tk.Frame(self.window)
        self.movie_frame.pack(pady=10, fill="both", expand=True)
        
        # Configuration for posters
        self.poster_width = 220
        self.poster_height = 330
        self.poster_padding = 28
        self.images = [] # Prevent garbage collection

        # Load "Today" by default
        self.select_date(self.current_date, 0, btn_obj=self.btn_today)

        # Admin Button at bottom
        tk.Button(self.window, text="Admin Login", command=self.open_admin_login).pack(side="bottom", pady=20)

    def select_date(self, date_str, index, btn_obj=None):
        """ Handles visual highlighting of dates and data fetching """
        self.current_date = date_str
        
        # Reset all buttons to gray
        for widget in self.date_frame.winfo_children():
            widget.configure(bg="#e0e0e0", fg="black")

        # Highlight the clicked button (or passed object)
        if btn_obj:
            target_btn = btn_obj
        else:
            # Find the button by index if object not passed
            target_btn = self.date_frame.winfo_children()[index]
            
        target_btn.configure(bg="#2196F3", fg="white") # Blue active state

        # Refresh the movies
        self.load_movies_for_date(date_str)

    def load_movies_for_date(self, date_str):
        """ Clears the screen and loads movies playing on date_str """
        
        # 1. Clear existing posters
        for widget in self.movie_frame.winfo_children():
            widget.destroy()
        self.images = [] # Clear image cache

        # 2. Fetch from DB
        movies = get_movies_by_date(date_str)

        if not movies:
            tk.Label(
                self.movie_frame, 
                text=f"No showtimes scheduled for {date_str}", 
                fg="gray", font=("Arial", 12)
            ).pack(pady=50)
            return

        # 3. Create Posters
        for movie_dict in movies:
            self.create_poster(self.movie_frame, movie_dict)

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
