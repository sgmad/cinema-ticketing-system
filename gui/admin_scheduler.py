import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # pip install tkcalendar
from db.queries import get_all_movies, get_all_halls, add_showtime

class AdminScheduler:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Schedule Showtime")
        self.window.geometry("400x500")

        # FETCH DATA FOR DROPDOWNS
        self.movies = get_all_movies() # [{'id':1, 'title':'...'}, ...]
        self.halls = get_all_halls()   # [{'id':1, 'name':'Cinema 1'}, ...]

        if not self.halls:
            messagebox.showerror("Error", "No Halls found in database. Please add halls via SQL first.")
            self.window.destroy()
            return

        # Prepare lists for Comboboxes
        self.movie_titles = [m['title'] for m in self.movies]
        self.hall_names = [h['name'] for h in self.halls]

        # UI LAYOUT
        tk.Label(self.window, text="Add New Showtime", font=("Arial", 16, "bold")).pack(pady=20)

        # 1. Select Movie
        tk.Label(self.window, text="Select Movie:").pack(anchor="w", padx=40)
        self.cb_movie = ttk.Combobox(self.window, values=self.movie_titles, state="readonly", width=30)
        self.cb_movie.pack(pady=5)

        # 2. Select Hall
        tk.Label(self.window, text="Select Hall:").pack(anchor="w", padx=40)
        self.cb_hall = ttk.Combobox(self.window, values=self.hall_names, state="readonly", width=30)
        self.cb_hall.pack(pady=5)

        # 3. Select Date (Requires tkcalendar)
        # If you don't want to install tkcalendar, use a simple Entry widget: YYYY-MM-DD
        tk.Label(self.window, text="Date:").pack(anchor="w", padx=40)
        try:
            self.cal_date = DateEntry(self.window, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        except:
            # Fallback if library missing
            self.cal_date = tk.Entry(self.window, width=33)
            self.cal_date.insert(0, "2025-10-30")
        self.cal_date.pack(pady=5)

        # 4. Select Time
        tk.Label(self.window, text="Time (HH:MM 24hr format):").pack(anchor="w", padx=40)
        self.entry_time = tk.Entry(self.window, width=33)
        self.entry_time.insert(0, "14:00")
        self.entry_time.pack(pady=5)

        # 5. Price
        tk.Label(self.window, text="Price ($):").pack(anchor="w", padx=40)
        self.entry_price = tk.Entry(self.window, width=33)
        self.entry_price.insert(0, "12.50")
        self.entry_price.pack(pady=5)

        # Save Button
        tk.Button(
            self.window, 
            text="Create Showtime", 
            bg="#4CAF50", fg="white",
            command=self.save_schedule
        ).pack(pady=30)

    def save_schedule(self):
        # 1. Get Selected Data
        movie_idx = self.cb_movie.current()
        hall_idx = self.cb_hall.current()
        
        if movie_idx == -1 or hall_idx == -1:
            messagebox.showerror("Error", "Please select a movie and a hall.")
            return

        movie_id = self.movies[movie_idx]['id']
        hall_id = self.halls[hall_idx]['id']
        
        # 2. Format Date/Time
        # Needs to be 'YYYY-MM-DD HH:MM:SS'
        date_str = self.cal_date.get() # "2025-10-30"
        time_str = self.entry_time.get() # "14:00"
        
        # Simple validation
        if len(time_str) != 5:
             messagebox.showerror("Error", "Time must be in HH:MM format (e.g. 09:30 or 14:00)")
             return

        final_datetime = f"{date_str} {time_str}:00"
        price = self.entry_price.get()

        # 3. Insert to DB
        success = add_showtime(movie_id, hall_id, final_datetime, float(price))

        if success:
            messagebox.showinfo("Success", "Showtime added!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Failed to add showtime.")

    def run(self):
        self.window.mainloop()

# Test
if __name__ == "__main__":
    AdminScheduler().run()