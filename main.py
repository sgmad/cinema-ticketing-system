import tkinter as tk
from gui.customer_home import CustomerHome

def main():
    root = tk.Tk()
    root.withdraw() # Hides the small blank window
    
    # Launch the Application Window
    app = CustomerHome()
    
    # Ensure closing the app kills the root
    # Without this, the process keeps running in the background
    app.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    
    # Start
    root.mainloop()

if __name__ == "__main__":
    main()