# ScreenPass Cinema Ticketing System

A Python-based desktop application for cinema management and ticket booking.

## Features
- **Dynamic Seat Mapping:** Automatically adjusts grid size for Standard, IMAX, and VIP halls.
- **Live Data Import:** Fetches "Now Playing" movies, cast, and taglines via TMDB API.
- **Smart Scheduling:** Prevents double-booking halls and rotates movies logically over a 14-day period.
- **Admin Dashboard:** Full CRUD control over Movies, Halls, Schedules, and Bookings.
- **Dark Mode UI:** Modern "Cyberpunk Violet" aesthetic with visual hierarchy.

## Installation
1. Install XAMPP and start Apache/MySQL.
2. Create a database named `cinema_db`.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Initialize the database and fetch movie data:
   `python setup_database.py`

## Usage
- **Run App:** `python main.py`
- **Admin Credentials:** `admin` / `password123`
