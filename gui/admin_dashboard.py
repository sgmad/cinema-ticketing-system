import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from db.queries import get_all_movies, add_movie, delete_movie, create_connection
from gui.admin_scheduler import AdminScheduler
from gui.admin_bookings import AdminBookings
from gui.admin_halls import AdminHalls
import shutil
import os

class AdminDashboard:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Admin Dashboard - Movie Management")
        self.window.configure(bg="#f0f0f0")

        window_width = 1150
        window_height = 750
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.selected_image_path = None
        self.current_edit_id = None
        
        self.selected_image_path = None
        self.current_edit_id = None 

        # ==========================================
        # LEFT SIDE: FORM
        # ==========================================
        frame_left = tk.Frame(self.window, width=400, bg="#f0f0f0", padx=15, pady=15)
        frame_left.pack(side="left", fill="y")
        
        self.lbl_header = tk.Label(frame_left, text="Add New Movie", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.lbl_header.pack(pady=(10, 20))

        # Input Container
        input_frame = tk.Frame(frame_left, bg="#f0f0f0")
        input_frame.pack(fill="x")

        # Standard Helper
        def create_entry(label_text):
            tk.Label(input_frame, text=label_text, bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
            entry = tk.Entry(input_frame, font=("Arial", 10))
            entry.pack(fill="x", pady=(0, 5))
            return entry

        self.entry_title = create_entry("Movie Title:")
        self.entry_genre = create_entry("Genre:")
        
        # ROW 1: Duration | MPAA
        row1 = tk.Frame(input_frame, bg="#f0f0f0")
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Duration (min):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(side="left")
        self.entry_duration = tk.Entry(row1, width=10)
        self.entry_duration.pack(side="left", padx=(5, 20))
        
        tk.Label(row1, text="MPAA (e.g. PG-13):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(side="left")
        self.entry_mpaa = tk.Entry(row1, width=10)
        self.entry_mpaa.pack(side="left", padx=5)

        # ROW 2: IMDb Score
        row2 = tk.Frame(input_frame, bg="#f0f0f0")
        row2.pack(fill="x", pady=5)
        tk.Label(row2, text="IMDb Score (e.g. ★ 8.1):", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(side="left")
        self.entry_imdb = tk.Entry(row2, width=15)
        self.entry_imdb.pack(side="left", padx=5)

        # Tagline (Review field)
        tk.Label(input_frame, text="Tagline / Marketing Hook:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,0))
        self.entry_tagline = tk.Entry(input_frame, font=("Arial", 10))
        self.entry_tagline.pack(fill="x")

        # Description
        tk.Label(input_frame, text="Synopsis:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10,0))
        self.text_desc = tk.Text(input_frame, height=4, font=("Arial", 9))
        self.text_desc.pack(fill="x")

        # Image Selection
        self.btn_image = tk.Button(input_frame, text="Select Poster Image", command=self.select_image)
        self.btn_image.pack(fill="x", pady=(10, 5))
        self.lbl_image_status = tk.Label(input_frame, text="No image selected", fg="gray", bg="#f0f0f0", font=("Arial", 8))
        self.lbl_image_status.pack(pady=(0, 10))

        # ACTION BUTTONS
        btn_grid = tk.Frame(frame_left, bg="#f0f0f0")
        btn_grid.pack(fill="x", pady=10)

        self.btn_save = tk.Button(btn_grid, text="Save New Movie", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2, command=self.save_movie)
        self.btn_save.pack(fill="x", pady=2)
        
        self.btn_clear = tk.Button(btn_grid, text="Clear Form / Cancel", bg="#9E9E9E", fg="white", command=self.clear_form)
        self.btn_clear.pack(fill="x", pady=2)

        tk.Button(btn_grid, text="Delete Selected", bg="#f44336", fg="white", command=self.remove_movie).pack(fill="x", pady=(10, 2))

        # NAVIGATION
        tk.Label(frame_left, text="----------------", fg="#ccc", bg="#f0f0f0").pack(pady=10)
        
        tk.Button(frame_left, text="📅 Schedule Showtime", bg="#2196F3", fg="white", command=self.open_scheduler).pack(fill="x", pady=2)
        tk.Button(frame_left, text="📜 Manage Bookings", bg="#FF9800", fg="white", command=self.open_bookings).pack(fill="x", pady=2)
        tk.Button(frame_left, text="🏛 Manage Halls", bg="#607D8B", fg="white", command=lambda: AdminHalls().run()).pack(fill="x", pady=2)

        # ==========================================
        # RIGHT SIDE: TABLE
        # ==========================================
        frame_right = tk.Frame(self.window, bg="white", padx=20, pady=20)
        frame_right.pack(side="right", fill="both", expand=True)
        
        tk.Label(frame_right, text="Inventory List", font=("Arial", 12, "bold"), bg="white").pack(anchor="nw")

        columns = ("id", "title", "genre", "mpaa", "imdb")
        self.tree = ttk.Treeview(frame_right, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID"); self.tree.column("id", width=30)
        self.tree.heading("title", text="Title"); self.tree.column("title", width=200)
        self.tree.heading("genre", text="Genre"); self.tree.column("genre", width=100)
        self.tree.heading("mpaa", text="MPAA"); self.tree.column("mpaa", width=60)
        self.tree.heading("imdb", text="Score"); self.tree.column("imdb", width=80)

        scrollbar = ttk.Scrollbar(frame_right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_movie_select)
        self.refresh_table()

    # =========================================================
    # LOGIC
    # =========================================================
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")], parent=self.window)
        if file_path:
            self.selected_image_path = file_path
            self.lbl_image_status.config(text=f"New: {os.path.basename(file_path)}", fg="green")

    def on_movie_select(self, event):
        selected = self.tree.selection()
        if not selected: return

        self.current_edit_id = self.tree.item(selected)['values'][0]
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE id = %s", (self.current_edit_id,))
        movie = cursor.fetchone()
        conn.close()

        if movie:
            self.entry_title.delete(0, 'end'); self.entry_title.insert(0, movie['title'])
            self.entry_genre.delete(0, 'end'); self.entry_genre.insert(0, movie['genre'])
            self.entry_duration.delete(0, 'end'); self.entry_duration.insert(0, str(movie['duration_minutes']))
            self.entry_mpaa.delete(0, 'end'); self.entry_mpaa.insert(0, movie.get('rating', ''))
            self.entry_imdb.delete(0, 'end'); self.entry_imdb.insert(0, movie.get('imdb_rating', ''))
            self.entry_tagline.delete(0, 'end'); self.entry_tagline.insert(0, movie.get('review', '').replace('"', ''))
            self.text_desc.delete("1.0", 'end'); self.text_desc.insert("1.0", movie['description'])
            
            self.lbl_header.config(text=f"Editing Movie #{self.current_edit_id}", fg="#2196F3")
            self.btn_save.config(text="Update Movie", bg="#2196F3")

    def save_movie(self):
        title = self.entry_title.get()
        genre = self.entry_genre.get()
        duration = self.entry_duration.get()
        mpaa = self.entry_mpaa.get()
        imdb = self.entry_imdb.get()
        tagline = self.entry_tagline.get()
        desc = self.text_desc.get("1.0", "end-1c")

        if not title or not duration:
            messagebox.showerror("Error", "Title and Duration are required!", parent=self.window)
            return

        final_poster_path = None
        if self.selected_image_path:
            try:
                target_dir = "assets/sample_posters"
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                dest = os.path.join(target_dir, os.path.basename(self.selected_image_path))
                shutil.copy(self.selected_image_path, dest)
                final_poster_path = dest.replace("\\", "/")
            except Exception as e:
                messagebox.showerror("Error", f"Image copy failed: {e}", parent=self.window)
                return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            if self.current_edit_id:
                if final_poster_path:
                    query = """UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, rating=%s, description=%s, poster_path=%s, review=%s, imdb_rating=%s WHERE id=%s"""
                    vals = (title, genre, duration, mpaa, desc, final_poster_path, tagline, imdb, self.current_edit_id)
                else:
                    query = """UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, rating=%s, description=%s, review=%s, imdb_rating=%s WHERE id=%s"""
                    vals = (title, genre, duration, mpaa, desc, tagline, imdb, self.current_edit_id)
                
                cursor.execute(query, vals)
                conn.commit()
                messagebox.showinfo("Success", "Movie Updated!", parent=self.window)
            
            else:
                if not final_poster_path: final_poster_path = "assets/sample_posters/default.png"
                query = """INSERT INTO movies (title, genre, duration_minutes, rating, description, poster_path, review, imdb_rating) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                vals = (title, genre, duration, mpaa, desc, final_poster_path, tagline, imdb)
                cursor.execute(query, vals)
                conn.commit()
                messagebox.showinfo("Success", "Movie Created!", parent=self.window)

        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=self.window)
        finally:
            conn.close()
            
        self.clear_form()
        self.refresh_table()

    def clear_form(self):
        self.current_edit_id = None
        self.selected_image_path = None
        for entry in [self.entry_title, self.entry_genre, self.entry_duration, self.entry_mpaa, self.entry_imdb, self.entry_tagline]:
            entry.delete(0, 'end')
        self.text_desc.delete("1.0", 'end')
        
        self.lbl_header.config(text="Add New Movie", fg="black")
        self.btn_save.config(text="Save New Movie", bg="#4CAF50")
        self.lbl_image_status.config(text="No image selected", fg="gray")
        if self.tree.selection(): self.tree.selection_remove(self.tree.selection())

    def remove_movie(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Please select a movie.", parent=self.window)
            return

        movie_id = self.tree.item(sel)['values'][0]
        if messagebox.askyesno("Confirm", "Delete this movie?", parent=self.window):
            delete_movie(movie_id)
            self.clear_form()
            self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for m in get_all_movies():
            mpaa = m.get('rating', '')
            imdb = m.get('imdb_rating', '')
            self.tree.insert("", "end", values=(m['id'], m['title'], m['genre'], mpaa, imdb))

    def open_scheduler(self): AdminScheduler().run()
    def open_bookings(self): AdminBookings().run()
    def run(self): self.window.mainloop()

if __name__ == "__main__":
    AdminDashboard().run()