import mysql.connector

DB_CONFIG = { 'host': 'localhost', 'database': 'cinema_db', 'user': 'root', 'password': '' }

def nuke_and_rebuild():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("INITIATING TOTAL SYSTEM WIPE...")
    
    # 1. DISABLE FOREIGN KEYS (To prevents errors when dropping linked tables)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # 2. DYNAMICALLY FIND ALL TABLES (Stop guessing names)
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'cinema_db'")
    tables = [row[0] for row in cursor.fetchall()]
    
    if not tables:
        print("   - No tables found. Database is already empty.")
    else:
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"   - DROPPED table: {table}")
            
    # 3. RE-ENABLE CHECKS
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("Database is now completely empty.")
    
    print("\nBuilding Clean 3NF Schema...")

    # 1. USERS (Unified Admin/User table)
    cursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'admin'
    )
    """)
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'password123', 'admin')")

    # 2. HALLS
    cursor.execute("""
    CREATE TABLE halls (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        total_rows INT NOT NULL,
        total_cols INT NOT NULL
    )
    """)
    # Insert Default Halls
    hall_data = [
        ('Cinema 1', 8, 12), 
        ('Cinema 2', 10, 14),
        ('IMAX Theater', 12, 18), 
        ('VIP Lounge', 5, 8)
    ]
    cursor.executemany("INSERT INTO halls (name, total_rows, total_cols) VALUES (%s, %s, %s)", hall_data)

    # 3. MOVIES
    cursor.execute("""
    CREATE TABLE movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        genre VARCHAR(100),
        duration_minutes INT,
        rating VARCHAR(10),
        description TEXT,
        poster_path VARCHAR(255),
        director VARCHAR(100),
        cast TEXT,
        review TEXT,
        imdb_rating VARCHAR(20)
    )
    """)

    # 4. SHOWTIMES
    cursor.execute("""
    CREATE TABLE showtimes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT NOT NULL,
        hall_id INT NOT NULL,
        start_time DATETIME NOT NULL,
        price_standard DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        FOREIGN KEY (hall_id) REFERENCES halls(id) ON DELETE CASCADE
    )
    """)

    # 5. BOOKINGS (Transaction Header)
    cursor.execute("""
    CREATE TABLE bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100),
        total_amount DECIMAL(10,2),
        ticket_count INT,
        booking_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. TICKETS (Line Items)
    cursor.execute("""
    CREATE TABLE tickets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        booking_id INT NOT NULL,
        showtime_id INT NOT NULL,
        row_letter VARCHAR(5) NOT NULL,
        seat_num INT NOT NULL,
        price_at_purchase DECIMAL(10,2),
        FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
        FOREIGN KEY (showtime_id) REFERENCES showtimes(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("Schema Rebuilt Successfully.")

if __name__ == "__main__":
    nuke_and_rebuild()