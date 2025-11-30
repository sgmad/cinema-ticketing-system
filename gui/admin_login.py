import tkinter as tk
from tkinter import messagebox
from db.queries import check_admin_login
import ctypes

# COLOR PALETTE
BG_COLOR = "#121212"
SURFACE_COLOR = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
ACCENT = "#BB86FC"
ACCENT_DARK = "#3700B3"

class AdminLogin:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Admin Login")
        self.window.configure(bg=BG_COLOR)
        
        # Remove standard window chrome (optional, but cleaner for modals)
        # self.window.overrideredirect(True) # Uncomment if you want NO title bar at all

        # =========================================================
        # HCI FIX: CENTER THE WINDOW
        # =========================================================
        window_width = 360
        window_height = 420
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Make the window modal
        self.window.transient() 
        self.window.grab_set()
        
        # Dark Title Bar Hack (Windows only)
        try:
            self.window.update()
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ctypes.windll.user32.GetParent
            hwnd = get_parent(self.window.winfo_id())
            value = ctypes.c_int(2)
            set_window_attribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except: pass

        # =========================================================
        # UI LAYOUT
        # =========================================================
        
        # Container with padding
        main_frame = tk.Frame(self.window, bg=BG_COLOR, padx=30, pady=30)
        main_frame.pack(expand=True, fill="both")

        # Icon / Header
        tk.Label(
            main_frame, 
            text="🔒", 
            font=("Segoe UI Emoji", 40), 
            bg=BG_COLOR, fg=ACCENT
        ).pack(pady=(0, 10))

        tk.Label(
            main_frame, 
            text="Admin Access", 
            font=("Helvetica", 18, "bold"), 
            bg=BG_COLOR, fg=TEXT_MAIN
        ).pack(pady=(0, 20))

        # Helper to create styled inputs
        def create_input(label_text, is_password=False):
            tk.Label(
                main_frame, text=label_text, 
                font=("Helvetica", 9, "bold"), 
                bg=BG_COLOR, fg="#888888", anchor="w"
            ).pack(fill="x", pady=(10, 5))
            
            entry = tk.Entry(
                main_frame, 
                font=("Helvetica", 11), 
                bg=SURFACE_COLOR, 
                fg=TEXT_MAIN,
                insertbackground=ACCENT, # Cursor color
                relief="flat",
                highlightthickness=1,
                highlightbackground="#333",
                highlightcolor=ACCENT, # Purple border on focus
                bd=5 # Internal padding
            )
            entry.pack(fill="x")
            if is_password: entry.config(show="•")
            return entry

        self.entry_user = create_input("USERNAME")
        self.entry_pass = create_input("PASSWORD", is_password=True)

        # Login Button
        btn_login = tk.Button(
            main_frame, 
            text="LOGIN", 
            font=("Helvetica", 10, "bold"),
            bg=ACCENT, 
            fg="#000000",
            activebackground=ACCENT_DARK,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.attempt_login
        )
        btn_login.pack(fill="x", pady=(30, 0))
        
        # Bind "Enter" key
        self.window.bind('<Return>', lambda event: self.attempt_login())

        # Focus username immediately
        self.entry_user.focus_set()

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        user = check_admin_login(username, password)

        if user:
            self.window.destroy()
            from gui.admin_dashboard import AdminDashboard
            dashboard = AdminDashboard()
            dashboard.run()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")

    def run(self):
        self.window.mainloop()
