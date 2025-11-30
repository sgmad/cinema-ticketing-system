from db.connection import create_connection

# =====================================================
# MOVIE MANAGEMENT (ADMIN)
# =====================================================

def add_movie(title, genre, duration, rating, description, poster_path):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO movies (title, genre, duration_minutes, rating, description, poster_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (title, genre, duration, rating, description, poster_path)
        try:
            cursor.execute(query, values)
            conn.commit()
            print("Movie added successfully!")
            return True
        except Exception as e:
            print(f"Error adding movie: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def delete_movie(movie_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Delete associated showtimes first (Cleanup)
            cursor.execute("DELETE FROM showtimes WHERE movie_id = %s", (movie_id,))
            
            # Delete the movie
            cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting movie: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def get_all_movies():
    """ Used by both Admin (list view) and Customer (home screen) """
    conn = create_connection()
    movies = []
    if conn:
        cursor = conn.cursor(dictionary=True) # Return results as dictionaries
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
    return movies

def get_all_halls():
    conn = create_connection()
    halls = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM halls")
        halls = cursor.fetchall()
        cursor.close()
        conn.close()
    return halls

def get_movies_by_date(target_date_str):
    """
    target_date_str format: 'YYYY-MM-DD'
    Returns list of movies playing on that specific date.
    """
    conn = create_connection()
    movies = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # distinct: ensures we don't get the same movie twice if it plays 5 times that day
        query = """
        SELECT DISTINCT m.* FROM movies m
        JOIN showtimes s ON m.id = s.movie_id
        WHERE DATE(s.start_time) = %s
        ORDER BY m.title
        """
        cursor.execute(query, (target_date_str,))
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
    return movies

# =====================================================
# SHOWTIME MANAGEMENT (ADMIN)
# =====================================================

def add_showtime(movie_id, hall_id, start_time, price):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO showtimes (movie_id, hall_id, start_time, price_standard)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (movie_id, hall_id, start_time, price))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding showtime: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def get_showtimes_for_movie(movie_id):
    conn = create_connection()
    results = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # CHANGED: Added h.total_rows and h.total_cols to the SELECT
        query = """
        SELECT s.id, s.start_time, s.price_standard, 
               h.name as hall_name, h.total_rows, h.total_cols
        FROM showtimes s
        JOIN halls h ON s.hall_id = h.id
        WHERE s.movie_id = %s AND s.start_time >= NOW()
        ORDER BY s.start_time ASC
        """
        cursor.execute(query, (movie_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return results

def get_taken_seats(showtime_id):
    """ Returns a set of tuples representing taken seats, e.g., {('A', 1), ('A', 2)} """
    conn = create_connection()
    taken_seats = set() # Using a set for fast lookups
    if conn:
        cursor = conn.cursor()
        query = "SELECT seat_row_label, seat_number FROM tickets WHERE showtime_id = %s"
        cursor.execute(query, (showtime_id,))
        rows = cursor.fetchall()
        for r in rows:
            # r[0] is 'A', r[1] is 1
            taken_seats.add((r[0], r[1]))
        cursor.close()
        conn.close()
    return taken_seats

def save_booking(showtime_id, customer_name, seat_list, total_price):
    """
    Saves a booking and its associated tickets in one atomic transaction.
    seat_list is a list of tuples: [('A', 1), ('A', 2)]
    Returns the new booking_id if successful, or None if failed.
    """
    conn = create_connection()
    booking_id = None
    
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Start Transaction
            conn.start_transaction()

            # 2. Create the Booking Record (The Receipt Header)
            query_booking = "INSERT INTO bookings (customer_name, total_amount) VALUES (%s, %s)"
            cursor.execute(query_booking, (customer_name, total_price))
            booking_id = cursor.lastrowid # Get the ID generated (e.g., Booking #101)

            # 3. Create the Ticket Records (The Individual Seats)
            query_ticket = """
            INSERT INTO tickets (booking_id, showtime_id, seat_row_label, seat_number, price)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            # Calculate price per ticket (total / count)
            price_per_ticket = total_price / len(seat_list)

            for row, number in seat_list:
                cursor.execute(query_ticket, (booking_id, showtime_id, row, number, price_per_ticket))

            # 4. Commit (Save everything permanently)
            conn.commit()
            print(f"Transaction successful! Booking ID: {booking_id}")
            
        except Exception as e:
            # If ANYTHING goes wrong, undo everything
            conn.rollback()
            print(f"Transaction failed: {e}")
            booking_id = None
        finally:
            cursor.close()
            conn.close()
            
    return booking_id

# =====================================================
# BOOKING MANAGEMENT (ADMIN)
# =====================================================

def get_all_bookings():
    """ Fetches all bookings with summary details """
    conn = create_connection()
    results = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # We join to get the Count of tickets for each booking
        query = """
        SELECT b.id, b.customer_name, b.booking_date, b.total_amount, 
               COUNT(t.id) as ticket_count, m.title
        FROM bookings b
        LEFT JOIN tickets t ON b.id = t.booking_id
        LEFT JOIN showtimes s ON t.showtime_id = s.id
        LEFT JOIN movies m ON s.movie_id = m.id
        GROUP BY b.id
        ORDER BY b.booking_date DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return results

def delete_booking(booking_id):
    """ Deletes a booking AND its associated tickets (Cascade delete) """
    conn = create_connection()
    success = False
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Delete Tickets first (Child records)
            cursor.execute("DELETE FROM tickets WHERE booking_id = %s", (booking_id,))
            
            # 2. Delete Booking (Parent record)
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
            
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error deleting booking: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return success

# =====================================================
# AUTHENTICATION
# =====================================================

def check_admin_login(username, password):
    conn = create_connection()
    user = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        # In a real app, use hashing (bcrypt) for passwords!
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    return user