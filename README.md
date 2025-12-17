# 🎬 ScreenPass Cinema Ticketing System

> A comprehensive, 3-tier desktop application for cinema management and ticket reservations, built with Python, Tkinter, and MySQL.

## 📖 Overview

**ScreenPass** is a dual-interface software solution designed to simulate a real-world cinema ecosystem. It features a visual, immersive **Customer Kiosk** for browsing movies and booking seats, and a robust **Admin Dashboard** for managing inventory, scheduling, and sales reports.

The system implements a strict **3-Tier Architecture** (Presentation, Logic, Data), utilizes **Object-Oriented Design Patterns** (Singleton, Factory, DTO), and integrates with **The Movie Database (TMDB) API** for automated content ingestion.

---

## 🚀 Key Features

### 👤 Customer Kiosk (Front-End)
* **Visual Catalog:** Grid-based movie browsing with high-res posters and hover effects.
* **Real-Time Schedule:** Groups showtimes by date and format (IMAX, VIP, Standard).
* **Interactive Seat Map:** Dynamically renders seat layouts based on hall configuration. Handles collision detection for sold seats in real-time.
* **Digital Receipt:** Generates a transaction summary with a procedurally generated QR code.

### 🛡️ Admin Portal (Back-End)
* **Inventory Management:** CRUD operations for Movies with auto-fill via TMDB.
* **Smart Scheduling:** Drag-and-drop style scheduling with **automatic conflict detection** logic.
* **Hall Configurator:** Define physical dimensions (Rows x Columns) and pricing strategies using a Factory Pattern.
* **Sales Reporting:** View booking history, calculate totals, and process refunds (Cascade Deletion).

### ⚙️ Core Technology
* **Automated Scraper (ETL):** Fetches "Now Playing" movies from TMDB, cleans data, and downloads/caches assets locally.
* **3NF Database Schema:** Normalized MySQL database ensuring data integrity.
* **Custom UI Framework:** Built on `tkinter` with a custom `BaseWindow` class for consistent Dark Mode theming and window management.

---

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **GUI Framework:** Tkinter (Standard Library)
* **Database:** MySQL / MariaDB
* **External API:** TMDB (The Movie Database)
* **Key Libraries:** * `mysql-connector-python` (Database Connectivity)
    * `requests` (API Handling)
    * `Pillow` (Image Processing)
    * `tkcalendar` (Date Selection)

---

## 📂 System Architecture

The project follows a modular structure to separate concerns:

```text
ScreenPass/
├── assets/             # Cached movie posters and icons
├── db/                 # Database Layer
│   ├── db_manager.py   # Singleton Database Access Object (DAO)
│   └── schema_init.sql # Database definition
├── gui/                # Presentation Layer (Tkinter)
│   ├── base_window.py  # Parent class for all UI windows
│   ├── customer_*.py   # Customer-facing screens
│   └── admin_*.py      # Admin management screens
├── models/             # Logic Layer (DTOs)
│   ├── movie.py        # Movie Object
│   ├── showtime.py     # Showtime Logic
│   └── hall.py         # Hall Factory & Polymorphism
├── scraper.py          # ETL Script for TMDB
└── main.py             # Application Entry Point

```

---

## ⚡ Installation & Setup

### Prerequisites

* Python 3.x installed.
* MySQL Server installed and running locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/YourUsername/CinemaTicketingSystem.git](https://github.com/YourUsername/CinemaTicketingSystem.git)
cd CinemaTicketingSystem

```

### 2. Install Dependencies

```bash
pip install mysql-connector-python requests Pillow tkcalendar

```

### 3. Initialize the Database

Run the rebuild script to create the `cinema_db` database and seed it with default halls and admin users.

```bash
python nuke_and_rebuild.py

```

> **Note:** Ensure your MySQL credentials in `db/db_manager.py` match your local server (Default: `root` / `password: empty`).

### 4. Fetch Movie Data

Populate the database with real-world movie data using the scraper.

```bash
python scraper.py

```

---

## 🖥️ Usage

### Run the Application

Launch the main customer interface:

```bash
python main.py

```

### Access Admin Dashboard

1. On the Home Screen, click the **"Admin Portal"** button in the top right.
2. **Default Credentials:**
* **Username:** `admin`
* **Password:** `password123`



---

## 🧩 Key Mechanisms Explained

### The Seat Map Algorithm

The seat map in `gui/seat_map.py` is **content-aware**. It queries the `halls` table for dimensions (e.g., 10 rows, 14 cols) and dynamically calculates the window size and button grid layout. It then overlays `taken_seats` from the `tickets` table to disable specific buttons.

### The Scheduler Logic

The `extend_schedule` function uses a **"Card Dealer" algorithm**. It identifies "Anchor" movies (Top 2 popular) and rotates the remaining catalog in batches of 4 every 3 days. This ensures a diverse schedule that mimics real cinema programming.

---

## 📜 License

This project is for educational purposes. Movie data provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).
