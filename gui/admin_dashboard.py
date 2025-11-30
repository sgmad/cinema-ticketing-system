import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from db.queries import get_all_movies, add_movie, delete_movie
from gui.admin_scheduler import AdminScheduler
from gui.admin_bookings import AdminBookings
from gui.admin_halls import AdminHalls
import shutil
import os

class AdminDashboard:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Admin Dashboard - Movie Management")
        # CHANGED: Increased height from 600 to 650 to fit the new buttons
        self.window.geometry("900x650") 
        
        self.selected_image_path = None

        # ==========================================
        # LEFT SIDE: FORM (Add Movie)
        # ==========================================
        frame_form = tk.Frame(self.window, width=300, padx=20, pady=20)
        frame_form.pack(side="left", fill="y")
        
        tk.Label(frame_form, text="Add New Movie", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Title
        tk.Label(frame_form, text="Movie Title:").pack(anchor="w")
        self.entry_title = tk.Entry(frame_form, width=30)
        self.entry_title.pack(pady=(0, 10))

        # Genre
        tk.Label(frame_form, text="Genre:").pack(anchor="w")
        self.entry_genre = tk.Entry(frame_form, width=30)
        self.entry_genre.pack(pady=(0, 10))

        # Duration
        tk.Label(frame_form, text="Duration (minutes):").pack(anchor="w")
        self.entry_duration = tk.Entry(frame_form, width=30)
        self.entry_duration.pack(pady=(0, 10))

        # Rating
        tk.Label(frame_form, text="Rating (e.g. PG-13):").pack(anchor="w")
        self.entry_rating = tk.Entry(frame_form, width=30)
        self.entry_rating.pack(pady=(0, 10))
        
        # Description
        tk.Label(frame_form, text="Description:").pack(anchor="w")
        self.text_desc = tk.Text(frame_form, width=30, height=5)
        self.text_desc.pack(pady=(0, 10))

        # Image Selection
        self.btn_image = tk.Button(frame_form, text="Select Poster Image", command=self.select_image)
        self.btn_image.pack(fill="x", pady=(0, 5))
        
        self.lbl_image_status = tk.Label(frame_form, text="No image selected", fg="gray", font=("Arial", 8))
        self.lbl_image_status.pack(pady=(0, 10)) # Reduced padding here

        # ==========================================
        # BUTTON GROUP 1: MOVIE ACTIONS
        # ==========================================
        # Save Button
        tk.Button(frame_form, text="Save Movie", bg="#4CAF50", fg="white", command=self.save_movie).pack(fill="x", pady=(5, 5))
        
        # CHANGED: Moved Delete Button UP so it's grouped with Save
        tk.Button(frame_form, text="Delete Selected Movie", bg="#f44336", fg="white", command=self.remove_movie).pack(fill="x")

        # ==========================================
        # BUTTON GROUP 2: SCHEDULING
        # ==========================================
        tk.Label(frame_form, text="----------------", fg="#ccc").pack(pady=15)

        tk.Button(
            frame_form, 
            text="📅 Schedule Showtime", 
            bg="#2196F3", fg="white", 
            height=2,
            command=self.open_scheduler
        ).pack(fill="x")

        tk.Button(
            frame_form, 
            text="📜 Manage Bookings", 
            bg="#FF9800", fg="white", 
            height=2,
            command=self.open_bookings
        ).pack(fill="x", pady=(5, 0))

        tk.Button(
            frame_form, 
            text="🏛 Manage Halls", 
            bg="#607D8B", fg="white", 
            height=2,
            command=lambda: AdminHalls().run()
        ).pack(fill="x", pady=(5, 0))

        # ==========================================
        # RIGHT SIDE: TABLE (View Movies)
        # ==========================================
        # (This part remains the same as your previous code)
        frame_table = tk.Frame(self.window)
        frame_table.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        columns = ("id", "title", "genre", "rating")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("rating", text="Rating")
        
        self.tree.column("id", width=30)
        self.tree.column("title", width=150)
        self.tree.column("genre", width=100)
        self.tree.column("rating", width=80)

        self.tree.pack(fill="both", expand=True)
        self.refresh_table()

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_image_status.config(text=f"Selected: {filename}", fg="green")

    def save_movie(self):
        # 1. Get data from form
        title = self.entry_title.get()
        genre = self.entry_genre.get()
        duration = self.entry_duration.get()
        rating = self.entry_rating.get()
        desc = self.text_desc.get("1.0", "end-1c")
        
        # Validation
        if not title or not duration:
            messagebox.showerror("Error", "Title and Duration are required!")
            return

        # 2. Handle Image Copying
        final_poster_path = "assets/sample_posters/default.png" # Fallback
        
        if self.selected_image_path:
            try:
                # Create directory if it doesn't exist
                target_dir = "assets/sample_posters"
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Define destination
                filename = os.path.basename(self.selected_image_path)
                destination = os.path.join(target_dir, filename)
                
                # Copy file
                shutil.copy(self.selected_image_path, destination)
                
                # Update path for DB (using forward slashes for consistency)
                final_poster_path = destination.replace("\\", "/")
            except Exception as e:
                messagebox.showerror("Image Error", f"Failed to copy image: {e}")
                return

        # 3. Save to Database
        success = add_movie(title, genre, int(duration), rating, desc, final_poster_path)
        
        if success:
            messagebox.showinfo("Success", "Movie added successfully!")
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showerror("Database Error", "Could not save movie.")

    def open_scheduler(self):
        scheduler = AdminScheduler()
        scheduler.run()

    def open_bookings(self):
        AdminBookings().run()

    def remove_movie(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a movie to delete.")
            return

        # Get the ID of the selected movie
        item_data = self.tree.item(selected_item)
        movie_id = item_data['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this movie?"):
            success = delete_movie(movie_id)
            if success:
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Failed to delete movie.")

    def refresh_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch from DB
        movies = get_all_movies()
        for m in movies:
            self.tree.insert("", "end", values=(m['id'], m['title'], m['genre'], m['rating']))

    def clear_form(self):
        self.entry_title.delete(0, 'end')
        self.entry_genre.delete(0, 'end')
        self.entry_duration.delete(0, 'end')
        self.entry_rating.delete(0, 'end')
        self.text_desc.delete("1.0", 'end')
        self.selected_image_path = None
        self.lbl_image_status.config(text="No image selected", fg="gray")

    def run(self):
        self.window.mainloop()

# For testing independently
if __name__ == "__main__":
    app = AdminDashboard()
    app.run()
