import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db.queries import get_all_movies, get_all_halls, add_showtime, get_all_showtimes_full, delete_showtime, update_showtime
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

class AdminScheduler:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Manage Schedules")
        
        # 1. CENTERED & WIDER
        w, h = 1000, 600
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = int(sw/2 - w/2)
        y = int(sh/2 - h/2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        self.window.configure(bg="#f0f0f0")

        self.current_edit_id = None # Tracks if we are editing

        # FETCH DATA
        self.movies = get_all_movies() 
        self.halls = get_all_halls()

        if not self.halls:
            messagebox.showerror("Error", "No Halls found. Please add halls first.", parent=self.window)
            self.window.destroy()
            return

        self.movie_titles = [m['title'] for m in self.movies]
        self.hall_names = [h['name'] for h in self.halls]

        # ==========================================
        # LEFT SIDE: FORM
        # ==========================================
        frame_left = tk.Frame(self.window, width=350, bg="#f0f0f0", padx=20, pady=20)
        frame_left.pack(side="left", fill="y")
        
        self.lbl_header = tk.Label(frame_left, text="Add Showtime", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.lbl_header.pack(pady=(0, 20))

        def add_field(label, widget):
            tk.Label(frame_left, text=label, font=("Arial", 9, "bold"), bg="#f0f0f0", fg="#555").pack(anchor="w", pady=(5, 2))
            widget.pack(fill="x", pady=(0, 10))
            return widget

        # 1. Movie
        self.cb_movie = ttk.Combobox(frame_left, values=self.movie_titles, state="readonly", font=("Arial", 10))
        add_field("Select Movie:", self.cb_movie)

        # 2. Hall
        self.cb_hall = ttk.Combobox(frame_left, values=self.hall_names, state="readonly", font=("Arial", 10))
        add_field("Select Hall:", self.cb_hall)

        # 3. Date
        if DateEntry:
            self.cal_date = DateEntry(frame_left, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=("Arial", 10))
        else:
            self.cal_date = tk.Entry(frame_left, font=("Arial", 10))
            self.cal_date.insert(0, "YYYY-MM-DD")
        add_field("Date:", self.cal_date)

        # 4. Time
        self.entry_time = tk.Entry(frame_left, font=("Arial", 10))
        self.entry_time.insert(0, "14:00")
        add_field("Time (HH:MM):", self.entry_time)

        # 5. Price
        self.entry_price = tk.Entry(frame_left, font=("Arial", 10))
        self.entry_price.insert(0, "350.00")
        add_field("Price (₱):", self.entry_price)

        # Buttons
        self.btn_save = tk.Button(
            frame_left, text="Add Schedule", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
            pady=8, cursor="hand2", command=self.save_schedule
        )
        self.btn_save.pack(fill="x", pady=20)

        self.btn_clear = tk.Button(
            frame_left, text="Clear / Cancel", bg="#999", fg="white", font=("Arial", 10),
            pady=5, cursor="hand2", command=self.clear_form
        )
        self.btn_clear.pack(fill="x")

        tk.Button(
            frame_left, text="Delete Selected", bg="#f44336", fg="white", font=("Arial", 10),
            pady=5, cursor="hand2", command=self.delete_selected
        ).pack(fill="x", pady=(10,0))

        # ==========================================
        # RIGHT SIDE: LIST
        # ==========================================
        frame_right = tk.Frame(self.window, bg="white", padx=20, pady=20)
        frame_right.pack(side="right", fill="both", expand=True)

        tk.Label(frame_right, text="Click row to Edit", font=("Arial", 12, "bold"), bg="white").pack(anchor="nw")

        cols = ("ID", "Date", "Time", "Movie", "Hall", "Price")
        self.tree = ttk.Treeview(frame_right, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=40)
        self.tree.heading("Date", text="Date"); self.tree.column("Date", width=90)
        self.tree.heading("Time", text="Time"); self.tree.column("Time", width=70)
        self.tree.heading("Movie", text="Movie"); self.tree.column("Movie", width=180)
        self.tree.heading("Hall", text="Hall"); self.tree.column("Hall", width=120)
        self.tree.heading("Price", text="Price"); self.tree.column("Price", width=70)

        scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind Click
        self.tree.bind("<<TreeviewSelect>>", self.on_schedule_select)
        self.load_data()

    def on_schedule_select(self, event):
        sel = self.tree.selection()
        if not sel: return

        # Get values from the treeview row
        item = self.tree.item(sel)
        vals = item['values'] # [id, date, time, movie, hall, price]
        
        self.current_edit_id = vals[0]
        
        # Populate Form
        # 1. Movie & Hall (Find index in list to set combobox)
        if vals[3] in self.movie_titles:
            self.cb_movie.current(self.movie_titles.index(vals[3]))
        if vals[4] in self.hall_names:
            self.cb_hall.current(self.hall_names.index(vals[4]))
            
        # 2. Date & Time
        if DateEntry:
            self.cal_date.set_date(vals[1]) # tkcalendar method
        else:
            self.cal_date.delete(0, 'end'); self.cal_date.insert(0, vals[1])
            
        self.entry_time.delete(0, 'end'); self.entry_time.insert(0, vals[2])
        
        # 3. Price (Strip currency symbol if present)
        price_clean = str(vals[5]).replace("₱", "").replace("$", "")
        self.entry_price.delete(0, 'end'); self.entry_price.insert(0, price_clean)

        # UI State
        self.lbl_header.config(text=f"Edit Schedule #{self.current_edit_id}", fg="#2196F3")
        self.btn_save.config(text="Update Schedule", bg="#2196F3")

    def save_schedule(self):
        movie_idx = self.cb_movie.current()
        hall_idx = self.cb_hall.current()
        
        if movie_idx == -1 or hall_idx == -1:
            messagebox.showerror("Error", "Please select a movie and a hall.", parent=self.window)
            return

        movie_id = self.movies[movie_idx]['id']
        hall_id = self.halls[hall_idx]['id']
        date_str = self.cal_date.get()
        time_str = self.entry_time.get()
        
        if len(time_str) != 5 or ":" not in time_str:
             messagebox.showerror("Error", "Time must be in HH:MM format", parent=self.window)
             return

        final_datetime = f"{date_str} {time_str}:00"
        
        try:
            price = float(self.entry_price.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.", parent=self.window)
            return

        # =====================================================
        # LOGIC WITH CONFLICT CHECKING & PARENT WINDOW FIX
        # =====================================================
        
        if self.current_edit_id:
            # UPDATE
            success, msg = update_showtime(self.current_edit_id, movie_id, hall_id, final_datetime, price)
            
            if success:
                messagebox.showinfo("Success", "Schedule updated!", parent=self.window)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Scheduling Failed", msg, parent=self.window)
        else:
            # ADD NEW
            success, msg = add_showtime(movie_id, hall_id, final_datetime, price)
            
            if success:
                messagebox.showinfo("Success", "Showtime added!", parent=self.window)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Scheduling Failed", msg, parent=self.window)

    def clear_form(self):
        self.current_edit_id = None
        self.entry_time.delete(0, 'end'); self.entry_time.insert(0, "14:00")
        self.entry_price.delete(0, 'end'); self.entry_price.insert(0, "350.00")
        self.cb_movie.set(''); self.cb_hall.set('')
        
        self.lbl_header.config(text="Add Showtime", fg="black")
        self.btn_save.config(text="Add Schedule", bg="#4CAF50")
        
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a schedule to delete.", parent=self.window)
            return

        if messagebox.askyesno("Confirm", "Delete this showtime?", parent=self.window):
            item_id = self.tree.item(sel)['values'][0]
            if delete_showtime(item_id):
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Could not delete. Check if tickets are sold for this time.", parent=self.window)

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        for s in get_all_showtimes_full():
            dt = s['start_time']
            d_str = dt.strftime("%Y-%m-%d")
            t_str = dt.strftime("%H:%M")
            self.tree.insert("", "end", values=(s['id'], d_str, t_str, s['movie_title'], s['hall_name'], f"₱{s['price_standard']}"))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    AdminScheduler().run()
