import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# OOP IMPORTS
from gui.base_window import BaseWindow
from db.db_manager import DatabaseManager

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

class AdminScheduler(BaseWindow):
    def __init__(self):
        # 1. BaseWindow Setup
        super().__init__("Manage Schedules", 1000, 600)
        
        self.db = DatabaseManager()
        self.current_edit_id = None 

        # 2. Fetch Data Objects
        self.movies = self.db.fetch_all_movies()
        self.halls = self.db.fetch_all_halls()

        if not self.halls:
            messagebox.showerror("Error", "No Halls found. Please add halls first.", parent=self)
            self.destroy()
            return

        # Prepare Lists for Comboboxes
        self.movie_titles = [m.title for m in self.movies]
        self.hall_names = [h.name for h in self.halls]

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Main Layout Container
        main_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # ==========================================
        # LEFT COLUMN: SCHEDULING FORM
        # ==========================================
        frame_left = tk.Frame(main_frame, width=350, bg="#f0f0f0")
        frame_left.pack(side="left", fill="y", padx=(0, 20))
        
        self.lbl_header = tk.Label(frame_left, text="Add Showtime", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.lbl_header.pack(anchor="w", pady=(0, 15))

        def add_label(text):
            tk.Label(frame_left, text=text, font=("Arial", 9, "bold"), bg="#f0f0f0", fg="#555").pack(anchor="w", pady=(5, 0))

        # 1. Movie Selection
        add_label("Select Movie:")
        self.cb_movie = ttk.Combobox(frame_left, values=self.movie_titles, state="readonly", font=("Arial", 10), width=35)
        self.cb_movie.pack(pady=(0, 10))

        # 2. Hall Selection
        add_label("Select Hall:")
        self.cb_hall = ttk.Combobox(frame_left, values=self.hall_names, state="readonly", font=("Arial", 10), width=35)
        self.cb_hall.pack(pady=(0, 10))

        # 3. Date Selection
        add_label("Date:")
        if DateEntry:
            self.cal_date = DateEntry(frame_left, width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=("Arial", 10))
        else:
            self.cal_date = tk.Entry(frame_left, font=("Arial", 10), width=30)
            self.cal_date.insert(0, "YYYY-MM-DD")
        self.cal_date.pack(pady=(0, 10))

        # 4. Time Slot
        add_label("Time Slot:")
        self.time_slots = ["12:00", "15:00", "18:00", "21:00"]
        self.cb_time = ttk.Combobox(frame_left, values=self.time_slots, state="readonly", font=("Arial", 10), width=35)
        self.cb_time.set("12:00") 
        self.cb_time.pack(pady=(0, 10))

        # 5. Price Input
        add_label("Price (₱):")
        self.entry_price = tk.Entry(frame_left, font=("Arial", 10), width=38)
        self.entry_price.insert(0, "350.00")
        self.entry_price.pack(pady=(0, 10))

        # Action Buttons
        self.btn_save = tk.Button(
            frame_left, text="Add Schedule", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
            pady=8, cursor="hand2", command=self.save_schedule
        )
        self.btn_save.pack(fill="x", pady=(20, 5))

        self.btn_clear = tk.Button(
            frame_left, text="Clear / Cancel", bg="#999", fg="white", font=("Arial", 10),
            pady=5, cursor="hand2", command=self.clear_form
        )
        self.btn_clear.pack(fill="x")

        tk.Button(
            frame_left, text="Delete Selected", bg="#f44336", fg="white", font=("Arial", 10),
            pady=5, cursor="hand2", command=self.delete_selected
        ).pack(fill="x", pady=(20,0))

        # ==========================================
        # RIGHT COLUMN: SCHEDULE LIST
        # ==========================================
        frame_right = tk.Frame(main_frame, bg="#f0f0f0")
        frame_right.pack(side="right", fill="both", expand=True)

        # Instructions Label
        tk.Label(
            frame_right, 
            text="Click row to Edit", 
            font=("Arial", 10, "italic"), 
            fg="#666", 
            bg="#f0f0f0"
        ).pack(anchor="nw", pady=(0, 5))

        # Data Table
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
        
        # Scrollbar sticks to right, Tree fills space
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_schedule_select)

    def on_schedule_select(self, event):
        sel = self.tree.selection()
        if not sel: return

        item = self.tree.item(sel)
        vals = item['values'] 
        
        self.current_edit_id = vals[0]
        
        # Populate Comboboxes based on text match
        if vals[3] in self.movie_titles:
            self.cb_movie.current(self.movie_titles.index(vals[3]))
        if vals[4] in self.hall_names:
            self.cb_hall.current(self.hall_names.index(vals[4]))
            
        # Set Date Field
        if DateEntry:
            self.cal_date.set_date(vals[1])
        else:
            self.cal_date.delete(0, 'end'); self.cal_date.insert(0, vals[1])
            
        # Set Time Field
        if vals[2] in self.time_slots:
            self.cb_time.set(vals[2])
        else:
            self.cb_time.set(vals[2]) 
        
        # Clean Price String
        price_clean = str(vals[5]).replace("₱", "").replace("$", "")
        self.entry_price.delete(0, 'end'); self.entry_price.insert(0, price_clean)

        # Update UI State
        self.lbl_header.config(text=f"Edit Schedule #{self.current_edit_id}", fg="#2196F3")
        self.btn_save.config(text="Update Schedule", bg="#2196F3")

    def save_schedule(self):
        movie_idx = self.cb_movie.current()
        hall_idx = self.cb_hall.current()
        
        if movie_idx == -1 or hall_idx == -1:
            messagebox.showerror("Error", "Please select a movie and a hall.", parent=self)
            return

        movie_id = self.movies[movie_idx].id
        hall_id = self.halls[hall_idx].id
        
        date_str = self.cal_date.get()
        time_str = self.cb_time.get()
        
        if not time_str:
             messagebox.showerror("Error", "Please select a time slot.", parent=self)
             return

        # Prepare Datetime Object
        try:
            dt_string = f"{date_str} {time_str}:00"
            final_datetime_obj = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
             messagebox.showerror("Error", "Invalid Date format. Use YYYY-MM-DD", parent=self)
             return
        
        try:
            price = float(self.entry_price.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.", parent=self)
            return

        if self.current_edit_id:
            # Update Existing
            success, msg = self.db.update_showtime(self.current_edit_id, movie_id, hall_id, final_datetime_obj, price)
            if success:
                messagebox.showinfo("Success", "Schedule updated!", parent=self)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Scheduling Failed", msg, parent=self)
        else:
            # Add New
            success, msg = self.db.add_showtime(movie_id, hall_id, final_datetime_obj, price)
            if success:
                messagebox.showinfo("Success", "Showtime added!", parent=self)
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Scheduling Failed", msg, parent=self)

    def clear_form(self):
        self.current_edit_id = None
        self.cb_time.set("12:00")
        self.entry_price.delete(0, 'end'); self.entry_price.insert(0, "350.00")
        self.cb_movie.set(''); self.cb_hall.set('')
        
        self.lbl_header.config(text="Add Showtime", fg="black")
        self.btn_save.config(text="Add Schedule", bg="#4CAF50")
        
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a schedule to delete.", parent=self)
            return

        if messagebox.askyesno("Confirm", "Delete this showtime?", parent=self):
            item_id = self.tree.item(sel)['values'][0]
            if self.db.delete_showtime(item_id):
                self.clear_form()
                self.load_data()
            else:
                messagebox.showerror("Error", "Could not delete. Check if tickets are sold.", parent=self)

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        showtimes = self.db.fetch_all_showtimes_full()
        
        for s in showtimes:
            dt = s.start_time
            # Handle potential string vs datetime differences safely
            if isinstance(dt, str):
                try:
                    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                except:
                    pass 
            
            if isinstance(dt, datetime):
                d_str = dt.strftime("%Y-%m-%d")
                t_str = dt.strftime("%H:%M")
            else:
                d_str = str(dt)
                t_str = ""

            self.tree.insert("", "end", values=(s.id, d_str, t_str, s.movie_title, s.hall_name, f"₱{s.price}"))

if __name__ == "__main__":
    AdminScheduler().run()